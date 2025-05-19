import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

DB_PATH = "correos.db"
MODELO_PATH = "modelo_entrenado.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

def entrenar_modelo():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT asunto, es_spam FROM correos")
    datos = cursor.fetchall()
    conn.close()

    if not datos or len(set([d[1] for d in datos])) < 2:
        raise ValueError("Se necesitan ejemplos de al menos dos clases (spam y no spam) para entrenar el modelo.")

    asuntos = [d[0] for d in datos]
    etiquetas = [int(d[1]) for d in datos]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(asuntos)

    modelo = LogisticRegression()
    modelo.fit(X, etiquetas)

    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

def cargar_modelo():
    if os.path.exists(MODELO_PATH) and os.path.exists(VECTORIZER_PATH):
        modelo = joblib.load(MODELO_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

        return lambda asunto: modelo.predict(vectorizer.transform([asunto]))
    return None




