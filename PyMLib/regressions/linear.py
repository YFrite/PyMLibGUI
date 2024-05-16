from typing import Optional, Self

import numpy as np

from PyMLib.base import BaseModel
from PyMLib.optimizers import StochasticGradientDescent
from PyMLib.optimizers.base import BaseOptimizer


class LinearRegression(BaseModel):
    def __init__(self, optimizer: Optional[BaseOptimizer] = None):
        self._optimizer = None
        self.optimizer = optimizer or StochasticGradientDescent()

    def fit(self, X: np.ndarray, target: np.ndarray,
            epochs: Optional[int] = 100,
            batch_size: Optional[int] = None,
            tolerance: Optional[float] = None,
            epsilon: float = 3e-2) -> Self:
        if self.weights is None:
            self._optimizer.weights = np.random.normal(size=(X.shape[1], 1))

        if not batch_size:
            batch_size = X.shape[0]

        if tolerance:
            return self._fit_tolerance(tolerance, epsilon)

        return self._fit_epochs(X, target, epochs, epsilon, batch_size)

    def _fit_tolerance(self, tolerance: float, epsilon: float) -> Self:
        return self

    def _fit_epochs(self, X: np.ndarray, target: np.ndarray,
                    epochs: int, epsilon: float, batch_size: int, ) -> Self:
        for epoch in range(epochs):
            for margin in range(0, X.shape[0], batch_size):
                # TODO: DataLoader
                x_batch = X[margin: margin+batch_size]
                target_batch = target[margin: margin+batch_size].reshape(-1, 1)
                predicted = self.predict(x_batch)
                if self._optimizer.step(x_batch, target_batch, predicted, epsilon):
                    return self
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return X.dot(self._optimizer.weights)

    @property
    def optimizer(self) -> BaseOptimizer:
        return self._optimizer

    @optimizer.setter
    def optimizer(self, value: BaseOptimizer):
        if not isinstance(value, BaseOptimizer):
            raise ValueError("`optimizer` must be BaseOptimizer instance")

        self._optimizer = value

    @property
    def weights(self):
        return self._optimizer.weights
