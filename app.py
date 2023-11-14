import streamlit as st

st.title('Smart Home Prediction')

st.image("home.jpg", use_column_width=True)

feature = {}
features["area"] = st.number_input("Enter the area", 0)
features["bedrooms"] = st.number_input("Number of bedrooms", 0)
features["bathrooms"] = st.number_input("Number of bathrooms", 0)
features["stories"] = st.number_input("Number of stories", 0)
features["parking"] = st.number_input("Number of parking spaces", 0)
features["mainroad"] = st.selectbox("Close to the main road", ["Yes","No"])
features["guestroom"] = st.selectbox("Has a guest room", ["Yes","No"])
features["basement"] = st.selectbox("Has a basement", ["Yes","No"])
features["hotwaterheatinh"] = st.selectbox("Has hotwater heating", ["Yes","No"])
features["prefarea"] = st.selectbox("Has prefarea", ["Yes","No"])
features["furnishingstatus"] = st.radio("Furnishing status", ["Unfurnished", "Semi-furnished", "Furnished"])

st.button("Predict", type="primary")
if st.button("Hi"):
    st.write('Button clicked')
else:
    st.write('Goodbye')


import streamlit as st

# Create a form to collect the input features
features = {}
features["price"] = st.number_input("Price")
features["area"] = st.number_input("Area")
features["bedrooms"] = st.number_input("Bedrooms")
features["bathrooms"] = st.number_input("Bathrooms")
features["stories"] = st.number_input("Stories")
features["mainroad"] = st.selectbox("Main Road", ["Yes", "No"])
features["guestroom"] = st.selectbox("Guest Room", ["Yes", "No"])
features["basement"] = st.selectbox("Basement", ["Yes", "No"])
features["hotwaterheating"] = st.selectbox("Hot Water Heating", ["Yes", "No"])
features["airconditioning"] = st.selectbox("Air Conditioning", ["Yes", "No"])
features["parking"] = st.number_input("Parking")
features["prefarea"] = st.text_input("Preferred Area")
features["furnishingstatus"] = st.selectbox("Furnishing Status", ["Furnished", "Unfurnished"])

# Return the input features
return features



