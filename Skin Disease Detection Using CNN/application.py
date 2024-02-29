import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import hydralit_components as hc
import time
from prediction import predictor
url="""
<style>
[data-testid="stAppViewContainer"]{
background-color: #f39f86;
background-image: linear-gradient(315deg, #f39f86 0%, #f9d976 74%);
font-style:italic;
}
[data-testid="stHeader"]{
background-color:black;
color:white;
}
</style>
"""
st.markdown(url,unsafe_allow_html=True)
st.title("SKIN DISEASE DETECTION USING CONVOLUTIONAL NEURAL NETWORK")
st.header("A system to detect 10 different classes of diseases")
st.text("Upload a skin image to detect the disease")
uploaded_file = st.file_uploader("Choose a skin image", type="jpg")
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption='', use_column_width=True)
  st.write("")
  with hc.HyLoader('',hc.Loaders.pulse_bars,):
    time.sleep(10) 
  label,probability = predictor(image)
  if label == "":
    st.write("Disease could not be detected!")
  else:
    st.write("Class: ",label)
    st.write("Probability:  ",(probability * 100),"%")