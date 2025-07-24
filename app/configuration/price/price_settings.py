from pydantic_settings import BaseSettings


class PriceSettings(BaseSettings):
    mandi_price_url: str
    mandi_price_api_key: str

    class Config:
        env_file = ".env"


price_settings = PriceSettings()
