import os
import json
from google import genai
from google.genai import types

def get_crop_recommendations(
    place,
    soil_type,
    farm_size,
    irrigation_source,
    irrigation_type,
    crop_type,
    labor_availability,
    crop_duration
):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
        api_key = config["GOOGLE_API_KEY"]

    text1 = (
        f"Based on the following details, what crops should I grow? "
        f"Place: {place}, Soil Type: {soil_type}, Farm Size: {farm_size}, "
        f"Irrigation Source: {irrigation_source}, Irrigation Type: {irrigation_type}, "
        f"Crop Type: {crop_type}, Labor Availability: {labor_availability}, Crop Duration: {crop_duration}. "
        "Give me the crop names and reason. Be precise and concise."
    )
    client = genai.Client(api_key=api_key)
    response1 = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are an expert in agriculture and farming. Provide crop recommendations based on the user's input for different seasons(like months) of the year. Be precise and concise.",
            max_output_tokens=800,
            temperature=0.9
        ),
        contents=text1
    )

    # Define the function declaration for the model
    crop_function = {
        "name": "format_crop_recommendations",
        "description": "format crop recommendations.",
        "parameters": {
            "type": "object",
            "properties": {
                "crop_name": {
                    "type": "string",
                    "description": "Crop Name (e.g. Tomato)",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for recommendation (e.g. Tomato is a warm-season crop that thrives in sandy soil with good drainage.)",
                },
            },
        },
    }

    tools = types.Tool(function_declarations=[crop_function])
    config = types.GenerateContentConfig(tools=[tools])

    function_instruction = (
        "Extract the crop name and reason from the following text and call the function "
        "'format_crop_recommendations' with these values:\n\n"
    )
    prompt_for_function = function_instruction + response1.text

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_for_function,
        config=config,
    )

    results = []
    for part in response.candidates[0].content.parts:
        function_call = part.function_call
        if function_call and function_call.name == "format_crop_recommendations":
            crop_name = function_call.args.get("crop_name", "")
            reason = function_call.args.get("reason", "")
            results.append({
                "crop_name": crop_name,
                "reason": reason
            })
    return results


