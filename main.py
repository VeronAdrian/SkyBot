from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import json
import re

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

# Función para extraer números de una cadena de texto
def obtener_numeros(text):
    return re.findall(r'\d+', text)

# Función para resolver operaciones matemáticas
def resolver_operacion(text):
    numeros = obtener_numeros(text)
    if len(numeros) != 2:
        return "Lo siento, no puedo entender la operación."
    operador = re.search(r'[\+\-\*/]', text).group()
    if operador == '+':
        return int(numeros[0]) + int(numeros[1])
    elif operador == '-':
        return int(numeros[0]) - int(numeros[1])
    elif operador == '*':
        return int(numeros[0]) * int(numeros[1])
    elif operador == '/':
        if int(numeros[1]) == 0:
            return "División por cero no está permitida."
        else:
            return int(numeros[0]) / int(numeros[1])
    else:
        return "Operador no válido."

# Función para obtener la respuesta
def obtener_respuesta(entrada):
    similaridad = cosine_similarity(pipeline.named_steps["tfidf"].transform([entrada]), pipeline.named_steps["tfidf"].transform(x_train))
    mejor_respuesta_idx = np.argmax(similaridad)
    if(respuestas[mejor_respuesta_idx] == "matematica"):
        return resolver_operacion(entrada)
    else:
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