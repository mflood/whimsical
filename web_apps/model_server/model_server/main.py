from fastapi import FastAPI
from model_server.models import UserIn, AddressIn, GeoOut

from fastapi.security.api_key import APIKey
from model_server.auth import get_api_key

from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer



api_keys = [
    "prettyplease"
]  # This is encrypted in the database


#def api_key_auth(api_key: str = Depends(get_api_key)):
#    if api_key not in api_keys:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Forbidden"
#        )
#

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/token")
async def token():
    return {"token": "prettyplease"}

@app.get("/geocode", response_model=GeoOut)
async def geocode(address_in: AddressIn):
    resp = GeoOut(latitude=10.1, 
    longitude=13)
    return resp

#@app.get("/safe/geocode", response_model=GeoOut, dependencies=[Depends(api_key_auth)])
#async def geocode(address: str, country_code: str): 
#    resp = GeoOut(latitude=10.1, 
#    longitude=13)
#    return resp
#

@app.get("/safe/geocode", response_model=GeoOut, dependencies=[Depends(get_api_key)])
async def geocode(address: str, country_code: str): 
    resp = GeoOut(latitude=10.1, 
    longitude=13)
    return resp





# end
