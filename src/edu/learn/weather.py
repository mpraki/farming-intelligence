import json

from google import genai
from google.genai import types

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    api_key = config["GOOGLE_API_KEY"]


def get_current_temperature(loc: str) -> str:
    return "Temp at " + loc + ": 32 degrees Celsius"


# Define the function declaration for the model
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

# Configure the client and tools
client = genai.Client(api_key=api_key)
tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="What's the temperature in Attur, Salem and Amsterdam?",
    config=config,
)

print(response)

for part in response.candidates[0].content.parts:
    function_call = part.function_call
    if function_call:
        print(f"Function call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        if function_call.name == "get_current_temperature":
            location = function_call.args.get("location", "")
            result = get_current_temperature(location)
            print(f"Result: {result}")
    else:
        print("No function call found in the response.")
        print(response.text)
