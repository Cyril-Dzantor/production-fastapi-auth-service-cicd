def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "strongpassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_email(client):
    # First registration
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "strongpassword"}
    )
    # Second registration with the same email
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client):
    # Register the user
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "strongpassword"}
    )
    # Attempt login
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "strongpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail_invalid_password(client):
    client.post(
        "/auth/register",
        json={"email": "fail@example.com", "password": "strongpassword"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "fail@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_refresh_token_success(client):
    client.post("/auth/register", json={"email": "refresh@example.com", "password": "pass"})
    login_resp = client.post("/auth/login", data={"username": "refresh@example.com", "password": "pass"})
    refresh_token = login_resp.json()["refresh_token"]
    
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()

def test_logout_success(client):
    client.post("/auth/register", json={"email": "logout@example.com", "password": "pass"})
    login_resp = client.post("/auth/login", data={"username": "logout@example.com", "password": "pass"})
    access_token = login_resp.json()["access_token"]
    
    resp = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Successfully logged out"

    # Verify blacklisting by trying to logout again with the same token
    resp2 = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert resp2.status_code == 401
