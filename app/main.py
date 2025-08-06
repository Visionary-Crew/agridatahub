from fastapi import FastAPI
from app.endpoints.price.mandi_price_router import mandi_price_router


app = FastAPI()
app.include_router(mandi_price_router)
