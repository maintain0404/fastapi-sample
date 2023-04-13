from async_asgi_testclient import TestClient  # type: ignore[import]

from main import app


async def test_healtcheck():
    async with TestClient(app) as cli:
        res = await cli.get("/api/health")

        assert res.status_code == 200
        assert res.json() == {"message": "Ok"}
