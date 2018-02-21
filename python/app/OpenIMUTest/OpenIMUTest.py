
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtChart import QChart, QChartView, QLineSeries
import numpy as np


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size - 1) * 2 + 1:2] = xdata
    memory[1:(size - 1) * 2 + 2:2] = ydata
    return polyline


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)

    def set_title(self, title):
        self.chart.setTitle(title)

    def add_data(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    window = TestWindow()

    # 100Hz, one day accelerometer values
    npoints = 100 * 60 * 24

    # Time
    xdata = np.linspace(0., 10., npoints)

    window.add_data(xdata, np.sin(xdata), color=Qt.red)
    window.add_data(xdata, np.cos(xdata), color=Qt.green)
    window.add_data(xdata, np.cos(2 * xdata), color=Qt.blue)
    window.set_title("Simple example with %d curves of %d points "\
                     "(OpenGL Accelerated Series)"\
                     % (window.ncurves, npoints))
    window.setWindowTitle("Simple performance example")
    window.show()
    window.resize(500, 400)

    sys.exit(app.exec_())