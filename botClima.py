from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from deep_translator import GoogleTranslator
from sklearn.pipeline import Pipeline
import tkinter as tk
import numpy as np
import importlib
import requests
import json
import re

city = ""
watingActivity = False

# Lee los archivos JSON
with open("BotData/questions.json", "r") as file:
    questions = json.load(file)["questions"]
    
with open("BotData/answers.json", "r") as file:
    answers = json.load(file)["answers"]

# Entrenar el modelo
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])
x_train = questions
y_train = answers
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
        "cnt": 1 
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
        is_hot = main['temp'] > 30 
        # Verificar si hace mucho frío
        is_cold = main['temp'] < 0 
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
def get_response(entrada):
    match = cosine_similarity(pipeline.named_steps["tfidf"].transform([entrada]), pipeline.named_steps["tfidf"].transform(x_train))
    best_match = np.argmax(match)
    return answers[best_match]


def chatbot(message,text_chat):
    global city
    global watingActivity

    gui= importlib.import_module("gui")
    text_chat =gui.text_chat

    if(city == ""):
        city = message
        text_chat.insert(tk.END, f"Sky: {get_weather(city)}\n¿Quisieras saber algo más?\nEscriba 'Salir' para finalizar.\n",'Sky')
    elif(watingActivity):
        text_chat.insert(tk.END, f"Sky: {get_activity_recommendation(city,message)}\n")
        watingActivity = False
    else:
        options(get_response(message),text_chat)

def options(message,text_chat):
    global city
    global watingActivity
 
    if message == "weather_now":
        text_chat.insert(tk.END, f"Sky: {get_detailed_weather(city)}\n")
    elif message == "air_quality":
        text_chat.insert(tk.END, f"Sky: {get_air_pollution(city)}\n")
    elif message == "weather_future":
        text_chat.insert(tk.END, f"Sky: {get_forecast(city)}\n")
    elif message == "activity_suggestion":
        text_chat.insert(tk.END, f"Sky: ¿Qué actividad planeas realizar? (ejemplo: correr, nadar, etc.) \n")
        watingActivity = True
    elif message == "change_city":
        text_chat.insert(tk.END, "Sky: ¿En qué ciudad quieres saber el clima?\n")
        city = ""
    elif message == "quit":
        text_chat.insert(tk.END, f"Sky: ¡Saludos! Que tengas un gran día :)")
        quit()
    else:
        text_chat.insert(tk.END, f"Sky: {message}\n")
    
def fast_answer(entry):
    return get_response(entry)