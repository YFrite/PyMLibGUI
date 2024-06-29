from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPolygonF, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsPathItem

from widgets.utils import calculate_edge_points, calculate_control_points


class Arrow(QGraphicsPathItem):
    def __init__(self, start_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = None
        self.arrow_head_height = 10
        self.arrow_head_a_2 = 10
        self.arrow_head = QPolygonF()

        _, self.bottom_pos = calculate_edge_points(start_item)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.setZValue(-1)
        start_item.add_arrow(self)

    def update_arrow(self):
        _, self.bottom_pos = calculate_edge_points(self.start_item)
        top_pos, _ = calculate_edge_points(self.end_item)

        self.update_path(QPointF(top_pos.x(), top_pos.y() - self.arrow_head_height))
        self.draw_arrow_head(top_pos)

    def update_path(self, end_point):
        path = QPainterPath(self.bottom_pos)
        control_point1, control_point2 = calculate_control_points(self.bottom_pos, end_point)
        path.cubicTo(control_point1, control_point2, QPointF(end_point.x(), end_point.y()))

        self.setPath(path)

    def set_end_item(self, item):
        self.end_item = item
        self.end_item.add_arrow(self)
        self.update_arrow()

    def remove_arrow(self):
        self.start_item.arrows.remove(self)

    def draw_arrow_head(self, end_pos):
        p1 = QPointF(end_pos.x() - self.arrow_head_a_2, end_pos.y() - self.arrow_head_height)
        p2 = QPointF(end_pos.x() + self.arrow_head_a_2, end_pos.y() - self.arrow_head_height)
        head_p = QPointF(end_pos.x(), end_pos.y())
        self.arrow_head = QPolygonF([head_p, p1, p2])

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        painter.setBrush(Qt.black)
        painter.drawPolygon(self.arrow_head)
        widget.update()
