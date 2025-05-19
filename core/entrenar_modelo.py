import sqlite3
import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from core.modelo import limpiar_texto

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "correos.db")
MODELO_PATH = os.path.join(BASE_DIR, "modelo_entrenado.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

def entrenar_modelo():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT asunto, es_spam FROM correos")
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        print("⚠️ No hay datos para entrenar el modelo.")
        return

    asuntos = [limpiar_texto(asunto) for asunto, _ in datos]
    etiquetas = [etiqueta for _, etiqueta in datos]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(asuntos)

    modelo = MultinomialNB()
    modelo.fit(X, etiquetas)

    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("✅ Modelo entrenado y guardado correctamente.")

if __name__ == "__main__":
    entrenar_modelo()
