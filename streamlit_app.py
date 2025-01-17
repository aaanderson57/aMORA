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

st.title("Sao Paulo Housing Prices Prediction")

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
