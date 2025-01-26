from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Field, Schema, List
from pymongo import MongoClient
import requests
import arrow
from datetime import datetime
from utils.rate_limiter import RateLimiter  # Importazione assoluta

# Configurazione Flask
app = Flask(__name__)

# Connessione a MongoDB
client = MongoClient('mongodb://mongo:27017/')  # "mongo" è il nome del servizio in Docker Compose
db = client['weather_db']
collection = db['weather_data']

# Rate Limiter (10 chiamate al giorno)
rate_limiter = RateLimiter(max_calls=10, period=86400)  # 86400 secondi = 1 giorno

# Funzione per ottenere i dati da Stormglass
def fetch_weather_data():
    if not rate_limiter.allow_request():
        raise Exception("Limite di chiamate giornaliere raggiunto")

    # Configura la richiesta all'API di Stormglass
    start = arrow.now().floor('day')
    end = arrow.now().ceil('day')
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            #setto le coordinate di Cenesi Caput Mundi
            'lat': 44.077511,
            'lng': 8.137869,
            'params': ','.join(['waveHeight', 'airTemperature']),
            'start': start.to('UTC').timestamp(), 
            'end': end.to('UTC').timestamp() 
        },
        headers={
            'Authorization': 'd6b4c7cc-461f-11ec-bf98-0242ac130002-d6b4c8b2-461f-11ec-bf98-0242ac130002' 
        }
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Errore durante la richiesta all'API: {response.status_code}")

# Endpoint REST per ottenere e salvare i dati
@app.route('/fetch-weather', methods=['GET'])
def fetch_and_save_weather():
    try:
        # Ottieni i dati da Stormglass
        weather_data = fetch_weather_data()

        # Salva i dati in MongoDB
        document = {
            'timestamp': datetime.now(),
            'data': weather_data
        }
        collection.insert_one(document)

        return jsonify({"status": "success", "message": "Dati salvati con successo"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Definizione del tipo GraphQL per i dati meteo
class WeatherType(ObjectType):
    timestamp = String()
    data = Field(lambda: WeatherDataType)

class WeatherDataType(ObjectType):
    waveHeight = Field(lambda: WaveHeightType)
    airTemperature = Field(lambda: AirTemperatureType)

class WaveHeightType(ObjectType):
    value = String()
    unit = String()

class AirTemperatureType(ObjectType):
    value = String()
    unit = String()

# Definizione delle query GraphQL
class Query(ObjectType):
    weather_data = List(WeatherType)

    def resolve_weather_data(self, info):
        # Recupera tutti i dati salvati in MongoDB
        documents = collection.find()
        return [WeatherType(timestamp=str(doc['timestamp']), data=doc['data']) for doc in documents]

# Creazione dello schema GraphQL
schema = Schema(query=Query)

# Aggiungi GraphQL al server Flask
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)