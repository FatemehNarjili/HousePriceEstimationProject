import sys
sys.path.append('/home/fatemeh/Documents/HousePriceEstimationProject')


import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

from models.preprocessing import Preprocessing
from models.catboost import CatBoostModel
from models.knn import KNNModel
from models.light_gbm import LightGBMModel
from models.linear_regression import LinearRegressionModel
from models.random_forest import RandomForestModel
from models.xgboost import XGBoostModel


df = pd.read_csv('../data/final_map.csv')


df = df.drop(columns=['price'], axis='columns')


over_60 = pd.DataFrame((df['district_name'].value_counts() > 60))
column_district_name = over_60[over_60['count']].index
df_filter = df[df['district_name'].isin(column_district_name)].copy()


columns_int64 = df_filter.select_dtypes('int64').columns
for item in columns_int64:
    df_filter[item] = df_filter[item].astype('int8')


integer_columns = df_filter.select_dtypes(include=['int8']).columns
float_columns = df_filter.select_dtypes(include=['float64']).columns


float_64_columns = ['total_rooms', 'floor',
                    'real_estate_age', 'real_estate_area']
for item_64 in float_64_columns:
    df_filter[item_64] = df_filter[item_64].astype('int16')


df_train, df_test = train_test_split(
    df_filter, test_size=0.2, stratify=df_filter['district_name'], random_state=42)


X_train = df_train.drop(['price_per_meter', 'district_name'], axis=1)
y_train = df_train['price_per_meter']


X_test = df_test.drop(["price_per_meter", 'district_name'], axis=1)
y_test = df_test["price_per_meter"].copy()

preprocessor = Preprocessing()

# Linear Regression Model
lr = LinearRegressionModel(preprocessor.preprocess_data(df_train))
lr.train(X_train, y_train)
lr.evaluate(X_test, y_test)

pickle_out = open("pickle_files/linear_regression.pkl", "wb")
pickle.dump(lr.model, pickle_out)
pickle_out.close()

# KNN Model
knn = KNNModel(preprocessor.preprocess_data(df_train))
knn.train(X_train, y_train)
knn.evaluate(X_test, y_test)

pickle_out = open("pickle_files/knn.pkl", "wb")
pickle.dump(knn.model, pickle_out)
pickle_out.close()


# Random Forest Model
rf = RandomForestModel(preprocessor.preprocess_data(df_train))
rf.train(X_train, y_train)
rf.evaluate(X_test, y_test)

pickle_out = open("pickle_files/random_forest.pkl", "wb")
pickle.dump(rf.model, pickle_out)
pickle_out.close()


# Cat Boost Model 
catboost = CatBoostModel(preprocessor.preprocess_data(df_train))
catboost.train(X_train, y_train)
catboost.evaluate(X_test, y_test)

pickle_out = open("pickle_files/catboost.pkl", "wb")
pickle.dump(catboost.model, pickle_out)
pickle_out.close()

# LightGBM Model
lgbm = LightGBMModel(preprocessor.preprocess_data(df_train))
lgbm.train(X_train, y_train)
lgbm.evaluate(X_test, y_test)

pickle_out = open("pickle_files/lightgbm.pkl", "wb")
pickle.dump(lgbm.model, pickle_out)
pickle_out.close()


# XGBoost Model
xgb = XGBoostModel(preprocessor.preprocess_data(df_train))
xgb.train(X_train, y_train)
xgb.evaluate(X_test, y_test)

pickle_out = open("pickle_files/xgboost.pkl", "wb")
pickle.dump(xgb.model, pickle_out)
pickle_out.close()