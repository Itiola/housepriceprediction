#Import all dependencies which are libraries in this case
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pickle
import streamlit as st

#Load the data
data = pd.read_csv('housing.csv')

#Convert the csv data into a dataframe
df = pd.DataFrame(data)

#Applying label encoding to the dataframe
columns_to_modify = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
for column in columns_to_modify:
    df[column] = df[column].replace({'yes': 1, 'no': 0, 'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2})


# Select the features and target variable
#Split the data into features (X) and target variable (y), the independent and dependent variables
X = df[['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']]
y = df['price']

#Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

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


# Define a function to predict the house price
def predict_house_price(features):
    prediction = model.predict([features])
    return prediction[0]

# Add a button to predict the house price
if st.button("Predict House Price"):
    prediction = predict_house_price(features)
    st.write("Predicted house price:", prediction)


