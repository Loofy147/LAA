
import pytest
import laa_core
import numpy as np

class TestSkiRentalGuarantees:
    def test_consistency_perfect_prediction(self):
        """With perfect prediction, should achieve near-optimal"""
        sr = laa_core.SkiRental(buy_cost=100.0)

        # Perfect prediction: 120 days
        actual_days = 120
        prediction = float(actual_days)
        trust = 1.0  # Full trust

        # Track when algorithm buys
        buy_day = None
        for day in range(1, 200):
            if sr.decide(day, prediction, trust):
                buy_day = day
                break

        # Optimal: buy at day 100 (if >100 days) or never buy (if ≤100)
        if actual_days > 100:
            # Should buy around day 100-120
            assert 100 <= buy_day <= 120, f"Bought at day {buy_day}, expected 100-120"

            # Competitive ratio
            alg_cost = buy_day - 1 + 100
            opt_cost = 100
            cr = alg_cost / opt_cost

            assert cr <= 2.2, f"CR={cr}, expected ≤2.2 for consistency"

    def test_robustness_worst_prediction(self):
        """With worst prediction, should never exceed 2-competitive"""
        sr = laa_core.SkiRental(buy_cost=100.0)

        # Worst case: prediction is completely wrong
        actual_days = 50
        prediction = 200.0  # Way off
        trust = 0.0  # Zero trust (pure classical)

        buy_day = None
        for day in range(1, 200):
            if sr.decide(day, prediction, trust):
                buy_day = day
                break

        # Classical algorithm buys at day 100
        assert buy_day == 100, f"Bought at day {buy_day}, expected 100"

        # Competitive ratio (stopped at day 50)
        alg_cost = min(buy_day, actual_days)
        opt_cost = min(actual_days, 100)
        cr = alg_cost / opt_cost

        assert cr <= 2.0, f"CR={cr}, expected ≤2.0 for robustness"

    def test_smoothness(self):
        """Performance should degrade gracefully as error increases"""
        sr = laa_core.SkiRental(buy_cost=100.0)
        actual_days = 120
        trust = 0.7

        errors = [0.0, 0.1, 0.2, 0.5]
        crs = []

        for error in errors:
            prediction = actual_days * (1 + error)

            buy_day = None
            for day in range(1, 200):
                if sr.decide(day, prediction, trust):
                    buy_day = day
                    break

            alg_cost = min(buy_day - 1 + 100, actual_days)
            opt_cost = 100  # optimal: just buy
            cr = alg_cost / opt_cost
            crs.append(cr)

        # Check smoothness: CR should increase gradually
        for i in range(len(crs) - 1):
            assert crs[i+1] >= crs[i], f"Not smooth: CR jumped from {crs[i]} to {crs[i+1]}"
            assert crs[i+1] - crs[i] < 0.5, f"Too abrupt: CR jumped {crs[i+1] - crs[i]}"

class TestCachingGuarantees:
    def test_consistency(self):
        predictions = {1: 10, 2: 5, 3: 12}
        caching = laa_core.Caching(2, predictions)
        cache = [1, 2]
        decision, new_cache = caching.decide(3, cache)
        assert decision == False
        assert new_cache == [2, 3]

class TestOnewayTradingGuarantees:
    def test_consistency(self):
        ot = laa_core.OnewayTrading(100.0)
        decision = ot.decide(110.0, 120.0, 0.5)
        assert decision == True

class TestSchedulingGuarantees:
    def test_consistency(self):
        scheduling = laa_core.Scheduling(2)
        job_lengths = [10, 5, 12]
        predictions = [5, 10, 12]
        assignments = scheduling.decide(job_lengths, predictions)
        assert assignments == [0, 1, 1]

class TestSearchGuarantees:
    def test_consistency(self):
        search = laa_core.Search(100)
        values = [10, 5, 12, 50, 99]
        prediction = 4
        best_index = search.decide(values, prediction)
        assert best_index == 4
