from abc import ABC, abstractmethod

import numpy as np


class BaseOptimizer(ABC):

    @abstractmethod
    def step(self, **kwargs) -> bool:
        pass
