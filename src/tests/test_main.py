# /c/Users/관리자/Desktop/projects/todos/src/tests/test_main.py 내용

# GET Method 사용하여 "/" 검증
def test_health_check(client):      # client 는 내가 conftest.py에서 정의한 fixture
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}