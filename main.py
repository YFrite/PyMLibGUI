import sys
from typing import Type

import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, \
    QWidget, QPushButton, QHBoxLayout, QGraphicsSimpleTextItem
from sklearn.metrics import mean_squared_error

from PyMLib.classifications import LogisticRegression
from PyMLib.regressions import LinearRegression
from block import BaseBlock, FeaturesInput, BlockType, TargetInput, Algorithm, Output
from widgets.graph_arrow import Arrow


class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.start_item = None
        self.current_arrow = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if isinstance(item, BaseBlock):
                self.start_item = item
            elif isinstance(item, QGraphicsSimpleTextItem):
                self.start_item = item.parentItem()
            else:
                item = None

            if item:
                self.current_arrow = Arrow(self.start_item)
                self.scene().addItem(self.current_arrow)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.current_arrow:
            return

        self.current_arrow.update_path(self.mapToScene(event.pos()))

    def connect_graph(self, event):
        if not self.current_arrow:
            return

        item = self.itemAt(event.pos())

        if isinstance(item, BaseBlock):
            item = item
        elif isinstance(item, QGraphicsSimpleTextItem):
            item = item.parentItem()
        else:
            item = None

        if (item and not (self.start_item == item)
                and item.__block_type__ in BlockType.can_connect(self.start_item.__block_type__)):
            self.current_arrow.set_end_item(item)
            item.inputs.append(self.start_item)
        else:
            self.scene().removeItem(self.current_arrow)
            self.current_arrow.remove_arrow()

        self.current_arrow = None
        self.start_item = None

    def on_click(self, event):
        item = self.itemAt(event.pos())

        if not isinstance(item, BaseBlock): return

        item.on_click(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.RightButton:
            self.connect_graph(event)
            return
        self.on_click(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.outputs = []
        self.algorithms = []
        self.history = []

        self.setWindowTitle("PyMLibGUI")
        self.setGeometry(500, 500, 900, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Block menu
        self.left_panel = QVBoxLayout()
        self.left_panel.setAlignment(Qt.AlignTop)
        layout.addLayout(self.left_panel)

        self.add_block_button(FeaturesInput)
        self.add_block_button(TargetInput)
        self.add_block_button(Output)

        self.add_block_button(Algorithm, LinearRegression)
        self.add_block_button(Algorithm, LogisticRegression)

        # Bake button
        button = QPushButton("Bake!")
        button.clicked.connect(self.bake)
        self.left_panel.addWidget(button, alignment=Qt.AlignBottom)

        # Graph view
        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 600, 600)
        layout.addWidget(self.view)

    def bake(self):
        if not self.outputs: return

        for output in self.outputs:
            predicted, target = self.do_magic(output, None)

            pd.DataFrame({f"prediction_{i}": predicted[:, i] for i in range(predicted.shape[1])}).to_csv("predicted.csv", index=False)

            print(mean_squared_error(predicted, target))

    def do_magic(self, current_block, prev):
        print(type(current_block).__name__, "->", end=" ")

        for arrow in current_block.arrows:
            start_block = arrow.start_item

            print(type(start_block).__name__, " ->", end=" ")

            if prev == start_block: return

            if start_block.__block_type__ == BlockType.INPUT:
                return start_block.run()

            target = list(filter(lambda x: isinstance(x, TargetInput), start_block.inputs))[0].run()
            inputs = list(filter(lambda x: not isinstance(x, TargetInput), start_block.inputs))

            return start_block.run(target=target,
                                   X=np.concatenate([self.do_magic(input, start_block) for input in inputs], axis=1)), target

    def add_block_button(self, block_type: Type[BaseBlock], algorithm=None):
        button = QPushButton(block_type.__block_name__ if not algorithm else algorithm.__name__)
        button.clicked.connect(lambda: self.create_block(block_type, algorithm))
        self.left_panel.addWidget(button)

    def create_block(self, block_type: Type[BaseBlock], algorithm=None):
        if algorithm:
            block = block_type(0, 0, 200, 60, algorithm=algorithm)
            block.set_text(algorithm.__name__)
        else:
            block = block_type(0, 0, 200, 60, )
            block.set_text()
            if block.__block_type__ == BlockType.OUTPUT:
                self.outputs.append(block)

        self.scene.addItem(block)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
