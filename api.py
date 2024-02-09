import requests
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

def get_city_coordinates(city_name):
    #https://nominatim.openstreetmap.org/search?<params>
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1  # We only need the top result
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            return None, None
    else:
        print(f"Failed to get data for {city_name}, status code: {response.status_code}")
        return None, None

#! 50 calls/month for free
def get_weather_data_5(latitude, longitude, city_name):
    base_url = "https://open-weather13.p.rapidapi.com"
    url = f"{base_url}/city/fivedaysforcast/{latitude}/{longitude}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json() # len(data['list']) => 40
        
        #Construct JSON to return 
        city_json = {city_name: {}}
        for index, item in enumerate(data['list']):
            timestamp = item['dt']
            time = item['dt_txt']
            pop = item['pop']
            temp_min_kelvin = item['main']['temp_min']
            temp_max_kelvin = item['main']['temp_max']
            main_weather = item['weather'][0]['main']

            weather_info = {
            'timestamp': timestamp,
            'time': time,
            'pop': pop,
            'temp_min_kelvin': temp_min_kelvin,
            'temp_max_kelvin': temp_max_kelvin,
            'main_weather': main_weather}

            city_json[city_name][index] = weather_info
        return city_json
    else:
        print(f"Failed to get data for {city_name}, status code: {response.status_code}")
        return None
