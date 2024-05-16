
import numpy as np

from PyMLib.optimizers.base import BaseOptimizer


class StochasticGradientDescent(BaseOptimizer):
    def __init__(self, learning_rate: float = 3e-4, ):
        self._learning_rate = None
        self.learning_rate = learning_rate
        self._loss_function = None
        self._weights = None

    def step(self, X: np.ndarray | int,
             target: np.ndarray,
             predicted: np.ndarray, epsilon: float = 1e-5) -> bool:
        # grad = 4 * X ** 3
        grad = -X.T.dot(target-predicted)

        if abs(grad).sum() <= epsilon:
            print("stopped")
            return True
        self._weights -= self._learning_rate * grad
        return False

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value):
        self._learning_rate = value

    @learning_rate.setter
    def learning_rate(self, value: float):
        if not isinstance(value, float):
            raise ValueError("`learning_rate` must be float")
        self._learning_rate = value

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise ValueError("`weights` must be numpy array")
        self._weights = value
