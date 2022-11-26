import pytest
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient

import app.api.routers.route_root as router


@pytest.fixture
def setup(setup_app: FastAPI, setup_client: TestClient):
    router.templates = Jinja2Templates(directory="tests/api/templates/")
    setup_app.include_router(router=router.root_router)
    yield setup_client


def test_if_response_received(setup: TestClient):
    response = setup.get("/")
    assert response.status_code == 200


def test_if_home_template_returned(setup: TestClient):
    response = setup.get("/")
    assert "test_home" in response.text
