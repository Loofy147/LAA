
from mapie.regression import SplitConformalRegressor
from mapie.utils import train_conformalize_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression

class UQPredictionAdapter:
    """
    Wraps a scikit-learn compatible regressor to provide Uncertainty Quantification (UQ).

    This adapter uses Split Conformal Prediction, a distribution-free method for
    generating statistically rigorous prediction intervals. For a given confidence level,
    the true value is guaranteed to lie within the prediction interval with a high
    probability. This is crucial for Learning-Augmented Algorithms, as the uncertainty
    can be used to modulate the `trust` parameter or inform algorithmic decisions.

    The implementation relies on the `mapie` library.
    """

    def __init__(self, base_predictor=LinearRegression(), confidence_level=0.95):
        """
        Initializes the UQPredictionAdapter.

        Args:
            base_predictor: An unfitted scikit-learn compatible regressor instance. This
                model will be trained on a subset of the data provided to `fit`.
            confidence_level (float): The desired confidence level for the prediction
                intervals, typically between 0.0 and 1.0. For example, 0.95 means
                the generated intervals are expected to contain the true value 95%
                of the time.
        """
        self.conformalizer = SplitConformalRegressor(
            estimator=base_predictor,
            confidence_level=confidence_level,
            prefit=False
        )

    def fit(self, X, y):
        """
        Fits the underlying regressor and calibrates the conformalizer.

        The method splits the provided data into three sets: one for training the
        base predictor, one for calibrating the conformal prediction method (to
        determine the interval width), and a dummy test set (as required by the
        `mapie` utility function).

        Args:
            X (np.ndarray): The input features of shape `(n_samples, n_features)`.
            y (np.ndarray): The target values of shape `(n_samples,)`.
        """
        (
            X_train, X_conformalize, self.X_test_dummy,
            y_train, y_conformalize, self.y_test_dummy
        ) = train_conformalize_test_split(
            X, y, train_size=0.6, conformalize_size=0.2, test_size=0.2, random_state=42
        )
        self.conformalizer.fit(X_train, y_train).conformalize(X_conformalize, y_conformalize)

    def predict(self, X):
        """
        Makes predictions with calibrated uncertainty intervals.

        Args:
            X (np.ndarray): The input features for which to make predictions, with
                shape `(n_samples, n_features)`.

        Returns:
            dict: A dictionary containing the prediction results:
                'point' (np.ndarray): The point predictions (median of the interval).
                'lower' (np.ndarray): The lower bounds of the prediction intervals.
                'upper' (np.ndarray): The upper bounds of the prediction intervals.
                'uncertainty' (np.ndarray): The widths of the prediction intervals
                    (`upper` - `lower`).
        """
        y_pred, intervals = self.conformalizer.predict_interval(X)
        return {
            'point': y_pred,
            'lower': intervals[:, 0, 0],
            'upper': intervals[:, 1, 0],
            'uncertainty': intervals[:, 1, 0] - intervals[:, 0, 0]
        }

if __name__ == '__main__':
    X, y = make_regression(n_samples=105, n_features=1, noise=10.0, random_state=42)
    adapter = UQPredictionAdapter(confidence_level=0.9)
    adapter.fit(X, y)
    predictions = adapter.predict(adapter.X_test_dummy)

    print("Uncertainty Quantification Example:")
    print(f"Confidence Level: {adapter.conformalizer.confidence_level}")
    print(f"Number of test samples: {len(adapter.y_test_dummy)}")

    in_interval = np.sum(
        (adapter.y_test_dummy >= predictions['lower']) & (adapter.y_test_dummy <= predictions['upper'])
    )
    coverage = in_interval / len(adapter.y_test_dummy)
    print(f"Empirical Coverage: {coverage:.2f}")

    print("\nSample Predictions:")
    for i in range(min(5, len(adapter.y_test_dummy))):
        print(
            f"  - True: {adapter.y_test_dummy[i]:.2f}, "
            f"Pred: {predictions['point'][i]:.2f}, "
            f"Interval: [{predictions['lower'][i]:.2f}, {predictions['upper'][i]:.2f}], "
            f"Uncertainty: {predictions['uncertainty'][i]:.2f}"
        )
