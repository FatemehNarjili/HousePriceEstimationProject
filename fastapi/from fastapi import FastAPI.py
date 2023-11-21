import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import ModelXGB
import pandas as pd

app = FastAPI()

# Use the ModelXGB class for prediction
model = ModelXGB()

# Define a Pydantic model for the input data
class HouseData(BaseModel):
    district_name: str
    longitude: float = float(os.getenv("DEFAULT_LONGITUDE", 0))
    latitude: float = float(os.getenv("DEFAULT_LATITUDE", 0))
    real_estate_area: float = float(os.getenv("DEFAULT_REAL_ESTATE_AREA", 0))
    real_estate_age: int = int(os.getenv("DEFAULT_REAL_ESTATE_AGE", 0))
    total_rooms: int = int(os.getenv("DEFAULT_TOTAL_ROOMS", 0))
    floor: int = int(os.getenv("DEFAULT_FLOOR", 0))
    elevator: int = int(os.getenv("DEFAULT_ELEVATOR", False))
    parking: int = int(os.getenv("DEFAULT_PARKING", False))
    warehouse: int = int(os.getenv("DEFAULT_WAREHOUSE", False))
    balcony: int = int(os.getenv("DEFAULT_BALCONY", False))
    pool: int = int(os.getenv("DEFAULT_POOL", False))
    roof_garden: int = int(os.getenv("DEFAULT_ROOF_GARDEN", False))
    lobby: int = int(os.getenv("DEFAULT_LOBBY", False))
    lobby_man: int = int(os.getenv("DEFAULT_LOBBY_MAN", False))
    sauna: int = int(os.getenv("DEFAULT_SAUNA", False))
    jacuzzi: int = int(os.getenv("DEFAULT_JACUZZI", False))
    gym: int = int(os.getenv("DEFAULT_GYM", False))
    central_Vacuume_cleaner: int = int(os.getenv("DEFAULT_CENTRAL_VACUUME_CLEANER", False))
    janitor: int = int(os.getenv("DEFAULT_JANITOR", False))
    Guard: int = int(os.getenv("DEFAULT_GUARD", False))
    master_room: int = int(os.getenv("DEFAULT_MASTER_ROOM", False))
    conference_hall: int = int(os.getenv("DEFAULT_CONFERENCE_HALL", False))

# Endpoint for predicting house prices
@app.post("/predict")
def predict_price(data: HouseData):
    try:
        # Create a DataFrame from the input data
        input_data = pd.DataFrame([data.dict()])

        # Use the xgb model for prediction
        prediction = model.xgb.predict(input_data)

        # Return the prediction as a JSON response
        return {"prediction": prediction[0]}

    except Exception as e:
        # Handle errors gracefully
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
