import json
from api import get_weather_data_5, get_city_coordinates
from dotenv import load_dotenv
import os
import subprocess
import threading

load_dotenv()  # This loads the environment variables from .env
BASE_PATH = os.getenv('BASE_PATH') # Path to save your JSONS
CITIES_PATH = os.getenv('CITIES_PATH') # Path to fetch your list of cities to work on
SCRAPY_PATH = os.getenv('SCRAPY_PATH')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

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

def get_all_cities_weather(cities, api_key=RAPID_API_KEY):
    all_cities_weather = {}
    for city in cities:
        latitude, longitude = get_city_coordinates(city)
        print(f"Getting weather data for {city}: {latitude}, {longitude}")
        # you get a JSON for 1 city with 40 keys
        weather_json = get_weather_data_5(latitude, longitude, city, api_key)
        # Save the city weather data in case the loop crash
        save_city_weather(weather_json, city)
        all_cities_weather.update(weather_json)
    print("loop done")
    save_city_weather(all_cities_weather)
    print("all_cities_weather JSON saved")
    # keep only the cities_weather.json file
    cleanup_json_files()

def run_scrapy_spider():    
    # Change the current working directory to your Scrapy project directory
    os.chdir(SCRAPY_PATH)
    # Define the Scrapy command    
    command = "scrapy crawl hotel -o output.json"
    subprocess.run(command, shell=True, check=True)

# Run
# * output.json (scrapy) and cities_weather.json (API calls) have the same key on 'city' from CITIES_PATH
# Main execution logic
if __name__ == "__main__":
    # Load cities from JSON
    with open(CITIES_PATH) as f:
        cities = json.load(f)
        print(cities)
    # Start the scrapy spider in a separate thread
    # output.json (scrapy)
    scrapy_thread = threading.Thread(target=run_scrapy_spider)
    scrapy_thread.start()

    # Meanwhile, run the weather data collection
    # cities_weather.json (API calls)
    get_all_cities_weather(cities)

    # Wait for the scrapy thread to finish
    scrapy_thread.join()
        
    #! forgot to add the lat/long to the JSON
    # data = {}
    # for city in cities:
    #     latitude, longitude = get_city_coordinates(city)
    #     data[city] = {"latitude": latitude, "longitude": longitude}

    # path = '/Users/antoinebertin/Documents/jedha/full_stack/projects_full_stack/kayak/latitude_longitude.json'
    # with open(path, 'w') as f:
    #     json.dump(data, f, indent=4)