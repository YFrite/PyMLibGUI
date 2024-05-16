from PyMLib.base import BaseModel
from PyMLib.optimizers.base import BaseOptimizer
from block.base import ABCBlock


class AI(ABCBlock):
    def __init__(self, algorithm: BaseModel, optimizer: BaseOptimizer = None,  **kwargs):
        super().__init__(**kwargs)
        self.algorithm = algorithm
        self.optimizer = optimizer or self.algorithm.optimizer
        self.algorithm.optimizer = self.optimizer

    def draw(self):
        pass
