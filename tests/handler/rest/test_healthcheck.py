from async_asgi_testclient import TestClient  # type: ignore[import]

from app.main import app


async def test_healtcheck():
    async with TestClient(app) as cli:
        res = await cli.get("/health")

        assert res.status_code == 200
        assert res.json() == {"message": "Ok"}
