#!/usr/bin/env python3
"""
Simple test runner script that doesn't require Docker
Tests the backend API endpoints
"""
import subprocess
import sys
import time
from pathlib import Path

import requests

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"


def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")


def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")


def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")


def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")


def check_backend_running():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def test_health_endpoint():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        print_success("Health check endpoint works")
        return True
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False


def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        print_success("Root endpoint works")
        return True
    except Exception as e:
        print_error(f"Root endpoint failed: {e}")
        return False


def test_register_and_login():
    """Test user registration and login"""
    try:
        # Register
        username = f"testuser_{int(time.time())}"
        register_data = {"username": username, "password": "password123"}
        response = requests.post(
            "http://localhost:8000/auth/register", json=register_data
        )
        assert response.status_code == 201
        print_success(f"User registration works (user: {username})")

        # Login
        login_data = {"username": username, "password": "password123"}
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        token = data["access_token"]
        print_success("User login works")

        return token
    except Exception as e:
        print_error(f"Register/Login failed: {e}")
        return None


def test_create_plan(token):
    """Test creating a plan with authentication"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        plan_data = {
            "name": "Test Plan",
            "startDate": "2024-01-01T00:00:00",
            "public": False,
        }
        response = requests.post(
            "http://localhost:8000/plans/", json=plan_data, headers=headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Plan"
        print_success("Plan creation works")
        return data["id"]
    except Exception as e:
        print_error(f"Plan creation failed: {e}")
        return None


def test_get_plans(token):
    """Test getting plans"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/plans/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print_success(f"Get plans works (found {len(data)} plans)")
        return True
    except Exception as e:
        print_error(f"Get plans failed: {e}")
        return False


def test_create_exercise(token):
    """Test creating an exercise"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        exercise_data = {
            "name": "Bench Press",
            "description": "Chest exercise",
            "public": True,
        }
        response = requests.post(
            "http://localhost:8000/exercises/", json=exercise_data, headers=headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Bench Press"
        print_success("Exercise creation works")
        return data["id"]
    except Exception as e:
        print_error(f"Exercise creation failed: {e}")
        return None


def test_api_docs():
    """Test API documentation endpoints"""
    try:
        # Test Swagger UI
        response = requests.get("http://localhost:8000/docs")
        assert response.status_code == 200

        # Test ReDoc
        response = requests.get("http://localhost:8000/redoc")
        assert response.status_code == 200

        # Test OpenAPI schema
        response = requests.get("http://localhost:8000/openapi.json")
        assert response.status_code == 200

        print_success("API documentation is accessible")
        return True
    except Exception as e:
        print_error(f"API documentation test failed: {e}")
        return False


def main():
    print("\n" + "=" * 50)
    print("  Training App Backend Test Suite")
    print("=" * 50 + "\n")

    # Check if backend is running
    print_info("Checking if backend is running...")
    if not check_backend_running():
        print_error("Backend is not running on http://localhost:8000")
        print_info("Please start the backend first:")
        print("  cd backend")
        print("  python main.py")
        print("\nOr use Docker:")
        print("  docker-compose up -d")
        sys.exit(1)

    print_success("Backend is running\n")

    # Run tests
    results = []

    print_info("Running tests...\n")

    # Basic endpoint tests
    results.append(("Health Check", test_health_endpoint()))
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("API Documentation", test_api_docs()))

    # Authentication tests
    token = test_register_and_login()
    results.append(("Registration & Login", token is not None))

    if token:
        # Authenticated endpoint tests
        plan_id = test_create_plan(token)
        results.append(("Create Plan", plan_id is not None))

        results.append(("Get Plans", test_get_plans(token)))

        exercise_id = test_create_exercise(token)
        results.append(("Create Exercise", exercise_id is not None))
    else:
        print_warning("Skipping authenticated tests due to login failure")

    # Print summary
    print("\n" + "=" * 50)
    print("  Test Results")
    print("=" * 50 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        color = GREEN if result else RED
        print(f"{color}{status:8}{RESET} {test_name}")

    print("\n" + "-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    print("-" * 50 + "\n")

    if passed == total:
        print_success("All tests passed! 🎉\n")
        sys.exit(0)
    else:
        print_error(f"{total - passed} test(s) failed\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
