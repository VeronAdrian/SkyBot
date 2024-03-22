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
    
import requests

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
            forecast_info.append(f"Fecha y hora: {date_time}, Temperatura: {temperature} grados Celsius, Descripción: {weather_desc}")
        return "\n".join(forecast_info)
    else:
        return "Ciudad no encontrada. Por favor, verifica el nombre de la ciudad."
    

def chatbot():
    city=selectCity()
    menu(city)
    
def selectCity():
    city = input("¿En qué ciudad quieres saber el clima?: ")
    if city.lower() != "salir":
        print(get_weather(city))
    return city


def menu(city):
    while True:
        print("Menú:")
        print("1. Ver pronóstico del tiempo para los próximos días")
        print("2. Ver detalles del clima actual")
        print("3. Elegir otra ciudad")
        print("4. Salir")
        option = input("Elige una opción: ")
        if option == "1":
            print(get_forecast(city))
        elif option == "2":
            print(get_detailed_weather(city))
        elif option == "3":
            city = selectCity()
        elif option == "4":
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 3.")

if __name__ == "__main__":
    chatbot()


