
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Dict, List
import laa_core

app = FastAPI(title="LAA Platform API", version="0.1.0")

# Request Models with Validation

class SkiRentalRequest(BaseModel):
    """Request model for the Ski Rental algorithm."""
    buy_cost: float
    current_day: int
    prediction_days: float
    trust: float

    @field_validator('trust')
    def trust_must_be_between_0_and_1(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('trust must be between 0.0 and 1.0')
        return v

    @field_validator('buy_cost', 'current_day', 'prediction_days')
    def values_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('must be non-negative')
        return v

class RandomizedSkiRentalRequest(BaseModel):
    """Request model for the Randomized Ski Rental algorithm."""
    buy_cost: float
    current_day: int
    prediction_days: float
    trust: float

    @field_validator('trust')
    def trust_must_be_between_0_and_1(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('trust must be between 0.0 and 1.0')
        return v

    @field_validator('buy_cost', 'current_day', 'prediction_days')
    def values_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('must be non-negative')
        return v

class CachingRequest(BaseModel):
    """Request model for the Caching algorithm."""
    cache_size: int
    predictions: Dict[int, int]
    item: int
    cache: List[int]

    @field_validator('cache_size')
    def cache_size_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('must be non-negative')
        return v

class OnewayTradingRequest(BaseModel):
    """Request model for the Oneway Trading algorithm."""
    buy_price: float
    current_price: float
    prediction_price: float
    trust: float

    @field_validator('trust')
    def trust_must_be_between_0_and_1(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('trust must be between 0.0 and 1.0')
        return v

    @field_validator('buy_price', 'current_price', 'prediction_price')
    def prices_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('prices must be non-negative')
        return v

class SchedulingRequest(BaseModel):
    """Request model for the Scheduling algorithm."""
    num_machines: int
    job_lengths: List[int]
    prediction_job_lengths: List[int]

    @field_validator('num_machines')
    def num_machines_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('must be positive')
        return v

class SearchRequest(BaseModel):
    """Request model for the Search algorithm."""
    max_value: int
    values: List[int]
    prediction_value: int

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

class HealthResponse(BaseModel):
    status: str
    version: str

# API Endpoints

@app.post("/algorithms/ski-rental/decide", response_model=DecisionResponse)
def ski_rental_decide(req: SkiRentalRequest):
    """
    Determines whether to buy or rent skis based on the Ski Rental algorithm.
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

@app.post("/algorithms/randomized-ski-rental/decide", response_model=DecisionResponse)
def randomized_ski_rental_decide(req: RandomizedSkiRentalRequest):
    """
    Determines whether to buy or rent skis based on the Randomized Ski Rental algorithm.
    """
    try:
        sr = laa_core.RandomizedSkiRental(req.buy_cost)
        decision = sr.decide(req.current_day, req.prediction_days, req.trust)
        return {
            "decision": "buy" if decision else "rent",
            "algorithm": "randomized_ski_rental",
            "trust_parameter": req.trust
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/algorithms/caching/decide", response_model=CachingResponse)
def caching_decide(req: CachingRequest):
    """
    Makes a caching decision based on the Caching algorithm.
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

@app.post("/algorithms/oneway-trading/decide", response_model=DecisionResponse)
def oneway_trading_decide(req: OnewayTradingRequest):
    """
    Makes a trading decision based on the Oneway Trading algorithm.
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

@app.post("/algorithms/scheduling/decide", response_model=SchedulingResponse)
def scheduling_decide(req: SchedulingRequest):
    """
    Assigns jobs to machines based on the Scheduling algorithm.
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

@app.post("/algorithms/search/decide", response_model=SearchResponse)
def search_decide(req: SearchRequest):
    """
    Finds the best index in a list of values based on the Search algorithm.
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

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Checks the health of the API.
    """
    return {"status": "healthy", "version": "0.1.0"}
