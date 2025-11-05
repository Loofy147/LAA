
import requests
from typing import Dict, Any, List

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

    def ski_rental_decide(
        self,
        buy_cost: float,
        current_day: int,
        prediction_days: float,
        trust: float = 0.5
    ) -> Dict[str, Any]:
        """
        Makes a ski rental decision using the LAA API.

        Args:
            buy_cost: The cost of buying skis.
            current_day: The current day number.
            prediction_days: The predicted number of ski days.
            trust: A value between 0 and 1 indicating trust in the prediction.

        Returns:
            A dictionary containing the API response.
        """
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
        """
        Makes a caching decision using the LAA API.

        Args:
            cache_size: The maximum size of the cache.
            predictions: A map of item IDs to their predicted future access times.
            item: The item being accessed.
            cache: The current state of the cache.

        Returns:
            A dictionary containing the API response.
        """
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
        """
        Makes a oneway trading decision using the LAA API.

        Args:
            buy_price: The initial price of the asset.
            current_price: The current price of the asset.
            prediction_price: The predicted future price of the asset.
            trust: A value between 0 and 1 indicating trust in the prediction.

        Returns:
            A dictionary containing the API response.
        """
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
        """
        Makes a scheduling decision using the LAA API.

        Args:
            num_machines: The number of machines available for scheduling.
            job_lengths: A list of the actual lengths of the jobs.
            prediction_job_lengths: A list of the predicted lengths of the jobs.

        Returns:
            A dictionary containing the API response.
        """
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
        """
        Makes a search decision using the LAA API.

        Args:
            max_value: The maximum possible value in the search space.
            values: The list of values to search through.
            prediction_value: The predicted index of the best value.

        Returns:
            A dictionary containing the API response.
        """
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
