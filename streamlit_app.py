import streamlit as st
from src.edu.learn.csv_utils import *

st.title("Farming Intelligence User Input")

# Collect user input
def main():
    st.header("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    soil_type = st.text_input("Soil Type")
    soil_quality = st.selectbox("Soil Quality", ["Poor", "Average", "Good", "Excellent"])
    submit = st.button("Submit")

    if submit:
        st.success(f"Thank you, {name}! Your data has been recorded.")
        st.write({
            'Name': name,
            'Age': age,
            'Soil Type': soil_type,
            'Soil Quality': soil_quality
        })
    save_user_input(name, age, soil_type, soil_quality)
    st.line_chart(data=get_line_chart_data(), x='Name', y='Age')
    bar_data=get_bar_chart_data()
    print(bar_data)
    st.bar_chart(data=bar_data, x='Soil Type', y='Count')


if __name__ == "__main__":
    main()
