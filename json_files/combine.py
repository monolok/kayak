import json
import os

def combine_json_files_unique_entries(directory_path):
    combined_data = {}
    # Loop through all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            # Open and load the JSON data
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Check if data is not None
                if data:
                    key = filename.split('_')[0]  # Splitting by '_' to get city name
                    # Avoiding nested city names by checking the structure
                    if key in data and isinstance(data[key], dict):
                        combined_data[key] = data[key]
                    else:
                        combined_data[key] = data
                else:
                    print(f"Warning: The file {filename} is empty or not a valid JSON.")
    # Save the combined data to a new JSON file
    combined_file_path = os.path.join(directory_path, "combined_weather_data_unique.json")
    with open(combined_file_path, 'w') as combined_file:
        json.dump(combined_data, combined_file, indent=4)
    return combined_file_path

# Specify the directory containing the JSON files
directory_path = '/Users/antoinebertin/Documents/jedha/full_stack/projects_full_stack/kayak/json_files'
# Adjusted function to ensure unique city entries without nested city names
combined_file_path_unique = combine_json_files_unique_entries(directory_path)
combined_file_path_unique
