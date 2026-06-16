from fastapi.testclient import TestClient
import sys
import uuid
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_login_page():
    response = client.get("/login_page")
    assert response.status_code == 200


def test_signup_page():
    response = client.get("/signup_page")
    assert response.status_code == 200


def test_account_requires_login():
    fresh_client = TestClient(app)

    response = fresh_client.get(
        "/account",
        follow_redirects=False
    )

    assert response.status_code == 303


def test_logout():
    response = client.get(
        "/logout",
        follow_redirects=False
    )

    assert response.status_code == 303


def test_create_user():
    unique = uuid.uuid4().hex

    response = client.post(
        "/api/users",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["username"] == f"user_{unique}"
    assert data["email"] == f"{unique}@test.com"


def test_password_not_returned():
    unique = uuid.uuid4().hex

    response = client.post(
        "/api/users",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "password" not in data


def test_duplicate_username():
    unique = uuid.uuid4().hex

    first_response = client.post(
        "/api/users",
        json={
            "username": f"user_{unique}",
            "email": f"first_{unique}@test.com",
            "password": "password123"
        }
    )

    assert first_response.status_code == 201

    duplicate_response = client.post(
        "/api/users",
        json={
            "username": f"user_{unique}",
            "email": f"second_{unique}@test.com",
            "password": "password123"
        }
    )

    assert duplicate_response.status_code == 400


def test_upload_requires_login():
    fresh_client = TestClient(app)

    response = fresh_client.post(
        "/upload",
        files={
            "file": (
                "test.txt",
                b"hello world"
            )
        }
    )

    assert response.status_code == 401