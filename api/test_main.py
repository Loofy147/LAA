
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    """Tests that the /health endpoint returns a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

# Tests for SkiRental
def test_ski_rental_decide_buy():
    response = client.post("/algorithms/ski-rental/decide", json={"buy_cost": 10, "current_day": 10, "prediction_days": 10, "trust": 1.0})
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "buy"
    assert data["algorithm"] == "ski_rental"

def test_ski_rental_decide_rent():
    response = client.post("/algorithms/ski-rental/decide", json={"buy_cost": 10, "current_day": 9, "prediction_days": 10, "trust": 1.0})
    assert response.status_code == 200
    assert response.json()["decision"] == "rent"

def test_ski_rental_invalid_trust():
    response = client.post("/algorithms/ski-rental/decide", json={"buy_cost": 10, "current_day": 10, "prediction_days": 10, "trust": 1.1})
    assert response.status_code == 422 # Unprocessable Entity

# Tests for RandomizedSkiRental
def test_randomized_ski_rental_decide():
    response = client.post("/algorithms/randomized-ski-rental/decide", json={"buy_cost": 10, "current_day": 10, "prediction_days": 10, "trust": 1.0})
    assert response.status_code == 200
    assert "decision" in response.json()
    assert response.json()["algorithm"] == "randomized_ski_rental"

def test_randomized_ski_rental_invalid_trust():
    response = client.post("/algorithms/randomized-ski-rental/decide", json={"buy_cost": 10, "current_day": 10, "prediction_days": 10, "trust": -0.1})
    assert response.status_code == 422

# Tests for Caching
def test_caching_decide_hit():
    response = client.post("/algorithms/caching/decide", json={"cache_size": 3, "predictions": {}, "item": 1, "cache": [1, 2, 3]})
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "hit"
    assert data["new_cache"] == [1, 2, 3]

def test_caching_decide_miss_and_evict():
    response = client.post("/algorithms/caching/decide", json={"cache_size": 2, "predictions": {"1": 10, "2": 5}, "item": 3, "cache": [1, 2]})
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "miss"
    assert data["new_cache"] == [2, 3] # Item 1 should be evicted

def test_caching_invalid_cache_size():
    response = client.post("/algorithms/caching/decide", json={"cache_size": -1, "predictions": {}, "item": 1, "cache": []})
    assert response.status_code == 422

# Tests for OnewayTrading
def test_oneway_trading_decide_buy():
    response = client.post("/algorithms/oneway-trading/decide", json={"buy_price": 100, "current_price": 110, "prediction_price": 110, "trust": 1.0})
    assert response.status_code == 200
    assert response.json()["decision"] == "buy"

def test_oneway_trading_decide_wait():
    response = client.post("/algorithms/oneway-trading/decide", json={"buy_price": 100, "current_price": 109, "prediction_price": 110, "trust": 1.0})
    assert response.status_code == 200
    assert response.json()["decision"] == "wait"

def test_oneway_trading_invalid_price():
    response = client.post("/algorithms/oneway-trading/decide", json={"buy_price": -100, "current_price": 110, "prediction_price": 110, "trust": 1.0})
    assert response.status_code == 422

# Tests for Scheduling
def test_scheduling_decide():
    response = client.post("/algorithms/scheduling/decide", json={"num_machines": 2, "job_lengths": [10, 10], "prediction_job_lengths": [1, 1]})
    assert response.status_code == 200
    assert response.json()["assignments"] == [0, 1]

def test_scheduling_invalid_num_machines():
    response = client.post("/algorithms/scheduling/decide", json={"num_machines": 0, "job_lengths": [10, 10], "prediction_job_lengths": [1, 1]})
    assert response.status_code == 422

# Tests for Search
def test_search_decide():
    response = client.post("/algorithms/search/decide", json={"max_value": 100, "values": [10, 99, 50], "prediction_value": 1})
    assert response.status_code == 200
    assert response.json()["best_index"] == 1
