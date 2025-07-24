# Import necessary libraries

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, FunctionTransformer
from sklearn.metrics import mean_squared_error
import joblib

# Load data
df = pd.read_csv("housing.csv")

# Define features and target
features = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
            'parking', 'prefarea', 'furnishingstatus']
target = 'price'

X = df[features]
y = df[target]

# Columns for preprocessing
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
               'airconditioning', 'prefarea']

ordinal_col = ['furnishingstatus']
ordinal_categories = [['unfurnished', 'semi-furnished', 'furnished']]

numeric_cols = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']

# Define preprocessing steps
preprocessor = ColumnTransformer(transformers=[
    ('bin', FunctionTransformer(lambda x: x.replace({'yes': 1, 'no': 0})), binary_cols),
    ('ord', OrdinalEncoder(categories=ordinal_categories), ordinal_col),
    ('num', StandardScaler(), numeric_cols)
])

# Define full pipeline with model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
mse = mean_squared_error(y_test, preds)
print(f"Mean Squared Error: {mse:.2f}")

# Save entire pipeline
joblib.dump(pipeline, 'house_price_pipeline.joblib')
