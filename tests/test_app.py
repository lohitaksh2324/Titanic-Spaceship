"""
Automated Test Suite for Spaceship Titanic Prediction Service
CSL236 End-Term Project — Stage 5 Testing Requirements (Min. 4 Tests)
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_1_health_check():
    """Test 1: Health check endpoint returns 200 and indicates model is loaded."""
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "timestamp" in data


def test_2_ui_loads():
    """Test 2: Web UI root endpoint returns 200 and serves HTML content."""
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "text/html" in response.headers.get("content-type", "")
    assert "SPACESHIP TITANIC" in response.text
    assert "Passenger Manifest" in response.text


def test_3_domain_logic_cryosleep_vs_awake():
    """
    Test 3: Domain-Logic Test.
    A passenger in CryoSleep who spent $0 across all amenities should have
    a significantly higher probability of being Transported than an awake
    passenger who spent heavily on luxury amenities in a central cabin.
    """
    # Strong candidate for Transported: CryoSleep, Deck B, 0 spend
    strong_passenger = {
        "PassengerId": "1001_01",
        "HomePlanet": "Europa",
        "CryoSleep": True,
        "Cabin": "B/10/S",
        "Destination": "55 Cancri e",
        "Age": 29.0,
        "VIP": False,
        "RoomService": 0.0,
        "FoodCourt": 0.0,
        "ShoppingMall": 0.0,
        "Spa": 0.0,
        "VRDeck": 0.0,
    }

    # Weak candidate for Transported: Awake, Deck E, heavy luxury spend
    weak_passenger = {
        "PassengerId": "1002_01",
        "HomePlanet": "Earth",
        "CryoSleep": False,
        "Cabin": "E/50/P",
        "Destination": "TRAPPIST-1e",
        "Age": 35.0,
        "VIP": False,
        "RoomService": 1500.0,
        "FoodCourt": 800.0,
        "ShoppingMall": 600.0,
        "Spa": 2000.0,
        "VRDeck": 1800.0,
    }

    resp_strong = client.post("/predict", json=strong_passenger)
    resp_weak = client.post("/predict", json=weak_passenger)

    assert resp_strong.status_code == 200, resp_strong.text
    assert resp_weak.status_code == 200, resp_weak.text

    prob_strong = resp_strong.json()["probability"]
    prob_weak = resp_weak.json()["probability"]

    # The CryoSleep candidate must beat the awake heavy spender
    assert prob_strong > prob_weak, (
        f"Domain logic failed: Strong candidate prob ({prob_strong}) "
        f"must be greater than weak candidate prob ({prob_weak})"
    )
    # Strong candidate should be predicted True (Transported)
    assert resp_strong.json()["transported"] is True


def test_4_boundary_validation_expects_422():
    """
    Test 4: Boundary Test that expects HTTP 422.
    Passing invalid types or out-of-range values (e.g. negative age,
    negative room service, or invalid planet name) must return HTTP 422,
    NOT an internal server error (500).
    """
    # Case A: Negative age (< 0.0 violates ge=0.0)
    bad_payload_age = {
        "PassengerId": "2001_01",
        "HomePlanet": "Earth",
        "CryoSleep": False,
        "Cabin": "F/10/S",
        "Destination": "TRAPPIST-1e",
        "Age": -5.0,  # INVALID: must be >= 0
        "VIP": False,
        "RoomService": 0.0,
        "FoodCourt": 0.0,
        "ShoppingMall": 0.0,
        "Spa": 0.0,
        "VRDeck": 0.0,
    }
    resp_age = client.post("/predict", json=bad_payload_age)
    assert resp_age.status_code == 422, f"Expected 422 for negative age, got {resp_age.status_code}"

    # Case B: Invalid HomePlanet (not Earth, Europa, or Mars)
    bad_payload_planet = {
        "PassengerId": "2002_01",
        "HomePlanet": "Jupiter",  # INVALID planet
        "CryoSleep": False,
        "Cabin": "F/10/S",
        "Destination": "TRAPPIST-1e",
        "Age": 25.0,
        "VIP": False,
        "RoomService": 0.0,
        "FoodCourt": 0.0,
        "ShoppingMall": 0.0,
        "Spa": 0.0,
        "VRDeck": 0.0,
    }
    resp_planet = client.post("/predict", json=bad_payload_planet)
    assert resp_planet.status_code == 422, f"Expected 422 for invalid planet, got {resp_planet.status_code}"

    # Case C: Negative amenity spend (< 0 violates ge=0.0)
    bad_payload_spend = {
        "PassengerId": "2003_01",
        "HomePlanet": "Earth",
        "CryoSleep": False,
        "Cabin": "F/10/S",
        "Destination": "TRAPPIST-1e",
        "Age": 25.0,
        "VIP": False,
        "RoomService": -250.0,  # INVALID: must be >= 0
        "FoodCourt": 0.0,
        "ShoppingMall": 0.0,
        "Spa": 0.0,
        "VRDeck": 0.0,
    }
    resp_spend = client.post("/predict", json=bad_payload_spend)
    assert resp_spend.status_code == 422, f"Expected 422 for negative spend, got {resp_spend.status_code}"
