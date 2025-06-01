import pandas as pd
import os

def save_user_input(name, age, soil_type, soil_quality, filename='user_inputs.csv'):
    """
    Save user input to a CSV file using pandas. Creates the file with headers if it doesn't exist.
    """
    data = {
        'Name': [name],
        'Age': [age],
        'Soil Type': [soil_type],
        'Soil Quality': [soil_quality]
    }
    df = pd.DataFrame(data)
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

def get_line_chart_data(filename='user_inputs.csv'):
    """
    Read the CSV file and return a DataFrame for line chart plotting.
    """
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        return df
    else:
        return pd.DataFrame(columns=['Name', 'Age', 'Soil Type', 'Soil Quality'])
    
def get_bar_chart_data(filename='user_inputs.csv'):
    """
    Read the CSV file and return a DataFrame for bar chart plotting.
    """
    if os.path.isfile(filename):
        df = pd.read_csv(filename)

        return df.groupby('Soil Type').size().reset_index(name='Count')
    else:
        return pd.DataFrame(columns=['Name', 'Age', 'Soil Type', 'Soil Quality'])