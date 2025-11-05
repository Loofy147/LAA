
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    """Tests that the /health endpoint returns a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_ski_rental_decide():
    """Smoke test for the /ski-rental/decide endpoint."""
    response = client.post(
        "/algorithms/ski-rental/decide",
        json={
            "buy_cost": 100.0,
            "current_day": 10,
            "prediction_days": 120.0,
            "trust": 0.8,
        },
    )
    assert response.status_code == 200
    assert "decision" in response.json()

def test_caching_decide():
    """Smoke test for the /caching/decide endpoint."""
    response = client.post(
        "/algorithms/caching/decide",
        json={
            "cache_size": 2,
            "predictions": {"1": 10, "2": 5},
            "item": 1,
            "cache": [1, 2],
        },
    )
    assert response.status_code == 200
    assert "decision" in response.json()

def test_oneway_trading_decide():
    """Smoke test for the /oneway-trading/decide endpoint."""
    response = client.post(
        "/algorithms/oneway-trading/decide",
        json={
            "buy_price": 100.0,
            "current_price": 110.0,
            "prediction_price": 120.0,
            "trust": 0.5,
        },
    )
    assert response.status_code == 200
    assert "decision" in response.json()

def test_scheduling_decide():
    """Smoke test for the /scheduling/decide endpoint."""
    response = client.post(
        "/algorithms/scheduling/decide",
        json={
            "num_machines": 2,
            "job_lengths": [10, 5, 12],
            "prediction_job_lengths": [5, 10, 12],
        },
    )
    assert response.status_code == 200
    assert "assignments" in response.json()

def test_search_decide():
    """Smoke test for the /search/decide endpoint."""
    response = client.post(
        "/algorithms/search/decide",
        json={
            "max_value": 100,
            "values": [10, 50, 20, 90],
            "prediction_value": 3,
        },
    )
    assert response.status_code == 200
    assert "best_index" in response.json()
