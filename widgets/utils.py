from PyQt5.QtCore import QPointF, QMarginsF


def calculate_control_points(start_pos, end_pos):
    dx = end_pos.x() - start_pos.x()
    dy = end_pos.y() - start_pos.y()

    control_point1 = QPointF(start_pos.x() + dx * 0.25, start_pos.y())
    control_point2 = QPointF(end_pos.x() - dx * 0.25, end_pos.y())

    return control_point1, control_point2


def calculate_edge_points(dest_item):
    dest_rect = dest_item.sceneBoundingRect().marginsRemoved(QMarginsF(1, 1, 1, 1))

    d_dest = dest_rect.right() - dest_rect.left()
    x_dest = dest_rect.left() + d_dest / 2

    return QPointF(x_dest, dest_rect.top()), QPointF(x_dest, dest_rect.bottom())
