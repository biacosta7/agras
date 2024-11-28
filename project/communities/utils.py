import requests
import json

def get_weather_data(city):
    API_KEY = "912a26af15a25a457046937106614b08"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # Usa .json() para converter a resposta diretamente em JSON

        if data:
            return {
                'temperature': int(data['main']['temp']),
                'weather_description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            return {'error': 'Dados meteorológicos não encontrados.'}

    except requests.exceptions.RequestException as e:
        return {'error': f"Erro na requisição: {e}"}
    except (KeyError, IndexError) as e:
        return {'error': 'Erro ao processar os dados da API.'}
