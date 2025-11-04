
import requests
from typing import Dict, Any, List

class LAAClient:
    """Client SDK for LAA Platform"""

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})

    def ski_rental_decide(
        self,
        buy_cost: float,
        current_day: int,
        prediction_days: float,
        trust: float = 0.5
    ) -> Dict[str, Any]:
        """Make a ski rental decision"""
        response = self.session.post(
            f"{self.api_url}/algorithms/ski-rental/decide",
            json={
                "buy_cost": buy_cost,
                "current_day": current_day,
                "prediction_days": prediction_days,
                "trust": trust
            }
        )
        response.raise_for_status()
        return response.json()

    def caching_decide(
        self,
        cache_size: int,
        predictions: Dict[int, int],
        item: int,
        cache: List[int]
    ) -> Dict[str, Any]:
        """Make a caching decision"""
        response = self.session.post(
            f"{self.api_url}/algorithms/caching/decide",
            json={
                "cache_size": cache_size,
                "predictions": predictions,
                "item": item,
                "cache": cache
            }
        )
        response.raise_for_status()
        return response.json()

    def oneway_trading_decide(
        self,
        buy_price: float,
        current_price: float,
        prediction_price: float,
        trust: float = 0.5
    ) -> Dict[str, Any]:
        """Make a oneway trading decision"""
        response = self.session.post(
            f"{self.api_url}/algorithms/oneway-trading/decide",
            json={
                "buy_price": buy_price,
                "current_price": current_price,
                "prediction_price": prediction_price,
                "trust": trust
            }
        )
        response.raise_for_status()
        return response.json()

    def scheduling_decide(
        self,
        num_machines: int,
        job_lengths: List[int],
        prediction_job_lengths: List[int]
    ) -> Dict[str, Any]:
        """Make a scheduling decision"""
        response = self.session.post(
            f"{self.api_url}/algorithms/scheduling/decide",
            json={
                "num_machines": num_machines,
                "job_lengths": job_lengths,
                "prediction_job_lengths": prediction_job_lengths
            }
        )
        response.raise_for_status()
        return response.json()

    def search_decide(
        self,
        max_value: int,
        values: List[int],
        prediction_value: int
    ) -> Dict[str, Any]:
        """Make a search decision"""
        response = self.session.post(
            f"{self.api_url}/algorithms/search/decide",
            json={
                "max_value": max_value,
                "values": values,
                "prediction_value": prediction_value
            }
        )
        response.raise_for_status()
        return response.json()
