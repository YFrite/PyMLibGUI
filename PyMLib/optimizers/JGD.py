import numpy as np

from PyMLib.optimizers import StochasticGradientDescent

class JumpingGradientDescent(StochasticGradientDescent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []

    def step(self, X: np.ndarray, target: np.ndarray,
             predicted: np.ndarray, epsilon: float = 1e-5) -> bool:
        grad = -X.T.dot(target - predicted)
        self.history.append(((sum((target - predicted) ** 2) / 50) ** 0.5)[0])

        if abs(grad).sum() <= epsilon:
            return True

        self._weights -= self._learning_rate * grad
        return False