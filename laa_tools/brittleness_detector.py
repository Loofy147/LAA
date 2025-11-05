
import numpy as np

class BrittlenessDetector:
    """
    Analyzes the brittleness of a learning-augmented algorithm.

    Brittleness in a learning-augmented algorithm refers to a rapid degradation
    of performance when small errors (noise) are introduced to the predictions it
    relies on. This class quantifies brittleness by measuring the performance
    (competitive ratio) at various noise levels and calculating the gradient of
    this degradation.

    A steep gradient at low noise levels indicates a brittle algorithm, meaning
    its performance is not robust to minor prediction inaccuracies.
    """

    def __init__(self, algorithm, problem_generator):
        """
        Initializes the BrittlenessDetector.

        Args:
            algorithm: An object representing the learning-augmented algorithm. It must
                have a `run(problem, prediction)` method that returns the algorithm's
                cost.
            problem_generator: An object that generates problem instances. It must have a
                `generate()` method that returns a problem object. The problem object
                must have `get_perfect_prediction()` and `compute_optimal()` methods.
        """
        self.algorithm = algorithm
        self.problem_generator = problem_generator

    def analyze(self, num_trials=100, epsilons=None, threshold=0.5):
        """
        Performs the brittleness analysis by simulating performance under noisy predictions.

        The method runs multiple trials for each noise level (`epsilon`), calculates the
        average competitive ratio, and then determines the performance degradation
        gradient near zero noise.

        Args:
            num_trials (int): The number of random problem instances to generate and
                average over for each epsilon value.
            epsilons (list of float, optional): A list of noise levels to test. Noise is
                applied multiplicatively (prediction * (1 + epsilon)). If None, a
                default logarithmic scale is used.
            threshold (float): The gradient value above which the algorithm is considered
                brittle.

        Returns:
            dict: A dictionary containing the analysis results with the following keys:
                'is_brittle' (bool): True if the performance degradation gradient
                    exceeds the threshold.
                'severity' (float): The calculated gradient of the competitive ratio
                    with respect to the prediction error (epsilon).
                'profile' (dict): A dictionary mapping each epsilon to the average
                    competitive ratio observed at that noise level.
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
    print("Brittleness Analysis:")
    print(f"  - Is Brittle: {analysis['is_brittle']}")
    print(f"  - Severity Gradient: {analysis['severity']:.4f}")
    print("  - Performance Profile:")
    for eps, ratio in analysis['profile'].items():
        print(f"    - Epsilon={eps:.1e}: Competitive Ratio={ratio:.4f}")
