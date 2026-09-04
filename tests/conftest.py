import pytest
from fastapi.testclient import TestClient
from netfaultlab.main import app

@pytest.fixture
def client():
    return TestClient(app)
