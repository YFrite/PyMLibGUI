import numpy as np
from PyQt5.QtWidgets import QFileDialog

from block.base import BaseBlock, BlockType
import pandas as pd


class FeaturesInput(BaseBlock):
    __block_name__ = 'Features'
    __block_type__ = BlockType.INPUT

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

        self.data = None

    def on_click(self, event):
        file_name = QFileDialog.getOpenFileName(self.parentItem(), "Select csv features file", ".", "*.csv")[0]
        if not file_name: return

        self.data = pd.read_csv(file_name)

    def run(self) -> np.ndarray:
        return self.data.to_numpy().astype(np.float32)
