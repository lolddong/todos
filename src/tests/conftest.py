# /c/Users/관리자/Desktop/projects/todos/src/tests/conftest.py 내용
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
	return TestClient(app=app)