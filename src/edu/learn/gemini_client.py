import json

from google import genai
from google.genai import types


def get_gemini_api_url(text: str) -> str:
    with open("src/edu/learn/config.json", "r") as config_file:
        config = json.load(config_file)
        api_key = config["GOOGLE_API_KEY"]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are expert in farming and agriculture.",
            max_output_tokens=800,
            temperature=0.2
        ),
        contents=text
    )

    print(response.text)
    return response.text


