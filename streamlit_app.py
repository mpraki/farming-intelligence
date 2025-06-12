import streamlit as st

from src.edu.learn.csv_utils import *
from src.edu.learn.gemini_client import *
from src.edu.learn.rest_client import *

st.title("Farming Intelligence User Input")


# Collect user input
def main():
    st.header("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    soil_type = st.text_input("Soil Type")
    soil_quality = st.selectbox("Soil Quality", ["Poor", "Average", "Good", "Excellent"])
    # Collect user input for location
    location_input = st.text_input("Type your location")
    suggestions = get_places(location_input) if location_input else []

    # Select box with dynamic options
    location = st.selectbox("Location", options=suggestions)
    submit = st.button("Submit")

    if submit:
        st.success(f"Thank you, {name}! Your data has been recorded.")
        st.write({
            'Name': name,
            'Age': age,
            'Soil Type': soil_type,
            'Soil Quality': soil_quality,
            'Location': location
        })
        save_user_input(name, age, soil_type, soil_quality, location)

    place = location
    soil_type = soil_type
    farm_size = "4 acres"
    irrigation_source = "Well"
    irrigation_type = "Drip irrigation"
    crop_type = "cash crop"
    labor_availability = "available"
    crop_duration = "yearly"
    example = '{"crop_name": "Tomato", "description": "Tomato is a warm-season crop that thrives in sandy soil with good drainage. It requires moderate irrigation and can be grown in well-drained areas.", "profit": "high", "duration": "3 months"}'

    text1 = f"Based on the following details, what crops should I grow for each of the season? Place: {place}, Soil Type: {soil_type}, Farm Size: {farm_size}, Irrigation Source: {irrigation_source}, Irrigation Type: {irrigation_type}, Crop Type: {crop_type}, Labor Availability: {labor_availability}, Crop Duration: {crop_duration}. Please give me only the crop names in json format with the crop in the crop_name field and your input for the the crop in description field. Example response: ${example}"
    pd.DataFrame(get_gemini_api_url(text1))

    st.line_chart(data=get_line_chart_data(), x='Name', y='Age')
    bar_data = get_bar_chart_data()
    print(bar_data)
    st.bar_chart(data=bar_data, x='Soil Type', y='Count')


if __name__ == "__main__":
    main()
