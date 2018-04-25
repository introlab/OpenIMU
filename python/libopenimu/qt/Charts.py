# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License
# Copyright (c) 2015 Pierre Raybaut

"""
Simple example illustrating Qt Charts capabilities to plot curves with
a high number of points, using OpenGL accelerated series
"""
from PyQt5.QtGui import QPolygonF, QPainter, QMouseEvent, QResizeEvent
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QLegend, QBarSeries, QBarSet, QBarCategoryAxis, QDateTimeAxis
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPointF, QRectF, QPoint
import numpy as np
import datetime

class IMUChartView(QChartView):
    def __init__(self, parent=None):
        super(QChartView, self).__init__(parent=parent)
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

    def add_data(self, xdata, ydata, color=None, legend_text=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(3.0)
        curve.setPen(pen)

        curve.setUseOpenGL(True)
        curve.append(self.series_to_polyline(xdata, ydata))

        # epoch = datetime.datetime.now()
        # for i in range(0, len(xdata)):
            # curve.append(QPointF(xdata[i], ydata[i]))
            # mytime = datetime.datetime.fromtimestamp(xdata[i])
            # ms = np.int64((mytime - epoch).total_seconds() * 1000.0)
            # curve.append((mytime - epoch).total_seconds(), ydata[i])

        if legend_text is not None:
            curve.setName(legend_text)

        # Needed for mouse events on series
        self.chart.setAcceptHoverEvents(True)

        # connect signals / slots
        curve.clicked.connect(self.lineseries_clicked)
        curve.hovered.connect(self.lineseries_hovered)

        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1

    def tooltip(self):
        pass

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

        self.xTextItem.setText('X: ' + str(self.chart.mapToValue(e.pos()).x()))
        self.yTextItem.setText('Y: ' + str(self.chart.mapToValue(e.pos()).y()))

    def mousePressEvent(self, e: QMouseEvent):
        # Handling rubberbands
        super().mousePressEvent(e)
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
        print('Setting title: ',title)
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
        self.add_set('Test1',[0.1, 2, 3, 4])
        self.add_set('Test2',[3, 2, 1, 4])
        self.add_set('Test3',[4, 1, 3, 2])
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
        window.resize(640,480)
        window.show()
        return window

    def create_bar_view():
        window = QMainWindow()
        view = OpenIMUBarGraphView(window)
        view.add_test_data()
        window.setCentralWidget(view)
        window.setWindowTitle("IMUBarGraphView Demo")
        window.resize(640,480)
        window.show()
        return window

    window1 = create_imu_view()
    # window2 = create_bar_view()

    sys.exit(app.exec_())