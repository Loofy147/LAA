
import requests
from typing import Dict, List
from pydantic import BaseModel, ValidationError

# Response Models
class DecisionResponse(BaseModel):
    decision: str
    algorithm: str
    trust_parameter: float

class CachingResponse(BaseModel):
    decision: str
    new_cache: List[int]
    algorithm: str

class SchedulingResponse(BaseModel):
    assignments: List[int]
    algorithm: str

class SearchResponse(BaseModel):
    best_index: int
    algorithm: str

# Custom Exceptions
class LAAError(Exception):
    """Base exception for the LAA SDK."""
    pass

class APIError(LAAError):
    """Raised for non-2xx API responses."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"API Error {status_code}: {message}")

class ClientValidationError(LAAError):
    """Raised for client-side validation errors."""
    pass

class LAAClient:
    """
    Client SDK for interacting with the LAA Platform API.
    """

    def __init__(self, api_url: str, api_key: str):
        """
        Initializes the LAAClient.

        Args:
            api_url: The base URL of the LAA Platform API.
            api_key: Your API key for authentication.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})

    def _make_request(self, method: str, endpoint: str, json_data: dict, response_model):
        try:
            response = self.session.request(method, f"{self.api_url}{endpoint}", json=json_data)
            response.raise_for_status()
            return response_model(**response.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                raise ClientValidationError(f"Validation Error: {e.response.text}") from e
            raise APIError(e.response.status_code, e.response.text) from e
        except ValidationError as e:
            raise LAAError(f"Failed to parse API response: {e}") from e

    def ski_rental_decide(
        self,
        buy_cost: float,
        current_day: int,
        prediction_days: float,
        trust: float = 0.5
    ) -> DecisionResponse:
        """
        Makes a ski rental decision using the LAA API.
        """
        data = {
            "buy_cost": buy_cost,
            "current_day": current_day,
            "prediction_days": prediction_days,
            "trust": trust
        }
        return self._make_request("POST", "/algorithms/ski-rental/decide", data, DecisionResponse)

    def randomized_ski_rental_decide(
        self,
        buy_cost: float,
        current_day: int,
        prediction_days: float,
        trust: float = 0.5
    ) -> DecisionResponse:
        """
        Makes a randomized ski rental decision using the LAA API.
        """
        data = {
            "buy_cost": buy_cost,
            "current_day": current_day,
            "prediction_days": prediction_days,
            "trust": trust
        }
        return self._make_request("POST", "/algorithms/randomized-ski-rental/decide", data, DecisionResponse)

    def caching_decide(
        self,
        cache_size: int,
        predictions: Dict[int, int],
        item: int,
        cache: List[int]
    ) -> CachingResponse:
        """
        Makes a caching decision using the LAA API.
        """
        data = {
            "cache_size": cache_size,
            "predictions": predictions,
            "item": item,
            "cache": cache
        }
        return self._make_request("POST", "/algorithms/caching/decide", data, CachingResponse)

    def oneway_trading_decide(
        self,
        buy_price: float,
        current_price: float,
        prediction_price: float,
        trust: float = 0.5
    ) -> DecisionResponse:
        """
        Makes a oneway trading decision using the LAA API.
        """
        data = {
            "buy_price": buy_price,
            "current_price": current_price,
            "prediction_price": prediction_price,
            "trust": trust
        }
        return self._make_request("POST", "/algorithms/oneway-trading/decide", data, DecisionResponse)

    def scheduling_decide(
        self,
        num_machines: int,
        job_lengths: List[int],
        prediction_job_lengths: List[int]
    ) -> SchedulingResponse:
        """
        Makes a scheduling decision using the LAA API.
        """
        data = {
            "num_machines": num_machines,
            "job_lengths": job_lengths,
            "prediction_job_lengths": prediction_job_lengths
        }
        return self._make_request("POST", "/algorithms/scheduling/decide", data, SchedulingResponse)

    def search_decide(
        self,
        max_value: int,
        values: List[int],
        prediction_value: int
    ) -> SearchResponse:
        """
        Makes a search decision using the LAA API.
        """
        data = {
            "max_value": max_value,
            "values": values,
            "prediction_value": prediction_value
        }
        return self._make_request("POST", "/algorithms/search/decide", data, SearchResponse)
