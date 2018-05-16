from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import pyqtSignal

class TimeView(QGraphicsView):

    time_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super(QGraphicsView, self).__init__(parent=parent)

    def mouseReleaseEvent(self, event):
        self.time_clicked.emit(event.pos().x())