
import requests
from laa_tools.uq_prediction_adapter import UQPredictionAdapter
from laa_tools.brittleness_detector import BrittlenessDetector
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.datasets import make_regression

class LAA:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url

    def decide(self, algorithm, problem_instance, prediction):
        url = f'{self.base_url}/decide'
        data = {
            'algorithm': algorithm,
            'problem_instance': problem_instance,
            'prediction': prediction,
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_uq_prediction_adapter(self, base_predictor=LinearRegression(), alpha=0.05):
        return UQPredictionAdapter(base_predictor, alpha)

    def get_brittleness_detector(self, algorithm, problem_generator):
        return BrittlenessDetector(algorithm, problem_generator)

if __name__ == '__main__':
    sdk = LAA()

    # Test SkiRental
    ski_rental_problem = {'buy_cost': 100.0, 'day': 1}
    ski_rental_prediction = {'days': 120.0, 'trust': 0.5}
    ski_rental_decision = sdk.decide('ski_rental', ski_rental_problem, ski_rental_prediction)
    print(f"Ski Rental Decision: {ski_rental_decision}")

    # Test Caching
    caching_problem = {'cache_size': 2, 'predictions': {'1': 10, '2': 5, '3': 12}, 'item': 3, 'cache': [1, 2]}
    caching_prediction = {}
    caching_decision = sdk.decide('caching', caching_problem, caching_prediction)
    print(f"Caching Decision: {caching_decision}")

    # Test OnewayTrading
    oneway_trading_problem = {'buy_price': 100.0, 'current_price': 110.0}
    oneway_trading_prediction = {'price': 120.0, 'trust': 0.5}
    oneway_trading_decision = sdk.decide('oneway_trading', oneway_trading_problem, oneway_trading_prediction)
    print(f"Oneway Trading Decision: {oneway_trading_decision}")

    # Test Scheduling
    scheduling_problem = {'num_machines': 2, 'job_lengths': [10, 5, 12]}
    scheduling_prediction = {'job_lengths': [10, 5, 12]}
    scheduling_decision = sdk.decide('scheduling', scheduling_problem, scheduling_prediction)
    print(f"Scheduling Decision: {scheduling_decision}")

    # Test Search
    search_problem = {'max_value': 100, 'values': [10, 5, 12, 50, 99]}
    search_prediction = {'value': 99}
    search_decision = sdk.decide('search', search_problem, search_prediction)
    print(f"Search Decision: {search_decision}")

    # Test UQPredictionAdapter
    X, y = make_regression(n_samples=105, n_features=1, noise=10.0, random_state=42)
    adapter = sdk.get_uq_prediction_adapter()
    adapter.fit(X, y)
    predictions = adapter.predict(adapter.X_test_dummy)
    print(f"UQ Predictions: {predictions}")

    # Test BrittlenessDetector
    class DummyProblem:
        def get_perfect_prediction(self):
            return 100.0
        def compute_optimal(self):
            return 100.0

    class DummyAlgorithm:
        def run(self, problem, prediction):
            if prediction > 105:
                return 200.0
            else:
                return 110.0

    problem_generator = type('Generator', (), {'generate': lambda self: DummyProblem()})()
    algorithm = DummyAlgorithm()
    detector = sdk.get_brittleness_detector(algorithm, problem_generator)
    analysis = detector.analyze()
    print(f"Brittleness Analysis: {analysis}")
