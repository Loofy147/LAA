
from mapie.regression import SplitConformalRegressor
from mapie.utils import train_conformalize_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression

class UQPredictionAdapter:
    def __init__(self, base_predictor=LinearRegression(), confidence_level=0.95):
        self.conformalizer = SplitConformalRegressor(
            estimator=base_predictor,
            confidence_level=confidence_level,
            prefit=False
        )

    def fit(self, X, y):
        (
            X_train, X_conformalize, self.X_test_dummy,
            y_train, y_conformalize, self.y_test_dummy
        ) = train_conformalize_test_split(
            X, y, train_size=0.6, conformalize_size=0.2, test_size=0.2, random_state=42
        )
        self.conformalizer.fit(X_train, y_train).conformalize(X_conformalize, y_conformalize)

    def predict(self, X):
        y_pred, intervals = self.conformalizer.predict_interval(X)
        return {
            'point': y_pred,
            'lower': intervals[:, 0, 0],
            'upper': intervals[:, 1, 0],
            'uncertainty': intervals[:, 1, 0] - intervals[:, 0, 0]
        }

if __name__ == '__main__':
    X, y = make_regression(n_samples=105, n_features=1, noise=10.0, random_state=42)
    adapter = UQPredictionAdapter()
    adapter.fit(X, y)
    predictions = adapter.predict(adapter.X_test_dummy)
    print(predictions)
