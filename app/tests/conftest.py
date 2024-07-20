import pytest
from fastapi.testclient import TestClient
from api import app


@pytest.fixture(name="client")
def client_fixture():

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()

