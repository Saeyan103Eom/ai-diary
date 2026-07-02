def test_user_signup(client):
    response=client.post("/user/signup")
    assert response.status_code == 200
    assert response.json() is True