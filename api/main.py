
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import laa_core

app = FastAPI(title="LAA Platform API", version="0.1.0")

class SkiRentalRequest(BaseModel):
    """Request model for the Ski Rental algorithm."""
    buy_cost: float
    current_day: int
    prediction_days: float
    trust: float

class CachingRequest(BaseModel):
    """Request model for the Caching algorithm."""
    cache_size: int
    predictions: Dict[int, int]
    item: int
    cache: List[int]

class OnewayTradingRequest(BaseModel):
    """Request model for the Oneway Trading algorithm."""
    buy_price: float
    current_price: float
    prediction_price: float
    trust: float

class SchedulingRequest(BaseModel):
    """Request model for the Scheduling algorithm."""
    num_machines: int
    job_lengths: List[int]
    prediction_job_lengths: List[int]

class SearchRequest(BaseModel):
    """Request model for the Search algorithm."""
    max_value: int
    values: List[int]
    prediction_value: int

@app.post("/algorithms/ski-rental/decide")
def ski_rental_decide(req: SkiRentalRequest):
    """
    Determines whether to buy or rent skis based on the Ski Rental algorithm.

    Args:
        req: A SkiRentalRequest object containing the input parameters.

    Returns:
        A dictionary containing the decision ("buy" or "rent"), the algorithm name,
        and the trust parameter used.
    """
    try:
        sr = laa_core.SkiRental(req.buy_cost)
        decision = sr.decide(req.current_day, req.prediction_days, req.trust)
        return {
            "decision": "buy" if decision else "rent",
            "algorithm": "ski_rental",
            "trust_parameter": req.trust
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/algorithms/caching/decide")
def caching_decide(req: CachingRequest):
    """
    Makes a caching decision based on the Caching algorithm.

    Args:
        req: A CachingRequest object containing the input parameters.

    Returns:
        A dictionary containing the decision ("hit" or "miss"), the new cache state,
        and the algorithm name.
    """
    try:
        caching = laa_core.Caching(req.cache_size, req.predictions)
        decision, new_cache = caching.decide(req.item, req.cache)
        return {
            "decision": "hit" if decision else "miss",
            "new_cache": new_cache,
            "algorithm": "caching",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/algorithms/oneway-trading/decide")
def oneway_trading_decide(req: OnewayTradingRequest):
    """
    Makes a trading decision based on the Oneway Trading algorithm.

    Args:
        req: An OnewayTradingRequest object containing the input parameters.

    Returns:
        A dictionary containing the decision ("buy" or "wait"), the algorithm name,
        and the trust parameter used.
    """
    try:
        ot = laa_core.OnewayTrading(req.buy_price)
        decision = ot.decide(req.current_price, req.prediction_price, req.trust)
        return {
            "decision": "buy" if decision else "wait",
            "algorithm": "oneway_trading",
            "trust_parameter": req.trust,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/algorithms/scheduling/decide")
def scheduling_decide(req: SchedulingRequest):
    """
    Assigns jobs to machines based on the Scheduling algorithm.

    Args:
        req: A SchedulingRequest object containing the input parameters.

    Returns:
        A dictionary containing the job assignments and the algorithm name.
    """
    try:
        scheduling = laa_core.Scheduling(req.num_machines)
        assignments = scheduling.decide(req.job_lengths, req.prediction_job_lengths)
        return {
            "assignments": assignments,
            "algorithm": "scheduling",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/algorithms/search/decide")
def search_decide(req: SearchRequest):
    """
    Finds the best index in a list of values based on the Search algorithm.

    Args:
        req: A SearchRequest object containing the input parameters.

    Returns:
        A dictionary containing the best index found and the algorithm name.
    """
    try:
        search = laa_core.Search(req.max_value)
        best_index = search.decide(req.values, req.prediction_value)
        return {
            "best_index": best_index,
            "algorithm": "search",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Checks the health of the API.

    Returns:
        A dictionary containing the status and version of the API.
    """
    return {"status": "healthy", "version": "0.1.0"}
