import json, os

from google import genai
from google.genai import types


def get_gemini_api_url(text: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
        api_key = config["GOOGLE_API_KEY"]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Answer in limerick",
            max_output_tokens=800,
            temperature=0.9
        ),
        contents=text
    )

    print(response.text)
    return response.text

if __name__ == "__main__":
    get_gemini_api_url("describe about sun")
