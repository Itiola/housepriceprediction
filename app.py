import streamlit as st

st.title('Smart Home Prediction')

st.image("home.jpg", use_column_width=True)

st.number_input("Enter the area", 0)
st.number_input("Number of bedrooms", 0)
st.number_input("Number of bathrooms", 0)
st.number_input("Number of stories", 0)
st.number_input("Number of parking spaces", 0)

