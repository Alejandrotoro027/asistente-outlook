import re

PALABRAS_SPAM = [
    "gratis", "oferta", "urgente", "dinero", "premio", "haz clic", "click aquí",
    "ganador", "descuento", "compra ahora", "free", "deal", "win", "prize", "click here",
    "limited time", "offer", "smooth silky skin", "save big"
]

def es_spam(asunto, cuerpo, remitente):
    texto = f"{asunto} {cuerpo}".lower()
    for palabra in PALABRAS_SPAM:
        if palabra in texto:
            return True
    if re.search(r"\[\w{5,}\]", asunto):  # ejemplo: [fOBgm]
        return True
    return False


