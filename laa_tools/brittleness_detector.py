
import numpy as np

class BrittlenessDetector:
    """
    Analyzes the brittleness of a learning-augmented algorithm.

    This class assesses how the performance of an algorithm degrades as noise is
    introduced into the predictions it relies on.
    """

    def __init__(self, algorithm, problem_generator):
        """
        Initializes the BrittlenessDetector.

        Args:
            algorithm: The learning-augmented algorithm to be analyzed.
            problem_generator: An object that generates problem instances.
        """
        self.algorithm = algorithm
        self.problem_generator = problem_generator

    def analyze(self, num_trials=100, epsilons=None, threshold=0.5):
        """
        Performs the brittleness analysis.
        Args:
            num_trials: The number of random problem instances to generate.
            epsilons: A list of noise levels to test.
            threshold: The gradient threshold to consider an algorithm brittle.
        Returns:
            A dictionary containing the analysis results.
        """
        if epsilons is None:
            epsilons = np.logspace(-6, -1, 6)

        profile = {epsilon: [] for epsilon in epsilons}

        for _ in range(num_trials):
            problem = self.problem_generator.generate()
            perfect_prediction = problem.get_perfect_prediction()

            for epsilon in epsilons:
                noisy_prediction = perfect_prediction * (1 + epsilon)
                alg_cost = self.algorithm.run(problem, noisy_prediction)
                opt_cost = problem.compute_optimal()
                if opt_cost > 0:
                    profile[epsilon].append(alg_cost / opt_cost)

        avg_profile = {eps: np.mean(costs) if costs else 0 for eps, costs in profile.items()}

        sorted_epsilons = sorted(avg_profile.keys())
        if len(sorted_epsilons) < 2:
            return {'is_brittle': False, 'severity': 0, 'profile': avg_profile}

        # Calculate gradient between the first two non-zero noise levels
        c_at_zero = avg_profile[sorted_epsilons[0]]
        c_at_eps1 = avg_profile[sorted_epsilons[1]]
        gradient = (c_at_eps1 - c_at_zero) / sorted_epsilons[1]

        return {
            'is_brittle': gradient > threshold,
            'severity': gradient,
            'profile': avg_profile
        }

if __name__ == '__main__':
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
    detector = BrittlenessDetector(algorithm, problem_generator)
    analysis = detector.analyze()
    print(analysis)
