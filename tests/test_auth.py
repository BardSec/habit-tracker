def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Sign In" in response.data or b"sign in" in response.data.lower()


def test_dev_login(client, app):
    response = client.post(
        "/auth/login",
        data={"email": "dev@example.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_redirect_when_not_logged_in(client):
    response = client.get("/")
    assert response.status_code == 302
