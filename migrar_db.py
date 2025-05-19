import sqlite3

conn = sqlite3.connect("correos.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE correos ADD COLUMN origen_clasificacion TEXT DEFAULT 'automatica'")
    print("✅ Columna 'origen_clasificacion' agregada correctamente.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ La columna 'origen_clasificacion' ya existe.")
    else:
        raise

conn.commit()
conn.close()
