import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://api:8000") as ac:
        yield ac
