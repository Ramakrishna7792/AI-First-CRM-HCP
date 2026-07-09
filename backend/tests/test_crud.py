from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import app


engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)


def override_db():
    with TestingSession() as session:
        yield session


def setup_module():
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_db


def teardown_module():
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_authenticated_crud_flow():
    client = TestClient(app)
    registered = client.post("/api/v1/auth/register", json={
        "email": "crud@example.com", "full_name": "CRUD Tester", "password": "StrongPass123!",
    })
    assert registered.status_code == 201
    login = client.post("/api/v1/auth/login", json={
        "email": "crud@example.com", "password": "StrongPass123!",
    })
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    doctor = client.post("/api/v1/doctors", headers=headers, json={
        "name": "Dr. API Test", "specialization": "Cardiology", "city": "Pune",
    })
    assert doctor.status_code == 201
    doctor_id = doctor.json()["id"]
    assert client.patch(f"/api/v1/doctors/{doctor_id}", headers=headers, json={
        "hospital": "Test Hospital",
    }).json()["hospital"] == "Test Hospital"

    product = client.post("/api/v1/products", headers=headers, json={
        "product_name": "API Product", "category": "Cardiology", "description": "Test",
    })
    assert product.status_code == 201
    product_id = product.json()["id"]

    interaction = client.post("/api/v1/interactions", headers=headers, json={
        "doctor_id": doctor_id, "date": "2026-07-09", "interaction_type": "In-Person",
        "sentiment": "Positive", "summary": "Successful API test interaction.",
        "product_ids": [product_id],
    })
    assert interaction.status_code == 201, interaction.text
    interaction_id = interaction.json()["id"]
    assert interaction.json()["products"][0]["id"] == product_id
    assert client.patch(f"/api/v1/interactions/{interaction_id}", headers=headers, json={
        "followup": "Return in two weeks",
    }).json()["followup"] == "Return in two weeks"
    assert client.get("/api/v1/interactions", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/interactions/{interaction_id}", headers=headers).status_code == 204
    assert client.delete(f"/api/v1/products/{product_id}", headers=headers).status_code == 204
    assert client.delete(f"/api/v1/doctors/{doctor_id}", headers=headers).status_code == 204
