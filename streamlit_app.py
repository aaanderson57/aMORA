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

st.title("California Housing Prices Prediction")

# layout and input data
col1, col2 = st.columns([1, 2], gap='large')
with col1:
    st.header("Enter the attributes of the housing.")
