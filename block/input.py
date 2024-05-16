import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.uic.properties import QtGui

from block.base import ABCBlock


class Input(ABCBlock, QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = None
        self.dataframe = None

    def draw(self):
        pass

    def on_click(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Select csv file:')
        self.dataframe = pd.read_csv(self.file_name)

