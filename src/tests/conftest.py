import os

import pytest
from fastapi.testclient import TestClient

from core.cloud_service import CloudEnvironmentService
from main import app

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
def upload_cloud_env():
    CloudEnvironmentService.load(os.path.join(FIXTURES_DIR, "cloud.json"))
