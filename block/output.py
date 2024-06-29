from PyQt5.QtWidgets import QFileDialog

from block.base import BaseBlock, BlockType
import pandas as pd


class Output(BaseBlock):
    __block_name__ = 'Output'
    __block_type__ = BlockType.OUTPUT

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

        self.data = None

    def on_click(self, event):
        if not self.data:
            return

        filename, _ = QFileDialog.getSaveFileName()
        self.data.to_csv(filename)
