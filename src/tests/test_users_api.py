# /c/Users/관리자/Desktop/projects/todos/src/tests/test_users_api.py 내용
def test_user_sign_up(client):
    response = client.post("users/sign-up")
    assert response.status_code == 200
    assert response.json() is True