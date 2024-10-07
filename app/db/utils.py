import aiohttp
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from app.configs.secrets import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

async def make_api_call(
    session: aiohttp.ClientSession,
    url: str,
    method: str,
    headers: dict[str, str],
    data: dict = None,
):
    """
    Make an API call using the specified session, URL, method, and data.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The URL to make the API call to.
        method (str): The HTTP method to use for the API call.
        data (dict, optional): The data to send with the API call. Defaults to None.

    Returns:
        dict: The JSON response from the API call.
    """
    async with session.request(method, url, headers=headers, json=data) as response:
        if response.headers.get("Content-Type") == "application/json":
            return await response.json()
        else:
            raise ValueError(
                f"Unexpected Content-Type: {response.headers.get('Content-Type')}"
            )