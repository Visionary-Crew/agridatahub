from app.dal.api_clients import MandiPriceClient
from app.helpers import parse_csv


class MandiPriceService:
    @staticmethod
    async def import_crops_from_csv():
        csv_data = await MandiPriceClient.fetch_mandi_price()
        rows = parse_csv(csv_data)
        imported = 0
        for row in rows:
            try:
                print(row)
                imported += 1
            except Exception as e:
                # Log or handle invalid rows
                continue
        return imported
