import json

from google import genai
from google.genai import types

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    api_key = config["GOOGLE_API_KEY"]


def get_first_response():
    place = "Attur"
    soil_type = "red loamy soil"
    farm_size = "4 acres"
    irrigation_source = "Well"
    irrigation_type = "Drip irrigation"
    crop_type = "cash crop"
    labor_availability = "available"
    crop_duration = "yearly"

    prompt = f"Based on the following details, what crops should I grow? Place: {place}, Soil Type: {soil_type}, Farm Size: {farm_size}, Irrigation Source: {irrigation_source}, Irrigation Type: {irrigation_type}, Crop Type: {crop_type}, Labor Availability: {labor_availability}, Crop Duration: {crop_duration}. Please give me only the crop names."

    # Configure the client and tools
    client = genai.Client(api_key=api_key)
    # Send request with function declarations
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
        contents=prompt,
    )
    return response.text


def get_recommended_crop(crop_name: str) -> str:
    return "Crop Name: " + crop_name


def get_second_response():
    # Define the function declaration for the model
    crop_function = {
        "name": "get_recommended_crop",
        "description": "Gets the recommended crop for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "crop_name": {
                    "type": "string",
                    "description": "The name of the crop to be grown, e.g. Tomato",
                }
            },
            "required": ["crop_name"],
        },
    }
    # Configure the client and tools
    client2 = genai.Client(api_key=api_key)
    tools = types.Tool(function_declarations=[types.FunctionDeclaration(**crop_function)])
    config2 = types.GenerateContentConfig(tools=[tools], temperature=0.2)
    # Send request with function declarations
    first_response = get_first_response()
    print(first_response)

    response2 = client2.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Content(
                role="user", parts=[types.Part(
                    text="Given the following details, recommend all the crops and call the get_recommended_crop function with the crop name." + first_response)]
            )
        ],
        config=config2,
    )
    print(response2)

    for part in response2.candidates[0].content.parts:
        function_call = part.function_call
        if not function_call:
            print("No function call found in the response.")
            print(part.text)

        if function_call:
            print(f"Function call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
            if function_call.name == "get_recommended_crop":
                crop_name = function_call.args.get("crop_name", "")
                result = get_recommended_crop(crop_name)
                print(f"Result: {result}")

    if not response2.candidates[0].content.parts:
        print("Unexpectede response from LLM.")
        print(response2.text)


get_second_response()
