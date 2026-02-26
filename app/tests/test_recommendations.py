from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_recs_unauth():
    # No token provided — should 401
    r = client.get("/recommendations/people-you-may-know")
    assert r.status_code in (401, 422)  # depending on HTTPBearer errors
