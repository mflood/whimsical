from fastapi import FastAPI
from model_server.models import UserIn, AddressIn, GeoOut


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/geocode", response_model=GeoOut)
async def geocode(address_in: AddressIn):
    resp = GeoOut(latitude=10.1, 
    longitude=13)
    return resp
