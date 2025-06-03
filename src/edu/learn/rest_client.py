import json
import requests

def get_places(input_text):
    with open("src/edu/learn/config.json", "r") as config_file:
        config = json.load(config_file)
        api_key = config["GOOGLE_API_KEY"]

    url = "https://places.googleapis.com/v1/places:autocomplete"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key
    }

    data = {
        "input": input_text,
        "includedRegionCodes": ["in"],
        "includedPrimaryTypes": ["locality"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        return [suggestion["placePrediction"]["text"]["text"] for suggestion in response_data["suggestions"]]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
