import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def setup_app():
    yield FastAPI()


@pytest.fixture
def setup_client(setup_app: FastAPI):
    yield TestClient(setup_app)
