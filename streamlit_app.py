import streamlit as st
st.set_page_config(page_title="Housing Prices Prediction", page_icon=":house:")
import pandas as pd
import numpy as np
#import pickle
#import folium
#from geopy.geocoders import Nominatim
#import geopy.distance
#from streamlit_folium import st_folium
#from utils.combiner import CombinedAttributesAdder

st.title("São Paulo Housing Prices Prediction")

total_rooms = st.number_input(
            "Total Rooms within a block",
            value=2,
            min_value=0,
            max_value=10)

total_bedrooms = st.number_input(
            "Total Bedrooms within a block",
            value=2, 
            min_value=0, 
            max_value=10)

location = st.session_state['location']
input_data = {
            "lon": location.longitude,
            "lat": location.latitude,
            "housing_median_age": housing_median_age,
            "total_rooms": total_rooms,
            "total_bedrooms": total_bedrooms,
            "population": population,
            "households": households,
            "median_income": median_income,
            "ocean_proximity": ocean_proximity
            }
            
input_df = pd.DataFrame([input_data])

prediction = loaded_model.predict(input_df).squeeze()
st.session_state['prediction'] = prediction
st.success("Done!")
