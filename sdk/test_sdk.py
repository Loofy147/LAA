
import pytest
import requests
from unittest.mock import MagicMock
from laa_sdk import LAAClient, DecisionResponse, CachingResponse, SchedulingResponse, SearchResponse, APIError, ClientValidationError

@pytest.fixture
def client(mocker):
    """
    Provides a LAAClient instance with a mocked requests.Session.
    """
    mock_session = MagicMock()
    mocker.patch('requests.Session', return_value=mock_session)
    return LAAClient(api_url="http://test.com", api_key="test_key"), mock_session

def test_ski_rental_decide_success(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.json.return_value = {"decision": "buy", "algorithm": "ski_rental", "trust_parameter": 0.8}
    mock_session.request.return_value = mock_response

    result = laa_client.ski_rental_decide(100, 10, 120, 0.8)

    assert isinstance(result, DecisionResponse)
    assert result.decision == "buy"
    mock_session.request.assert_called_once_with(
        "POST",
        "http://test.com/algorithms/ski-rental/decide",
        json={"buy_cost": 100, "current_day": 10, "prediction_days": 120, "trust": 0.8}
    )

def test_randomized_ski_rental_decide_success(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.json.return_value = {"decision": "rent", "algorithm": "randomized_ski_rental", "trust_parameter": 0.5}
    mock_session.request.return_value = mock_response

    result = laa_client.randomized_ski_rental_decide(100, 5, 20, 0.5)

    assert isinstance(result, DecisionResponse)
    assert result.decision == "rent"

def test_caching_decide_success(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.json.return_value = {"decision": "miss", "new_cache": [2, 3], "algorithm": "caching"}
    mock_session.request.return_value = mock_response

    result = laa_client.caching_decide(2, {1: 10, 2: 5}, 3, [1, 2])

    assert isinstance(result, CachingResponse)
    assert result.new_cache == [2, 3]

def test_api_error_raised(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=500, text="Internal Server Error"))
    mock_session.request.return_value = mock_response

    with pytest.raises(APIError) as excinfo:
        laa_client.ski_rental_decide(100, 10, 120, 0.8)

    assert excinfo.value.status_code == 500
    assert "Internal Server Error" in str(excinfo.value)

def test_validation_error_raised(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=422, text="Unprocessable Entity"))
    mock_session.request.return_value = mock_response

    with pytest.raises(ClientValidationError):
        laa_client.ski_rental_decide(100, 10, 120, 1.1)

def test_scheduling_decide_success(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.json.return_value = {"assignments": [0, 1], "algorithm": "scheduling"}
    mock_session.request.return_value = mock_response

    result = laa_client.scheduling_decide(2, [10, 10], [1, 1])

    assert isinstance(result, SchedulingResponse)
    assert result.assignments == [0, 1]

def test_search_decide_success(client):
    laa_client, mock_session = client
    mock_response = MagicMock()
    mock_response.json.return_value = {"best_index": 1, "algorithm": "search"}
    mock_session.request.return_value = mock_response

    result = laa_client.search_decide(100, [10, 99, 50], 1)

    assert isinstance(result, SearchResponse)
    assert result.best_index == 1
