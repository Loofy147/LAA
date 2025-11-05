
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

    def analyze(self, num_trials=100, epsilons=None):
        """
        Performs the brittleness analysis.

        Args:
            num_trials: The number of random problem instances to generate.
            epsilons: A list of noise levels to test.

        Returns:
            A dictionary where keys are the epsilon values (noise levels) and
            values are the average performance ratios at those noise levels.
        """
        if epsilons is None:
            epsilons = np.logspace(-6, -1, 6)

        results = {epsilon: [] for epsilon in epsilons}

        for _ in range(num_trials):
            problem = self.problem_generator.generate()
            perfect_prediction = problem.get_perfect_prediction()

            for epsilon in epsilons:
                noisy_prediction = perfect_prediction * (1 + epsilon)
                alg_cost = self.algorithm.run(problem, noisy_prediction)
                opt_cost = problem.compute_optimal()
                results[epsilon].append(alg_cost / opt_cost)

        return {
            epsilon: np.mean(costs) for epsilon, costs in results.items()
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
