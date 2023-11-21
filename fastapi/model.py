# model.py

import numpy as np 
import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

class ModelXGB:
    def __init__(self, file_path="Data\data_final.csv"):
        self.df = pd.read_csv(file_path)
        self.X = self.df.drop(["price_per_meter", "district_name", "price"], axis=1)
        self.y = self.df["price_per_meter"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

        # Define numerical and categorical features
        numerical_features = ["latitude", "real_estate_area", "real_estate_age", "total_rooms", "longitude", "total_rooms", "floor"]
        categorical_features = []  # Add your categorical features here

        # Create pipelines for numerical and categorical features
        num_pipeline = Pipeline([("standardize", StandardScaler())])
        cat_pipeline = make_pipeline(
            SimpleImputer(strategy="most_frequent"),
            OneHotEncoder(handle_unknown="ignore")
        )

        # Create ColumnTransformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", num_pipeline, numerical_features),
                ("cat", cat_pipeline, categorical_features),
            ]
        )

        # Create XGBoost model
        self.xgb = Pipeline([
            ('xgboost', XGBRegressor(subsample=0.7, max_depth=9, eta=0.04, colsample_bytree=0.8))
        ])

    def train(self):
        self.preprocessor.fit(self.X_train)

        # Transform the training data
        X_train_transformed = self.preprocessor.transform(self.X_train)

        # Fit the XGBoost model on the transformed training data
        self.xgb.fit(X_train_transformed, self.y_train)

    def evaluate(self):
        mse = mean_squared_error(self.y_test, self.xgb.predict(self.X_test), squared=False)
        mae = mean_absolute_error(self.y_test, self.xgb.predict(self.X_test))
        r2 = r2_score(self.y_test, self.xgb.predict(self.X_test))
        return mse, mae, r2
