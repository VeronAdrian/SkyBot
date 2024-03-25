from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import json
import re

import requests
import tkinter as tk
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

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
pipeline.fit(x_train, y_train)

def connect_api(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def get_weather(city):
    data = connect_api(city)
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        country = data["sys"]["country"]
        
        weather_desc = GoogleTranslator(source='english', target='spanish').translate(weather_desc)
        
        return f"El clima en {city} {country}, es {weather_desc} con una temperatura de {temperature} grados Celsius."
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."

def get_daily_forecast(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/forecast/daily?"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "cnt": 1 # Solicita el pronóstico para el día actual
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def get_detailed_weather(city):
    data = connect_api(city)
    forecast_data = get_daily_forecast(city)
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        # Verificar si está lloviendo
        is_raining = 'Rain' in weather['main']
        # Verificar si hay tormenta
        is_stormy = any(x in weather['description'].lower() for x in ['storm', 'thunderstorm'])
        # Verificar si hay nieve
        is_snowing = 'Snow' in weather['main']
        # Verificar si hace mucho calor
        is_hot = main['temp'] > 30 # Ajusta este umbral según lo que consideres "mucho calor"
        # Verificar si hace mucho frío
        is_cold = main['temp'] < 0 # Ajusta este umbral según lo que consideres "mucho frío"
        is_cloudy = 'Clouds' in weather['main']
        
        weather_desc = GoogleTranslator(source='english', target='spanish').translate(weather['description'])

        detailed_info = f"El clima en {city} es {weather_desc} con una temperatura de {main['temp']} grados Celsius, presión atmosférica de {main['pressure']} hPa, humedad del {main['humidity']}% y velocidad del viento de {wind['speed']} m/s."
        
        # Extraer la temperatura mínima y máxima del día actual
        min_temp = forecast_data['list'][0]['temp']['min']
        max_temp = forecast_data['list'][0]['temp']['max']
        detailed_info += f" La temperatura mínima del día es de {min_temp} y la máxima es de {max_temp} grados Celsius."
        
        if is_raining:
            detailed_info += " Actualmente está lloviendo."
        else:
            detailed_info += " Actualmente no está lloviendo."
        
        if is_stormy:
            detailed_info += " Hay tormenta en la zona."
        
        if is_snowing:
            detailed_info += " Está nevando."
        
        if is_hot:
            detailed_info += " Hace mucho calor."
        
        if is_cold:
            detailed_info += " Hace mucho frío."
        
        if is_cloudy and weather_desc != "pocas nubes":
            detailed_info += " Está nublado."
        
        return detailed_info
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."

def get_forecast(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["cod"] != "404":
        forecast_list = data["list"]
        forecast_info = []
        for forecast in forecast_list:
            date_time = forecast["dt_txt"]
            temperature = forecast["main"]["temp"]
            weather_desc = forecast["weather"][0]["description"]
            weather_desc = GoogleTranslator(source='english', target='spanish').translate(weather_desc)
            forecast_info.append(f"Fecha y hora: {date_time}, Temperatura: {temperature} grados Celsius, Descripción: {weather_desc}")
        return "\n".join(forecast_info)
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."

def get_activity_recommendation(city, activity):
    weather_desc = get_detailed_weather(city)
    if "Actualmente está lloviendo" in weather_desc:
        return f"No es recomendable {activity} en {city} debido a que está lloviendo."
    elif "nublado" in weather_desc:
        return f"Podrías considerar {activity} en {city}, aunque está nublado."
    elif "tormenta" in weather_desc:
        return f"No es recomendable {activity} en {city} debido a que está lloviendo."
    elif "mucho calor" in weather_desc and activity != "nadar":
        return f"No es recomendable {activity} en {city} debido a que hace mucho calor."
    elif "nevando" in weather_desc and activity != "snow":
        return f"No es recomendable {activity} en {city} debido a que está nevando."
    else:
        return f"El clima en {city} es adecuado para {activity}. ¡Disfruta tu día!"

def get_coordinates(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/geo/1.0/direct?"
    params = {
        "q": city,
        "limit": 1,
        "appid": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

def get_air_pollution(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."
    
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution?"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        air_quality_index = data["list"][0]["main"]["aqi"]
        aqi_category = categorize_aqi(air_quality_index)
        
        return f"La calidad del aire en {city} es {air_quality_index}, lo que corresponde a la categoría: {aqi_category}."
    else:
        return "Error al obtener datos de contaminación del aire. Código de estado: " + str(response.status_code)

# Define AQI categories
aqi_categories = [
    (1, 'Bueno'), (2, 'Regular'), (3, 'Moderado'),
    (4, 'Malo'), (5, 'Muy malo')
]

def categorize_aqi(aqi_value):
    for value, category in aqi_categories:
        if aqi_value <= value:
            return category
    return None

# Función para obtener la respuesta
def obtener_respuesta(entrada):
    similaridad = cosine_similarity(pipeline.named_steps["tfidf"].transform([entrada]), pipeline.named_steps["tfidf"].transform(x_train))
    mejor_respuesta_idx = np.argmax(similaridad)
    return respuestas[mejor_respuesta_idx]


def chatbot(mensaje):
    global city
    global watingActivity

    if(city == ""):
        city = mensaje
        texto_chat.insert(tk.END, f"Sky: {get_weather(city)}\n")
    elif(watingActivity):
        texto_chat.insert(tk.END, f"Sky: {get_activity_recommendation(city,mensaje)}\n")
        watingActivity = False
    else:
        opciones(obtener_respuesta(mensaje))

def opciones(mensaje):
    global city
    global watingActivity
 
    if mensaje == "weather_now":
        texto_chat.insert(tk.END, f"Sky: {get_detailed_weather(city)}\n")
    elif mensaje == "air_quality":
        texto_chat.insert(tk.END, f"Sky: {get_air_pollution(city)}\n")
    elif mensaje == "weather_future":
        texto_chat.insert(tk.END, f"Sky: {get_forecast(city)}\n")
    elif mensaje == "activity_suggestion":
        texto_chat.insert(tk.END, f"Sky: ¿Qué actividad planeas realizar? (ejemplo: correr, nadar, etc.) \n")
        watingActivity = True
    elif mensaje == "change_city":
        texto_chat.insert(tk.END, "Sky: ¿En qué ciudad quieres saber el clima?\n")
        city = ""
    elif mensaje == "quit":
        texto_chat.insert(tk.END, f"Sky: ¡Saludos! Que tengas un gran día :)")
        quit()
    else:
        texto_chat.insert(tk.END, f"Sky: {mensaje}\n")
    
def enviar_mensaje():
    mensaje = entry_mensaje.get()
    if mensaje:
        texto_chat.config(state=tk.NORMAL)
        texto_chat.insert(tk.END, f"Usuario: {mensaje}\n")
        chatbot(mensaje)
        # Aquí puedes agregar la lógica para procesar el mensaje y obtener una respuesta
        # Por ejemplo, si el mensaje es "clima Madrid", puedes llamar a get_weather("Madrid")
        # y luego mostrar la respuesta en el área de texto del chat.
        # Por ahora, solo mostramos el mensaje del usuario.
        texto_chat.config(state=tk.DISABLED)
        entry_mensaje.delete(0, tk.END)

# Crea la ventana principal
ventana = tk.Tk()
ventana.title("Chatbot de Clima")

# Crea un marco para el chat
frame_chat = tk.Frame(ventana)
frame_chat.pack()

# Crea un área de texto para mostrar el chat
texto_chat = tk.Text(frame_chat, width=60, height=30, wrap="word")
texto_chat.pack(side=tk.LEFT)

# Crea un scrollbar para la ventana de texto
scrollbar = tk.Scrollbar(frame_chat, command=texto_chat.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
texto_chat.config(yscrollcommand=scrollbar.set)

# Establece los estilos de texto
texto_chat.tag_config('Usuario', background='#DCF8C6')
texto_chat.tag_config('Chatbot', background='#C2DFFF')

# Mensaje inicial del chatbot
texto_chat.config(state=tk.NORMAL)
texto_chat.insert(tk.END, "Sky: ¡Hola! Soy tu asistente de clima. ¿En qué ciudad quieres saber el clima?:\n")
texto_chat.config(state=tk.DISABLED)

# Crea un campo de entrada para el mensaje
entry_mensaje = tk.Entry(ventana, width=50)
entry_mensaje.pack()

# Crea un botón para enviar el mensaje
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack()

city = ""
watingActivity = False


# Ejecuta la aplicación
ventana.mainloop()

# Crea la ventana principal
ventana = tk.Tk()
ventana.title("Chatbot de Clima")

# Crea un marco para el chat
frame_chat = tk.Frame(ventana)
frame_chat.pack()

# Crea un área de texto para mostrar el chat
texto_chat = tk.Text(frame_chat, width=60, height=30, wrap="word")
texto_chat.pack(side=tk.LEFT)

# Crea un scrollbar para la ventana de texto
scrollbar = tk.Scrollbar(frame_chat, command=texto_chat.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
texto_chat.config(yscrollcommand=scrollbar.set)

# Establece los estilos de texto
texto_chat.tag_config('Usuario', background='#DCF8C6')
texto_chat.tag_config('Chatbot', background='#C2DFFF')

# Mensaje inicial del chatbot
texto_chat.config(state=tk.NORMAL)
texto_chat.insert(tk.END, "Sky: ¡Hola! Soy tu asistente de clima. ¿En qué ciudad quieres saber el clima?:\n")
texto_chat.config(state=tk.DISABLED)

# Crea un campo de entrada para el mensaje
entry_mensaje = tk.Entry(ventana, width=50)
entry_mensaje.pack()

# Crea un botón para enviar el mensaje
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack()

city = ""
watingActivity = False

# Ejecuta la aplicación
ventana.mainloop()
