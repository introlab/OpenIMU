# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with
a high number of points, using OpenGL accelerated series
"""
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QLegend


class IMUChartView(QChartView):
    def __init__(self, parent=None):
        super(QChartView, self).__init__(parent=parent)

        self.chart = QChart()
        self.setChart(self.chart)
        #self.chart.legend().hide()
        self.ncurves = 0
        self.setRenderHint(QPainter.Antialiasing)

    def add_data(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(self.series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1

    def set_title(self, title):
        print('Setting title: ',title)
        self.chart.setTitle(title)

    def series_to_polyline(self, xdata, ydata):
        """Convert series data to QPolygon(F) polyline

        This code is derived from PythonQwt's function named
        `qwt.plot_curve.series_to_polyline`"""
        size = len(xdata)
        polyline = QPolygonF(size)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
        memory = np.frombuffer(pointer, dtype)
        memory[:(size-1)*2+1:2] = xdata
        memory[1:(size-1)*2+2:2] = ydata
        return polyline


# Testing app
if __name__ == '__main__':
    import sys
    import numpy as np
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    window = QMainWindow()
    button = QPushButton(window)
    button.setText('hello world')
    imuView = IMUChartView(window)

    #100Hz, one day accelerometer values
    npoints = 100 * 60 * 24

    xdata = np.linspace(0., 10., npoints)
    imuView.add_data(xdata, np.sin(xdata), color=Qt.red)
    imuView.add_data(xdata, np.cos(xdata), color=Qt.green)
    imuView.add_data(xdata, np.cos(2 * xdata), color=Qt.blue)
    imuView.set_title("Simple example with %d curves of %d points "\
                     "(OpenGL Accelerated Series)"\
                     % (imuView.ncurves, npoints))

    imuView.set_title('IMUView demo')
    window.setCentralWidget(imuView)
    window.setWindowTitle("IMUChartView Demo")
    window.resize(640,480)
    window.show()
    sys.exit(app.exec_())