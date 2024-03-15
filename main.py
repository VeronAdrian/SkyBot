from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import json

# Lee los archivos JSON
with open("recursos/preguntas.json", "r") as archivo:
    preguntas = json.load(archivo)["preguntas"]
    
with open("recursos/respuestas.json", "r") as archivo:
    respuestas = json.load(archivo)["respuestas"]

# Entrenar el modelo
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])
x_train = preguntas
y_train = respuestas

# Función para obtener la respuesta
def obtener_respuesta(entrada):
    similaridad = cosine_similarity(pipeline.named_steps["tfidf"].transform([entrada]), pipeline.named_steps["tfidf"].transform(x_train))
    mejor_respuesta_idx = np.argmax(similaridad)
    return respuestas[mejor_respuesta_idx]

def main():
    pipeline.fit(x_train, y_train)
    # Interacción con el usuario
    print("¡Hola! Soy un chatbot. Puedes empezar a hacerme preguntas. Para salir, escribe 'salir'.")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == "salir":
            print("¡Hasta luego!")
            break
        else:
            respuesta = obtener_respuesta(entrada)
            print("ChatBot:", respuesta)

if __name__ == "__main__":
    main()