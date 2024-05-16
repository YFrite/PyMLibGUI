import numpy as np

from PyMLib.regressions import LinearRegression


class LogisticRegression(LinearRegression):
    def predict_target(self, X: np.ndarray, predicate: float = 0.5) -> np.ndarray:
        return np.where(self.predict(X) >= predicate, 1, 0)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-X @ self.weights))
