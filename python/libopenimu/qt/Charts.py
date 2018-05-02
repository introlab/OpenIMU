# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with
a high number of points, using OpenGL accelerated series
"""
from PyQt5.QtGui import QPolygonF, QPainter, QMouseEvent, QResizeEvent
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QLegend, QBarSeries, QBarSet, QSplineSeries, QXYSeries
from PyQt5.QtChart import QDateTimeAxis, QValueAxis, QBarCategoryAxis
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPointF, QRectF, QPoint, QDateTime

from qwt.plot import QwtPlot
from qwt.plot_curve import QwtPlotCurve


import numpy as np
from scipy.signal import decimate
import datetime


class IMUChartView(QChartView):
    def __init__(self, parent=None):
        super(QChartView, self).__init__(parent=parent)

        self.reftime = datetime.datetime.now()
        self.cursor = QGraphicsLineItem()
        self.scene().addItem(self.cursor)

        # self.setScene(QGraphicsScene())
        self.chart = QChart()
        # self.scene().addItem(self.chart)
        self.setChart(self.chart)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.ncurves = 0
        self.setRenderHint(QPainter.Antialiasing)
        self.setRubberBand(QChartView.HorizontalRubberBand)

        # X, Y label on bottom
        self.xTextItem = QGraphicsSimpleTextItem(self.chart)
        self.xTextItem.setText('X: ')
        self.yTextItem = QGraphicsSimpleTextItem(self.chart)
        self.yTextItem.setText('Y: ')
        self.update_x_y_coords()

        # Track mouse
        self.setMouseTracking(True)

    @pyqtSlot(QPointF)
    def lineseries_clicked(self, point):
        print('lineseries clicked', point)

    @pyqtSlot(QPointF)
    def lineseries_hovered(self, point):
        print('lineseries hovered', point)

    def update_x_y_coords(self):
        self.xTextItem.setPos(self.chart.size().width() / 2 - 100, self.chart.size().height() - 40)
        self.yTextItem.setPos(self.chart.size().width() / 2 + 100, self.chart.size().height() - 40)

    def decimate(self, xdata, ydata):
        assert(len(xdata) == len(ydata))

        # Decimate only if we have too much data
        decimate_factor = len(xdata) / 100000.0

        if decimate_factor > 1.0:
            decimate_factor = int(np.floor(decimate_factor))
            print('decimate factor', decimate_factor)
            # x = decimate(xdata, decimate_factor)
            # y = decimate(ydata, decimate_factor)
            x = np.ndarray(int(len(xdata) / decimate_factor), dtype=np.float64)
            y = np.ndarray(int(len(ydata) / decimate_factor), dtype=np.float64)
            for i in range(len(x)):
                index = i * decimate_factor
                assert(index < len(xdata))
                x[i] = xdata[index]
                y[i] = ydata[index]
                if x[i] < x[0]:
                    print('timestamp error', x[i], x[0])

            print('return size', len(x), len(y), 'timestamp', x[0])
            return x, y
        else:
            return xdata, ydata

    @pyqtSlot(float, float)
    def axis_range_changed(self, min, max):
        print('axis_range_changed', min, max)
        for axis in self.chart.axes():
            axis.applyNiceNumbers()

    def update_axes(self):

        # Get and remove all axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Create new axes
        # Create axis X
        # axisX = QDateTimeAxis()
        # axisX.setTickCount(5)
        # axisX.setFormat("dd MMM yyyy")
        # axisX.setTitleText("Date")
        # self.chart.addAxis(axisX, Qt.AlignBottom)
        # axisX.rangeChanged.connect(self.axis_range_changed)

        axisX = QValueAxis()
        axisX.setTickCount(10)
        axisX.setLabelFormat("%li")
        axisX.setTitleText("Seconds")
        self.chart.addAxis(axisX, Qt.AlignBottom)
        # axisX.rangeChanged.connect(self.axis_range_changed)


        # Create axis Y
        axisY = QValueAxis()
        axisY.setTickCount(5)
        axisY.setLabelFormat("%.3f")
        axisY.setTitleText("Values")
        self.chart.addAxis(axisY, Qt.AlignLeft)
        # axisY.rangeChanged.connect(self.axis_range_changed)

        ymin = None
        ymax = None

        # Attach axes to series, find min-max
        for series in self.chart.series():
            series.attachAxis(axisX)
            series.attachAxis(axisY)
            vect = series.pointsVector()
            for i in range(len(vect)):
                if ymin is None:
                    ymin = vect[i].y()
                    ymax = vect[i].y()
                else:
                    ymin = min(ymin, vect[i].y())
                    ymax = max(ymax, vect[i].y())

        # Update range
        # print('min max', ymin, ymax)
        if ymin is not None:
            axisY.setRange(ymin, ymax)

        # Make the X,Y axis more readable
        axisX.applyNiceNumbers()
        # axisY.applyNiceNumbers()


    def add_data(self, xdata, ydata, color=None, legend_text=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(1.5)
        curve.setPen(pen)

        curve.setUseOpenGL(True)

        # Decimate
        xdecimated, ydecimated = self.decimate(xdata, ydata)

        # Data must be in ms since epoch
        # curve.append(self.series_to_polyline(xdecimated * 1000.0, ydecimated))
        for i in range(len(xdecimated)):
            # TODO hack
            self.reftime = datetime.datetime.fromtimestamp(xdecimated[0])
            x = xdecimated[i] - xdecimated[0]
            curve.append(QPointF(x, ydecimated[i]))

        if legend_text is not None:
            curve.setName(legend_text)

        # Needed for mouse events on series
        self.chart.setAcceptHoverEvents(True)

        # connect signals / slots
        # curve.clicked.connect(self.lineseries_clicked)
        # curve.hovered.connect(self.lineseries_hovered)

        # Add series
        self.chart.addSeries(curve)
        self.ncurves += 1
        self.update_axes()

    def set_title(self, title):
        print('Setting title: ', title)
        self.chart.setTitle(title)

    def series_to_polyline(self, xdata, ydata):
        """Convert series data to QPolygon(F) polyline

        This code is derived from PythonQwt's function named
        `qwt.plot_curve.series_to_polyline`"""

        # print('series_to_polyline types:', type(xdata[0]), type(ydata[0]))
        size = len(xdata)
        polyline = QPolygonF(size)

        for i in range(0, len(xdata)):
            polyline[i] = QPointF(xdata[i] - xdata[0], ydata[i])

        # pointer = polyline.data()
        # dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        # pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
        # memory = np.frombuffer(pointer, dtype)
        # memory[:(size-1)*2+1:2] = xdata
        # memory[1:(size-1)*2+2:2] = ydata
        return polyline

    def add_test_data(self):

        # 100Hz, one day accelerometer values
        npoints = 1000 * 60 * 24

        xdata = np.linspace(0., 10., npoints)
        self.add_data(xdata, np.sin(xdata), color=Qt.red, legend_text='Acc. X')
        # self.add_data(xdata, np.cos(xdata), color=Qt.green, legend_text='Acc. Y')
        # self.add_data(xdata, np.cos(2 * xdata), color=Qt.blue, legend_text='Acc. Z')
        self.set_title("Simple example with %d curves of %d points " \
                          "(OpenGL Accelerated Series)" \
                          % (self.ncurves, npoints))

    def mouseMoveEvent(self, e: QMouseEvent):
        # Handling rubberbands
        super().mouseMoveEvent(e)

        # Go back to seconds (instead of ms)
        xmap = self.chart.mapToValue(e.pos()).x()
        ymap = self.chart.mapToValue(e.pos()).y()

        self.xTextItem.setText('X: ' + str(datetime.datetime.fromtimestamp(xmap + self.reftime.timestamp())))
        self.yTextItem.setText('Y: ' + str(ymap))

    def mousePressEvent(self, e: QMouseEvent):
        # Handling rubberbands
        super().mousePressEvent(e)

        xmap = self.chart.mapToValue(e.pos()).x()
        ymap = self.chart.mapToValue(e.pos()).y()

        self.cursor.setPos(e.pos())

        pen = self.cursor.pen()
        pen.setColor(Qt.red)
        pen.setWidthF(1.5)
        self.cursor.setPen(pen)
        # On Top
        self.cursor.setZValue(100.0)

        # self.cursor.set
        self.cursor.setLine(e.pos().x(), e.pos().y(), e.pos().x(), e.pos().y() + 1000)
        self.cursor.show()
        pass

    def mouseReleaseEvent(self, e: QMouseEvent):
        # Handling rubberbands
        super().mouseReleaseEvent(e)
        pass

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)

        # self.scene().setSceneRect(0, 0, e.size().width(), e.size().height())
        # Need to reposition X,Y labels
        self.update_x_y_coords()


class OpenIMUBarGraphView(QChartView):
    def __init__(self, parent=None):
        super(QChartView, self).__init__(parent=parent)
        self.chart = QChart()
        self.setChart(self.chart)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.series = QBarSeries(self)
        self.categoryAxis = QBarCategoryAxis(self)

    def set_title(self, title):
        print('Setting title: ', title)
        self.chart.setTitle(title)

    def set_category_axis(self, categories):
        self.categoryAxis.append(categories)

    def add_set(self, label, values):
        print('adding bar set')
        my_set = QBarSet(label, self)
        my_set.append(values)
        self.series.append(my_set)

    def update(self):
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.categoryAxis, self.series)

    def add_test_data(self):
        print('adding test data series')
        self.set_title('Testing bars')
        self.set_category_axis(['A','B','C','D'])
        self.add_set('Test1', [0.1, 2, 3, 4])
        self.add_set('Test2', [3, 2, 1, 4])
        self.add_set('Test3', [4, 1, 3, 2])
        self.update()


# Testing app
if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow, QPushButton
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)

    def create_imu_view():
        window = QMainWindow()
        view = IMUChartView(window)
        view.add_test_data()
        window.setCentralWidget(view)
        window.setWindowTitle("IMUChartView Demo")
        window.resize(640, 480)
        window.show()
        return window

    def create_bar_view():
        window = QMainWindow()
        view = OpenIMUBarGraphView(window)
        view.add_test_data()
        window.setCentralWidget(view)
        window.setWindowTitle("IMUBarGraphView Demo")
        window.resize(640, 480)
        window.show()
        return window


    def create_qwt_chart():
        window = QMainWindow()

        x = np.linspace(-10, 10, 500)
        y1, y2 = np.cos(x), np.sin(x)
        my_plot = QwtPlot("Two curves")
        curve1, curve2 = QwtPlotCurve("Curve 1"), QwtPlotCurve("Curve 2")
        curve1.setData(x, y1)
        curve2.setData(x, y2)
        curve1.attach(my_plot)
        curve2.attach(my_plot)
        my_plot.resize(600, 300)
        my_plot.replot()
        my_plot.show()

        window.setCentralWidget(my_plot)

        window.setWindowTitle("QWT Demo")
        window.resize(640, 480)
        window.show()
        return window

    window = create_qwt_chart()
    # window2 = create_bar_view()

    sys.exit(app.exec_())