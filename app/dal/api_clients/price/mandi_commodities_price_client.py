from app.dal.api_clients.base_api_client import BaseAPIClient
from app.configuration import price_settings


class MandiPriceClient(BaseAPIClient):

    @classmethod
    async def fetch_mandi_price(cls) -> str:
        url = f"{price_settings.mandi_price_url}?api-key={price_settings.mandi_price_api_key}&format=csv&limit=20"
        return await cls.fetch_csv(url)
