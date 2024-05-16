import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

from block import blocks
from PyMLib.regressions import LinearRegression


class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)

        if e.button() == Qt.LeftButton:
            print('press')


class PyMLibGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.blocks.addItems(blocks)

    def init_ui(self):
        uic.loadUi("design.ui", self)
        self.show()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyMLibGUI()
    ex.show()
    app.exec_()

