import httpx


class BaseAPIClient:

    @staticmethod
    async def fetch_csv(url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
