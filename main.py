import json
from api import get_weather_data_5, get_city_coordinates
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env
BASE_PATH = os.getenv('BASE_PATH') # Path to save your JSONS
CITIES_PATH = os.getenv('CITIES_PATH') # Path to fetch your list of cities to work on

# load the cities
with open(CITIES_PATH) as f:
    cities = json.load(f)

def save_city_weather(data, city="cities", base_path=BASE_PATH):
    path = f"{base_path}/{city}_weather.json"
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def cleanup_json_files(base_path=BASE_PATH, keep_file="cities_weather.json"):
    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)
        # Check if the current file is not the file we want to keep
        if filename != keep_file:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {filename}")

def get_all_cities_weather(cities):
    all_cities_weather = {}
    for city in cities:
        latitude, longitude = get_city_coordinates(city)
        # you get a JSON for 1 city with 40 keys
        weather_json = get_weather_data_5(latitude, longitude, city)
        # Save the city weather data in case the loop crash
        save_city_weather(city, weather_json)
        all_cities_weather.update(weather_json)
    print("loop done")
    save_city_weather(all_cities_weather)
    print("all_cities_weather JSON saved")
    # keep only the cities_weather.json file
    cleanup_json_files()

# Run
get_all_cities_weather(cities)
