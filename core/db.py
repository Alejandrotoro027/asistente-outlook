import sqlite3
from datetime import datetime

def inicializar_db():
    conn = sqlite3.connect("correos.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS correos (
            id TEXT PRIMARY KEY,
            asunto TEXT,
            remitente TEXT,
            carpeta TEXT,
            es_spam INTEGER,
            procesado_en TEXT,
            clasificacion TEXT,
            revisado_manual INTEGER DEFAULT 0,
            origen_clasificacion TEXT DEFAULT 'automatica'
        )
    """)

    # Verificar si la columna 'origen_clasificacion' existe, y agregarla si no
    c.execute("PRAGMA table_info(correos)")
    columnas = [col[1] for col in c.fetchall()]
    if "origen_clasificacion" not in columnas:
        c.execute("ALTER TABLE correos ADD COLUMN origen_clasificacion TEXT DEFAULT 'automatica'")

    conn.commit()
    conn.close()

def guardar_correo(id, asunto, remitente, carpeta, es_spam, clasificacion=None, origen_clasificacion='automatica'):
    conn = sqlite3.connect("correos.db")
    c = conn.cursor()
    procesado_en = datetime.now().isoformat()
    c.execute("""
        INSERT OR IGNORE INTO correos (
            id, asunto, remitente, carpeta, es_spam, procesado_en, clasificacion, revisado_manual, origen_clasificacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (id, asunto, remitente, carpeta, int(es_spam), procesado_en, clasificacion, origen_clasificacion))
    conn.commit()
    conn.close()

def obtener_todos(remitente="", tipo="", clasificacion="", revisado=""):
    conn = sqlite3.connect("correos.db")
    c = conn.cursor()
    query = """
        SELECT id, asunto, remitente, carpeta, es_spam, procesado_en, clasificacion, revisado_manual, origen_clasificacion
        FROM correos
        WHERE 1=1
    """
    params = []

    if remitente:
        query += " AND LOWER(remitente) LIKE ?"
        params.append(f"%{remitente.lower()}%")

    if tipo == "spam":
        query += " AND es_spam = 1"
    elif tipo == "no_spam":
        query += " AND es_spam = 0"

    if clasificacion:
        query += " AND clasificacion = ?"
        params.append(clasificacion)

    if revisado == "revisados":
        query += " AND revisado_manual = 1"
    elif revisado == "no_revisados":
        query += " AND (revisado_manual IS NULL OR revisado_manual = 0)"

    query += " ORDER BY procesado_en DESC"

    c.execute(query, params)
    datos = c.fetchall()
    conn.close()
    return datos

def actualizar_clasificacion(id, es_spam, clasificacion):
    conn = sqlite3.connect("correos.db")
    c = conn.cursor()
    c.execute("""
        UPDATE correos
        SET es_spam = ?, clasificacion = ?, revisado_manual = 1, origen_clasificacion = 'manual'
        WHERE id = ?
    """, (int(es_spam), clasificacion, id))
    conn.commit()
    conn.close()

def obtener_clasificaciones_pendientes(filtro="todos"):
    conn = sqlite3.connect("correos.db")
    c = conn.cursor()
    query = """
        SELECT id, asunto, remitente, carpeta, es_spam, procesado_en, clasificacion, revisado_manual, origen_clasificacion
        FROM correos
        WHERE 1=1
    """
    if filtro == "revisados":
        query += " AND revisado_manual = 1"
    elif filtro == "no_revisados":
        query += " AND (revisado_manual IS NULL OR revisado_manual = 0)"

    query += " ORDER BY procesado_en DESC"
    c.execute(query)
    datos = c.fetchall()
    conn.close()
    return datos
