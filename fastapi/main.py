import os
import sys
sys.path.append('/home/fatemeh/Documents/HousePriceEstimationProject')


from models.preprocessing import Preprocessing
from models.xgboost import XGBoostModel
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from house_data import HouseData


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

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

########
df_train, df_test = train_test_split(
    df_filter, test_size=0.2, stratify=df_filter['district_name'], random_state=42)


X_train = df_train.drop(['price_per_meter', 'district_name'], axis=1)
y_train = df_train['price_per_meter']


X_test = df_test.drop(["price_per_meter", 'district_name'], axis=1)
y_test = df_test["price_per_meter"].copy()
preprocessor = Preprocessing()
model = XGBoostModel(preprocessor.preprocess_data(df_train))


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(data: HouseData, request: Request):
    model.train(X_train, y_train)

    input_data = pd.DataFrame([data.model_dump()])

    price_estimate = model.predict(input_data)[0]
    return {"message": f"The estimated price is {price_estimate.round()}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
