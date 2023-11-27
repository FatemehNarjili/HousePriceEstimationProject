import sys
sys.path.append('/home/fatemeh/Documents/HousePriceEstimationProject')


import pickle
import uvicorn
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from house_data import HouseData


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

pickle_in = open("xgboost.pkl", "rb")
model = pickle.load(pickle_in)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(data: HouseData, request: Request):
    input_data = pd.DataFrame([data.model_dump()])

    price_estimate = model.predict(input_data)[0]
    return {"message": f"The estimated price is {price_estimate.round()}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
