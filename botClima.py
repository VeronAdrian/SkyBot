import requests

def get_weather(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"El clima en {city} es {weather_desc} con una temperatura de {temperature} grados Celsius."
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."

def get_detailed_weather(city):
    api_key = "931aa658cbbb2c158a8171e9ef2bfb90"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        detailed_info = f"El clima en {city} es {weather['description']} con una temperatura de {main['temp']} grados Celsius, presión atmosférica de {main['pressure']} hPa, humedad del {main['humidity']}% y velocidad del viento de {wind['speed']} m/s."
        return detailed_info
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."

    

def chatbot():
    while True:
        city = input("¿En qué ciudad quieres saber el clima? (Escribe 'salir' para terminar): ")
        if city.lower() == "salir":
            break
        print(get_weather(city))
        print("Opciones:")
        print("1. Ver pronóstico del tiempo para los próximos días")
        print("2. Ver detalles del clima actual")
        print("3. Salir")
        option = input("Elige una opción: ")
        if option == "1":
            print(get_weather(city))
        elif option == "2":
            print(get_detailed_weather(city))
            pass
        elif option == "3":
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 3.")

if __name__ == "__main__":
    chatbot()


