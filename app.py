#Import all dependencies which are libraries in this case
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
#import pickle
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

features = {}
features["area"] = st.number_input("Enter the area", 0)
features["bedrooms"] = st.number_input("Number of bedrooms", 0)
features["bathrooms"] = st.number_input("Number of bathrooms", 0)
features["stories"] = st.number_input("Number of stories", 0)
features["parking"] = st.number_input("Number of parking spaces", 0)


# Convert 'yes' or 'no' input to 1 for yes and 0 for no
features["mainroad"] = 1 if st.checkbox("Close to the main road") else 0
features["guestroom"] = 1 if st.checkbox("Has a guest room") else 0
features["basement"] = 1 if st.checkbox("Has a basement") else 0
features["airconditioning"] = 1 if st.checkbox("Has airconditioning") else 0
features["hotwaterheating"] = 1 if st.checkbox("Has hot water heating") else 0
features["prefarea"] = 1 if st.checkbox("Has prefarea") else 0

# Create a selectbox for the main road feature with options "Yes" and "No"
#main_road_selectbox = st.selectbox("Close to the main road", ["Yes", "No"])

# Convert the selectbox value to 1 or 0
#if main_road_selectbox == "Yes":
#    features["mainroad"] = 1
#else:
#    features["mainroad"] = 0

# Convert 'unfurnished', 'semi-furnished', and 'furnished' to 0, 1, and 2 respectively
furnishing_status_mapping = {"Unfurnished": 0, "Semi-furnished": 1, "Furnished": 2}
features["furnishingstatus"] = furnishing_status_mapping[st.radio("Furnishing status", ["Unfurnished", "Semi-furnished", "Furnished"])]

# Define a function to predict the house price
def predict_house_price(features):
    prediction = model.predict([features])
    return prediction[0]
    
# Convert the input features to a 2D array
features_2d = np.array([list(features.values())])

# Predict the house price when the user clicks the submit button
if st.button("Predict House Price", type = "primary"):
    prediction = model.predict(features_2d)
    st.write("Predicted house price:", prediction[0])

