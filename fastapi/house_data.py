import os
from pydantic import BaseModel


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
    central_Vacuume_cleaner: int = int(
        os.getenv("DEFAULT_CENTRAL_VACUUME_CLEANER", False))
    janitor: int = int(os.getenv("DEFAULT_JANITOR", False))
    Guard: int = int(os.getenv("DEFAULT_GUARD", False))
    master_room: int = int(os.getenv("DEFAULT_MASTER_ROOM", False))
    conference_hall: int = int(os.getenv("DEFAULT_CONFERENCE_HALL", False))
