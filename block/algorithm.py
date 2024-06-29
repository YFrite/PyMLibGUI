from typing import Type

from PyQt5.QtWidgets import QFileDialog

from PyMLib.base import BaseModel
from block.base import BaseBlock, BlockType
import pandas as pd


class Algorithm(BaseBlock):
    __block_name__ = 'Algorithm'
    __block_type__ = BlockType.ALGORITHM

    def __init__(self, *kwargs, algorithm: Type[BaseModel], ):
        self.algorithm_name = algorithm.__name__

        super().__init__(*kwargs)
        self.data = None

        self.algorithm = algorithm()

    def on_click(self, event):
        pass

    def run(self, X, target):
        return self.algorithm.fit(X=X, target=target, epochs=100).predict(X=X).reshape(-1, 1)
