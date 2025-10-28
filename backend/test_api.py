import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Training App API",
        "version": "1.0.0",
    }


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register", json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data or data.get("password") != "testpass123"


def test_register_duplicate_user():
    """Test registering duplicate username fails"""
    # First registration
    client.post("/auth/register", json={"username": "duplicate", "password": "pass123"})

    # Try to register again with same username
    response = client.post(
        "/auth/register", json={"username": "duplicate", "password": "pass456"}
    )
    assert response.status_code == 400


def test_login_user():
    """Test user login"""
    # Register user first
    client.post(
        "/auth/register", json={"username": "logintest", "password": "password123"}
    )

    # Login
    response = client.post(
        "/auth/login", json={"username": "logintest", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    """Test login with wrong password fails"""
    # Register user first
    client.post(
        "/auth/register", json={"username": "wrongpass", "password": "correct123"}
    )

    # Try login with wrong password
    response = client.post(
        "/auth/login", json={"username": "wrongpass", "password": "wrong123"}
    )
    assert response.status_code == 401


def test_create_plan_requires_auth():
    """Test creating a plan requires authentication"""
    response = client.post(
        "/plans/",
        json={"name": "Test Plan", "startDate": "2024-01-01T00:00:00", "public": False},
    )
    assert response.status_code == 403  # Forbidden without auth


def test_create_plan_with_auth():
    """Test creating a plan with authentication"""
    # Register and login
    client.post("/auth/register", json={"username": "planuser", "password": "pass123"})
    login_response = client.post(
        "/auth/login", json={"username": "planuser", "password": "pass123"}
    )
    token = login_response.json()["access_token"]

    # Create plan
    response = client.post(
        "/plans/",
        json={
            "name": "My Training Plan",
            "startDate": "2024-01-01T00:00:00",
            "public": False,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Training Plan"
    assert "id" in data


def test_get_plans_with_auth():
    """Test getting plans requires authentication"""
    # Register and login
    client.post("/auth/register", json={"username": "getplans", "password": "pass123"})
    login_response = client.post(
        "/auth/login", json={"username": "getplans", "password": "pass123"}
    )
    token = login_response.json()["access_token"]

    # Get plans
    response = client.get("/plans/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_exercise_with_auth():
    """Test creating an exercise with authentication"""
    # Register and login
    client.post(
        "/auth/register", json={"username": "exerciseuser", "password": "pass123"}
    )
    login_response = client.post(
        "/auth/login", json={"username": "exerciseuser", "password": "pass123"}
    )
    token = login_response.json()["access_token"]

    # Create exercise
    response = client.post(
        "/exercises/",
        json={"name": "Bench Press", "description": "Chest exercise", "public": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bench Press"
    assert data["description"] == "Chest exercise"
    assert data["public"] is True


def test_api_documentation():
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Training App API"
