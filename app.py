import streamlit as st

st.title('Smart Home Prediction')

st.image("home.jpg", use_column_width=True)

st.number_input("Enter the area", 0)
st.number_input("Number of bedrooms", 0)
st.number_input("Number of bathrooms", 0)
st.number_input("Number of stories", 0)
st.number_input("Number of parking spaces", 0)
st.selectbox("Close to the main road", ["Yes","No"])
st.selectbox("Has a guest room", ["Yes","No"])
st.selectbox("Has a basement", ["Yes","No"])
st.selectbox("Has hotwater heating", ["Yes","No"])
st.selectbox("Has prefarea", ["Yes","No"])
st.radio("Furnishing status", ["Unfurnished", "Semi-furnished", "Furnished"])
submit_button = st.form_submit_button("Predict")
if submit_button:
  print("The button has been clicked")






