
import pytest
from laa_tools.brittleness_detector import BrittlenessDetector

class DummyProblem:
    """A simple problem definition for testing."""
    def get_perfect_prediction(self):
        return 100.0
    def compute_optimal(self):
        return 100.0

class BrittleDummyAlgorithm:
    """An algorithm that exhibits brittle behavior."""
    def run(self, problem, prediction):
        # Performance collapses with any noise
        if prediction > 100.0:
            return 200.0
        return 100.0

class SmoothDummyAlgorithm:
    """An algorithm that exhibits smooth behavior."""
    def run(self, problem, prediction):
        # Performance degrades gracefully
        error = abs(prediction - 100.0) / 100.0
        return 100.0 * (1 + error)

class DummyProblemGenerator:
    """Generates dummy problem instances."""
    def generate(self):
        return DummyProblem()

def test_brittleness_detector_identifies_brittle_algorithm():
    """The detector should correctly identify a brittle algorithm."""
    brittle_algo = BrittleDummyAlgorithm()
    detector = BrittlenessDetector(brittle_algo, DummyProblemGenerator())

    # Use a small epsilon to check for the jump
    analysis = detector.analyze(num_trials=10, epsilons=[0.0, 1e-6], threshold=1000)

    assert analysis['is_brittle'] == True, "The detector failed to identify a brittle algorithm."
    assert analysis['severity'] > 1000, "The severity of the brittleness was not calculated correctly."

def test_brittleness_detector_identifies_smooth_algorithm():
    """The detector should correctly identify a smooth algorithm."""
    smooth_algo = SmoothDummyAlgorithm()
    detector = BrittlenessDetector(smooth_algo, DummyProblemGenerator())

    analysis = detector.analyze(num_trials=10, epsilons=[0.0, 1e-6], threshold=1000)

    assert analysis['is_brittle'] == False, "The detector incorrectly identified a smooth algorithm as brittle."
    assert analysis['severity'] < 1000, "The severity for a smooth algorithm should be low."
