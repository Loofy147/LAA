
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

    def test_item_already_in_cache(self):
        predictions = {1: 10, 2: 5}
        caching = laa_core.Caching(2, predictions)
        cache = [1, 2]
        decision, new_cache = caching.decide(1, cache)
        assert decision == True
        assert new_cache == [1, 2]

    def test_cache_not_full(self):
        predictions = {1: 10, 2: 5, 3: 12}
        caching = laa_core.Caching(3, predictions)
        cache = [1, 2]
        decision, new_cache = caching.decide(3, cache)
        assert decision == False, "Adding an item to a non-full cache should be a miss."
        assert new_cache == [1, 2, 3]

    def test_missing_predictions(self):
        """Items with missing predictions should be evicted first."""
        predictions = {2: 5} # Prediction for 1 is missing
        caching = laa_core.Caching(2, predictions)
        cache = [1, 2]
        decision, new_cache = caching.decide(3, cache)
        assert decision == False
        # Item 1 should be evicted as it has no prediction
        assert new_cache == [2, 3], "Should evict the item with the missing prediction."

class TestOnewayTradingGuarantees:
    def test_consistency(self):
        ot = laa_core.OnewayTrading(100.0)
        decision = ot.decide(110.0, 120.0, 0.5)
        assert decision == True

    def test_price_below_threshold(self):
        ot = laa_core.OnewayTrading(100.0)
        decision = ot.decide(109.0, 120.0, 0.5)
        assert decision == False

    def test_full_trust(self):
        ot = laa_core.OnewayTrading(100.0)
        # Threshold should equal prediction
        assert ot.decide(120.0, 120.0, 1.0) == True
        assert ot.decide(119.0, 120.0, 1.0) == False

    def test_zero_trust(self):
        ot = laa_core.OnewayTrading(100.0)
        # Threshold should equal buy_price
        assert ot.decide(100.0, 120.0, 0.0) == True
        assert ot.decide(99.0, 120.0, 0.0) == False

class TestSchedulingGuarantees:
    def test_consistency(self):
        scheduling = laa_core.Scheduling(2)
        job_lengths = [10, 5, 12]
        predictions = [5, 10, 12]
        assignments = scheduling.decide(job_lengths, predictions)
        assert assignments == [0, 1, 1]

    def test_more_machines_than_jobs(self):
        scheduling = laa_core.Scheduling(3)
        job_lengths = [10, 20]
        predictions = [5, 1]
        assignments = scheduling.decide(job_lengths, predictions)
        assert assignments == [1, 0]

    def test_identical_predictions(self):
        scheduling = laa_core.Scheduling(2)
        job_lengths = [10, 5, 12]
        predictions = [5, 10, 5]
        assignments = scheduling.decide(job_lengths, predictions)
        # Job 0 (pred 5), Job 2 (pred 5), Job 1 (pred 10)
        # Job 0 -> Machine 0
        # Job 2 -> Machine 1
        # Job 1 -> Machine 0
        assert assignments == [0, 0, 1]

class TestSearchGuarantees:
    def test_consistency(self):
        search = laa_core.Search(100)
        values = [10, 5, 12, 50, 99]
        prediction = 4
        best_index = search.decide(values, prediction)
        assert best_index == 4

    def test_prediction_out_of_bounds(self):
        search = laa_core.Search(100)
        values = [10, 20, 30]
        prediction = 10
        best_index = search.decide(values, prediction)
        assert best_index == 2

    def test_highest_value_before_prediction(self):
        search = laa_core.Search(100)
        values = [50, 10, 20]
        prediction = 1
        best_index = search.decide(values, prediction)
        assert best_index == 0

    def test_duplicate_values(self):
        search = laa_core.Search(100)
        values = [10, 50, 20, 50]
        prediction = 3
        best_index = search.decide(values, prediction)
        assert best_index == 1
