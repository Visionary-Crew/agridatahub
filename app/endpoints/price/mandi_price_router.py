from fastapi import APIRouter, HTTPException
from app.services import MandiPriceService

mandi_price_router = APIRouter()


@mandi_price_router.get("/get_mandi_price/", tags=["mandi"])
async def get_mandi_price():
    try:
        await MandiPriceService.import_crops_from_csv()
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=500, detail=str(ex))
