import pytest
from fastapi.testclient import TestClient


class TestAuthRegister:
    def test_register_success(self, client: TestClient):
        response = client.post("/auth/", json={"username": "newuser", "password": "password123"})
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data

    def test_register_duplicate_username(self, client: TestClient, test_user):
        response = client.post("/auth/", json={"username": "testuser", "password": "password123"})
        assert response.status_code == 409
        assert response.json()["detail"] == "Username already exists"

    def test_register_missing_fields(self, client: TestClient):
        response = client.post("/auth/", json={"username": "onlyuser"})
        assert response.status_code == 422


class TestAuthLogin:
    def test_login_success(self, client: TestClient, test_user):
        response = client.post("/auth/token", data={"username": "testuser", "password": "test"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user):
        response = client.post("/auth/token", data={"username": "testuser", "password": "wrong"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

    def test_login_nonexistent_user(self, client: TestClient):
        response = client.post("/auth/token", data={"username": "ghost", "password": "pass"})
        assert response.status_code == 401

    def test_login_missing_fields(self, client: TestClient):
        response = client.post("/auth/token", data={"username": "onlyuser"})
        assert response.status_code == 422


class TestAuthMe:
    def test_me_with_valid_token(self, client: TestClient, test_user):
        login_resp = client.post("/auth/token", data={"username": "testuser", "password": "test"})
        token = login_resp.json()["access_token"]

        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["id"] == test_user.id

    def test_me_without_token(self, client: TestClient):
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_me_with_invalid_token(self, client: TestClient):
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert response.status_code == 401