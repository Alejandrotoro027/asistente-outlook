from flask import Flask, redirect, request, session, render_template, send_file
import os
import csv
import io
from core import auth, eliminador, db
from core.modelo import entrenar_modelo

app = Flask(__name__)
app.secret_key = os.urandom(24)

db.inicializar_db()

@app.template_filter("formatear_fecha")
def formatear_fecha(fecha_str):
    return fecha_str.replace("T", " ")[:19] if fecha_str else "-"

@app.route("/")
def home():
    logged_in = "token" in session
    return render_template("index.html", logged_in=logged_in)

@app.route("/login")
def login():
    auth_url = auth.build_auth_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token = auth.get_token_from_code(code)
    session["token"] = token
    return redirect("/")

@app.route("/limpieza")
def limpieza_intermedia():
    token = session.get("token")
    if not token:
        return redirect("/login")
    return render_template("procesando.html")

@app.route("/limpieza_real")
def limpieza_real():
    token = session.get("token")
    if not token:
        return redirect("/login")
    try:
        eliminados, movidos = eliminador.procesar_correos(token)
        return render_template("resultados.html", eliminados=eliminados, movidos=movidos)
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/entrenar")
def entrenar():
    try:
        entrenar_modelo()
        return render_template("entrenamiento.html", exito=True)
    except Exception as e:
        return render_template("entrenamiento.html", exito=False, error=str(e))

@app.route("/entrenar/revisar", methods=["GET", "POST"])
def revisar_clasificaciones():
    if request.method == "POST":
        id_correo = request.form.get("id")
        es_spam = request.form.get("es_spam") == "1"
        nueva_clasificacion = request.form.get("clasificacion")
        db.actualizar_clasificacion(id_correo, es_spam, nueva_clasificacion)

    filtro = request.args.get("filtro", "todos")
    correos = db.obtener_clasificaciones_pendientes(filtro)
    return render_template("revisar_clasificaciones.html", correos=correos, filtro=filtro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/historial")
def historial():
    remitente = request.args.get("remitente", "").strip()
    tipo = request.args.get("tipo", "")
    clasificacion = request.args.get("clasificacion", "")
    revisado = request.args.get("revisado", "")
    pagina_rev = int(request.args.get("pagina_rev", 1))
    pagina_no = int(request.args.get("pagina_no", 1))
    por_pagina = 10

    todos_los_correos = db.obtener_todos(remitente=remitente, tipo=tipo, clasificacion=clasificacion, revisado=revisado)

    revisados = [c for c in todos_los_correos if c[7]]
    no_revisados = [c for c in todos_los_correos if not c[7]]

    total_rev = len(revisados)
    total_no = len(no_revisados)

    total_paginas_rev = max(1, (total_rev + por_pagina - 1) // por_pagina)
    total_paginas_no = max(1, (total_no + por_pagina - 1) // por_pagina)

    rev_paginados = revisados[(pagina_rev - 1) * por_pagina: pagina_rev * por_pagina]
    no_paginados = no_revisados[(pagina_no - 1) * por_pagina: pagina_no * por_pagina]

    return render_template("historial.html",
        revisados=rev_paginados,
        no_revisados=no_paginados,
        pagina_rev=pagina_rev,
        pagina_no=pagina_no,
        total_paginas_rev=total_paginas_rev,
        total_paginas_no=total_paginas_no,
        por_pagina=por_pagina,
        remitente=remitente,
        tipo=tipo,
        clasificacion=clasificacion,
        revisado=revisado
    )

@app.route("/historial/exportar")
def exportar_csv():
    remitente = request.args.get("remitente", "").strip()
    tipo = request.args.get("tipo", "")
    clasificacion = request.args.get("clasificacion", "")
    revisado = request.args.get("revisado", "")
    todos = db.obtener_todos(remitente=remitente, tipo=tipo, clasificacion=clasificacion, revisado=revisado)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Asunto", "Remitente", "Carpeta", "Es SPAM", "Procesado En", "Clasificación", "Revisado Manual", "Origen Clasificación"])
    for fila in todos:
        writer.writerow(fila)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="historial_correos.csv"
    )
