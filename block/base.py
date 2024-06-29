from enum import Enum, auto

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSimpleTextItem


class BlockType(Enum):
    NONE = 0
    DATA = auto()
    INPUT = auto()
    OUTPUT = auto()
    ALGORITHM = auto()

    @staticmethod
    def can_connect(other: "BlockType") -> list["BlockType"]:
        available_types = {BlockType.INPUT: [BlockType.OUTPUT, BlockType.ALGORITHM],
                           BlockType.OUTPUT: [BlockType.ALGORITHM],
                           BlockType.ALGORITHM: [BlockType.OUTPUT, BlockType.ALGORITHM]}
        return available_types[other]


class BaseBlock(QGraphicsRectItem):
    __block_type__ = BlockType.NONE
    __block_name__ = "Base"

    def __init__(self, x, y, width, height, margin=20, *args, **kwargs, ):
        super().__init__(x, y, width, height)
        self.margin = margin

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.white)
        self.textItem = None

        # self.sceneBoundingRect()

        self.arrows = []
        self.inputs = []

    def set_text(self, text=None):
        if not text:
            self.textItem = QGraphicsSimpleTextItem(self.__block_name__, self)
        else:
            self.textItem = QGraphicsSimpleTextItem(text, self)

        text_rect = self.textItem.boundingRect()

        text_rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(text_rect.topLeft())

    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for arrow in self.arrows:
                arrow.update_arrow()

        return super().itemChange(change, value)

    def on_click(self, event):
        raise NotImplementedError()
