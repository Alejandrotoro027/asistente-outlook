import requests
from core.db import guardar_correo, obtener_clasificaciones_pendientes
from core.modelo import cargar_modelo

PALABRAS_CLAVE_SPAM = [
    "promoción", "descuento", "gratis", "compra", "oferta",
    "free", "discount", "buy now", "limited time", "offer", "save",
    "Smooth Silky Skin", "deal", "claim", "winner", "Exclusive Offer"
]

CLASIFICACIONES = {
    "trabajos": ["trabajo", "postulación", "oferta laboral", "entrevista", "empleo", "cv", "currículum"],
    "bancos": ["estado de cuenta", "transferencia", "pago", "banco", "saldo disponible"],
    "compras": ["factura", "pedido", "compra", "mercado libre", "amazon", "aliexpress"],
}

def es_spam_basico(asunto):
    return any(p in asunto.lower() for p in PALABRAS_CLAVE_SPAM)

def clasificar_tematica(asunto):
    asunto_lower = asunto.lower()
    for categoria, palabras in CLASIFICACIONES.items():
        if any(palabra in asunto_lower for palabra in palabras):
            return categoria
    return None

def obtener_id_carpeta(nombre_carpeta, carpetas):
    for carpeta in carpetas:
        if carpeta.get("displayName", "").lower() == nombre_carpeta.lower():
            return carpeta.get("id")
    return None

def procesar_correos(access_token):
    ya_procesados = {row[0]: row for row in obtener_clasificaciones_pendientes()}
    url = "https://graph.microsoft.com/v1.0/me/mailFolders"
    headers = {"Authorization": f"Bearer {access_token}"}
    carpetas_res = requests.get(url, headers=headers)

    if carpetas_res.status_code != 200:
        raise Exception(f"No se pudo obtener carpetas: {carpetas_res.status_code}")

    carpetas = carpetas_res.json().get("value", [])
    eliminados, movidos = [], []
    modelo = cargar_modelo()

    for carpeta in carpetas:
        folder_id = carpeta.get("id")
        folder_name = carpeta.get("displayName") or "desconocida"

        mensajes_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages?$top=100"
        mensajes_res = requests.get(mensajes_url, headers=headers)
        if mensajes_res.status_code != 200:
            continue

        mensajes = mensajes_res.json().get("value", [])

        for msg in mensajes:
            mensaje_id = msg.get("id")
            asunto = msg.get("subject", "(sin asunto)")
            remitente = msg.get("from", {}).get("emailAddress", {}).get("address", "")

            if mensaje_id in ya_procesados:
                fila = ya_procesados[mensaje_id]
                revisado_manual = fila[7]
                es_spam = fila[4]
                clasificacion = fila[6]
                origen = "manual" if revisado_manual else "automatica"

                if es_spam:
                    requests.delete(f"https://graph.microsoft.com/v1.0/me/messages/{mensaje_id}", headers=headers)
                    eliminados.append((asunto, remitente))
                elif clasificacion:
                    destino_id = obtener_id_carpeta(clasificacion, carpetas)
                    if destino_id:
                        move_body = {"destinationId": destino_id}
                        requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mensaje_id}/move", headers=headers, json=move_body)
                        movidos.append((asunto, remitente, clasificacion))
                continue

            # No ha sido procesado antes
            if modelo:
                try:
                    es_spam = modelo.predict([asunto])[0] == 0
                except Exception:
                    es_spam = es_spam_basico(asunto)
            else:
                es_spam = es_spam_basico(asunto)

            clasificacion = clasificar_tematica(asunto)

            if es_spam:
                requests.delete(f"https://graph.microsoft.com/v1.0/me/messages/{mensaje_id}", headers=headers)
                eliminados.append((asunto, remitente))
                guardar_correo(mensaje_id, asunto, remitente, folder_name, 1, "eliminar", origen_clasificacion="automatica")
            elif clasificacion:
                destino_id = obtener_id_carpeta(clasificacion, carpetas)
                if destino_id:
                    move_body = {"destinationId": destino_id}
                    requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mensaje_id}/move", headers=headers, json=move_body)
                    movidos.append((asunto, remitente, clasificacion))
                guardar_correo(mensaje_id, asunto, remitente, clasificacion, 0, clasificacion, origen_clasificacion="automatica")
            else:
                if folder_name.lower() in ["correo no deseado", "junkemail"]:
                    inbox_id = obtener_id_carpeta("inbox", carpetas)
                    if inbox_id:
                        move_body = {"destinationId": inbox_id}
                        requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mensaje_id}/move", headers=headers, json=move_body)
                        movidos.append((asunto, remitente, "inbox"))
                guardar_correo(mensaje_id, asunto, remitente, folder_name, 0, None, origen_clasificacion="automatica")

    return eliminados, movidos

