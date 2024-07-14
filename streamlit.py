import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

# Streamlit app
st.title('Taxi Recommendation System')

# Load the data from Excel files
final_weekday = pd.read_csv("assets/processed_data/final_weekday_streamlit.csv")
final_weekend = pd.read_csv("assets/processed_data/final_weekend_streamlit.csv")

# Input for origin coordinates
origins = st.text_input("Enter the origin coordinates (latitude, longitude)", value='1.2780, 103.8404')

# Initialize session state variables
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'skip_clicked' not in st.session_state:
    st.session_state.skip_clicked = False

# Function to calculate distance and duration
def calculate_distance_duration(origin, destination, API_KEY):
    distance_matrix_url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}"
        f"&destinations={destination}&departure_time=now&key={API_KEY}"
    )
    response = requests.get(distance_matrix_url)
    data = response.json()
    return data

# Function to get the recommended location
def get_recommended_location():
    # Get the current datetime
    current_datetime = datetime.now() - timedelta(hours=1)

    # Extract the time in HH:MM format
    time_str = current_datetime.strftime("%H:%M")

    # Get the next hour
    nearest_next_hour = current_datetime.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    nearest_next_hour_str = nearest_next_hour.strftime("%H:%M")

    # Determine if it's a weekday or weekend
    day_type = "Weekend" if nearest_next_hour.weekday() >= 5 else "Weekday"

    time_remaining = nearest_next_hour - current_datetime
    time_remaining_minutes = time_remaining.total_seconds() / 60

    #st.write(f'Time to the next hour, {nearest_next_hour_str} is {round(time_remaining_minutes)} minutes')
    #st.write(f'Iteration starting from hexagon with highest crowd-to-taxi ratio')
    #st.write('')

    # Select the appropriate DataFrame based on the day type
    if day_type == 'Weekday':
        recommended_df = final_weekday[[nearest_next_hour_str, 'h3_index', 'latitude', 'longitude']]
    else:
        recommended_df = final_weekend[[nearest_next_hour_str, 'h3_index', 'latitude', 'longitude']]

    recommended_df = recommended_df.sort_values(ascending=False, by=nearest_next_hour_str)

    API_KEY = st.secrets["google"]["api_key"]
    
    # Loop through the DataFrame starting from the stored index
    for i in range(st.session_state.index, len(recommended_df)):
        lat = recommended_df.iloc[i]['latitude']
        long = recommended_df.iloc[i]['longitude']
        h3_index = recommended_df.iloc[i]['h3_index']
        destinations = f'{lat}, {long}'

        data = calculate_distance_duration(origins, destinations, API_KEY)
        #st.write(f'Target destination: {h3_index} h3_index')

        if data['status'] == 'OK':
            distance = data['rows'][0]['elements'][0]['distance']['text']
            duration_str = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
            #st.write(f'Calculating time required: {duration_str}')

            # Convert duration to minutes
            duration_parts = duration_str.split()
            if 'hour' in duration_str:
                hours = int(duration_parts[0])
                minutes = int(duration_parts[2])
                duration = hours * 60 + minutes
            else:
                duration = int(duration_parts[0])

            if duration < time_remaining_minutes:
                #st.write('')
                #st.write(f'Please go to the {lat:.4f} latitude and {long:.4f} longitude, located at {h3_index} h3_index')
                # Google Maps JavaScript API URL for displaying the route
                maps_url = f"https://www.google.com/maps/embed/v1/directions?key={API_KEY}&origin={origins}&destination={destinations}"
                st.write(f'<iframe width="1000" height="520" src="{maps_url}" frameborder="0" style="border:0" allowfullscreen></iframe>',unsafe_allow_html=True)
                st.session_state.index = i + 1  # Update the stored index after each iteration
                break
            #st.write(f'There is not enough time to reach the target destination')
            #st.write(f'Choosing other destination')
            #st.write('')
        else:
            st.write("Error:", data['status'])

    else:
        st.write('No suitable location found within the remaining time')

if st.button('Get Recommended Location'):
    get_recommended_location()

if st.button('Skip'):
    st.session_state.index += 1  # Increment the index to continue from the next iteration
    get_recommended_location()