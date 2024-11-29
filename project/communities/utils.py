import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Usa .json() para converter a resposta diretamente em JSON

        if data:
            return {
                'temperature': int(data['main']['temp']),
                'weather_description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'], 
                'feels_like': int(data['main']['feels_like']),  
                'wind_speed': data['wind']['speed'], 
            }
        else:
            return {'error': 'Dados meteorológicos não encontrados.'}

    except requests.exceptions.RequestException as e:
        return {'error': f"Erro na requisição: {e}"}
    except (KeyError, IndexError) as e:
        return {'error': 'Erro ao processar os dados da API.'}
