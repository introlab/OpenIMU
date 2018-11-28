from PyQt5.QtWidgets import QGraphicsView, QRubberBand
from PyQt5.QtCore import pyqtSignal, QPoint, QRect, QSize


class TimeView(QGraphicsView):

    time_clicked = pyqtSignal(float)
    time_selected = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(QGraphicsView, self).__init__(parent=parent)
        self.initialClick = QPoint()
        self.selectionBand = QRubberBand(QRubberBand.Rectangle, self)
        self.selecting = False

    def wheelEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        clicked_x = self.mapToScene(event.pos()).x()
        self.selectionBand.hide()
        if clicked_x == self.mapToScene(self.initialClick).x():
            self.time_clicked.emit(clicked_x)
        else:
            if self.initialClick.x() < clicked_x:
                self.time_selected.emit(self.mapToScene(self.initialClick).x(), clicked_x)
            else:
                self.time_selected.emit(clicked_x, self.mapToScene(self.initialClick).x())

        self.selecting = False

    def mousePressEvent(self, event):
        self.selecting = True
        self.initialClick = event.pos()
        self.selectionBand.setGeometry(QRect(self.initialClick.x(), 0, 1, self.height()))
        self.selectionBand.show()

    def mouseMoveEvent(self, event):
        if self.selecting:
            current_pos = event.pos()
            if current_pos.x() < self.initialClick.x():
                start_x = current_pos.x()
                width = self.initialClick.x() - start_x
            else:
                start_x = self.initialClick.x()
                width = current_pos.x() - self.initialClick.x()
            self.selectionBand.setGeometry(QRect(start_x, 0, width, self.height()))
