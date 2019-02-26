from PyQt5.QtGui import QPolygonF, QPainter, QMouseEvent, QResizeEvent, QBrush, QColor, QPen, QGuiApplication
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarSeries, QBarSet
from PyQt5.QtChart import QDateTimeAxis, QValueAxis, QBarCategoryAxis
from PyQt5.QtWidgets import QGraphicsLineItem, QLabel, QOpenGLWidget, QRubberBand
from PyQt5.QtCore import Qt, pyqtSlot, QPointF, QRect, QPoint

from libopenimu.qt.BaseGraph import BaseGraph, GraphInteractionMode

import numpy as np
import datetime


class IMUChartView(QChartView, BaseGraph):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.cursor = QGraphicsLineItem()
        self.scene().addItem(self.cursor)

        self.xvalues = {}

        self.chart = QChart()
        self.setChart(self.chart)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)
        self.ncurves = 0
        self.setRenderHint(QPainter.Antialiasing)

        # Selection features
        # self.setRubberBand(QChartView.HorizontalRubberBand)
        self.selectionBand = QRubberBand(QRubberBand.Rectangle, self)
        self.selecting = False
        self.initialClick = QPoint()

        # Track mouse
        self.setMouseTracking(True)

        self.labelValue = QLabel(self)
        self.labelValue.setStyleSheet("background-color: rgba(255,255,255,75%); color: black;")
        self.labelValue.setAlignment(Qt.AlignCenter)
        self.labelValue.setMargin(5)
        self.labelValue.setVisible(False)

        self.build_style()

    def build_style(self):
        self.setStyleSheet("QLabel{color:blue;}")
        self.chart.setTheme(QChart.ChartThemeBlueCerulean)
        self.setBackgroundBrush(QBrush(Qt.darkGray))
        self.chart.setPlotAreaBackgroundBrush(QBrush(Qt.black))
        self.chart.setPlotAreaBackgroundVisible(True)

    def save_as_png(self, file_path):
        pixmap = self.grab()

        child = self.findChild(QOpenGLWidget)

        painter = QPainter(pixmap)
        if child is not None:
            d = child.mapToGlobal(QPoint()) - self.mapToGlobal(QPoint())
            painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
            painter.drawImage(d, child.grabFramebuffer())

        painter.end()
        pixmap.save(file_path, 'PNG')

    #  def closeEvent(self, event):
    #     self.aboutToClose.emit(self)

    @staticmethod
    def decimate(xdata, ydata):
        # assert(len(xdata) == len(ydata))

        # Decimate only if we have too much data
        decimate_factor = len(xdata) / 100000.0
        # decimate_factor = 1.0

        if decimate_factor > 1.0:
            decimate_factor = int(np.floor(decimate_factor))
            # print('decimate factor', decimate_factor)

            x = np.ndarray(int(len(xdata) / decimate_factor), dtype=np.float64)
            y = np.ndarray(int(len(ydata) / decimate_factor), dtype=np.float64)
            # for i in range(len(x)):
            for i, _ in enumerate(x):
                index = i * decimate_factor
                # assert(index < len(xdata))
                x[i] = xdata[index]
                y[i] = ydata[index]
                if x[i] < x[0]:
                    print('timestamp error', x[i], x[0])
            return x, y
        else:
            return xdata, ydata

    @pyqtSlot(float, float)
    def axis_range_changed(self, min_value, max_value):
        # print('axis_range_changed', min, max)
        for axis in self.chart.axes():
            axis.applyNiceNumbers()

    def update_axes(self):

        # Get and remove all axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Create new axes
        # Create axis X
        axisx = QDateTimeAxis()
        axisx.setTickCount(5)
        axisx.setFormat("dd MMM yyyy hh:mm:ss")
        axisx.setTitleText("Date")
        self.chart.addAxis(axisx, Qt.AlignBottom)

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
            series.attachAxis(axisx)
            series.attachAxis(axisY)
            vect = series.pointsVector()
            # for i in range(len(vect)):
            for i, _ in enumerate(vect):
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
        # axisx.applyNiceNumbers()
        # axisY.applyNiceNumbers()

    def add_data(self, xdata, ydata, color=None, legend_text=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(1.5)
        curve.setPen(pen)
        # curve.setPointsVisible(True)
        # curve.setUseOpenGL(True)
        self.total_samples = max(self.total_samples, len(xdata))

        # Decimate
        xdecimated, ydecimated = self.decimate(xdata, ydata)

        # Data must be in ms since epoch
        # curve.append(self.series_to_polyline(xdecimated * 1000.0, ydecimated))
        # self.reftime = datetime.datetime.fromtimestamp(xdecimated[0])

        # if len(xdecimated) > 0:
        #    xdecimated = xdecimated - xdecimated[0]

        xdecimated *= 1000  # No decimal expected
        points = []
        for i, _ in enumerate(xdecimated):
            # TODO hack
            # curve.append(QPointF(xdecimated[i], ydecimated[i]))
            points.append(QPointF(xdecimated[i], ydecimated[i]))

        curve.replace(points)
        points.clear()

        if legend_text is not None:
            curve.setName(legend_text)

        # Needed for mouse events on series
        self.chart.setAcceptHoverEvents(True)
        self.xvalues[self.ncurves] = np.array(xdecimated)

        # connect signals / slots
        # curve.clicked.connect(self.lineseries_clicked)
        # curve.hovered.connect(self.lineseries_hovered)

        # Add series
        self.chart.addSeries(curve)
        self.ncurves += 1
        self.update_axes()

    def update_data(self, xdata, ydata, series_id):
        if series_id < len(self.chart.series()):
            # Find start time to replace data
            current_series = self.chart.series()[series_id]
            current_points = current_series.pointsVector()

            # Find start and end indexes
            start_index = -1
            try:
                start_index = current_points.index(QPointF(xdata[0]*1000, ydata[0]))  # Right on the value!
                # print("update_data: start_index found exact match.")
            except ValueError:
                # print("update_data: start_index no exact match - scanning deeper...")
                for i, value in enumerate(current_points):
                    # print(str(current_points[i].x()) + " == " + str(xdata[0]*1000))
                    if current_points[i].x() == xdata[0]*1000 or (i > 0 and current_points[i - 1].x() < xdata[0]*1000
                                                             < current_points[i].x()):
                        start_index = i
                        # print("update_data: start_index found approximative match.")
                        break

            end_index = -1
            try:
                end_index = current_points.index(QPointF(xdata[len(xdata)-1] * 1000, ydata[len(ydata)-1]))  # Right on!
                # print("update_data: start_index found exact match.")
            except ValueError:
                # print("update_data: start_index no exact match - scanning deeper...")
                for i, value in enumerate(current_points):
                    # print(str(current_points[i].x()) + " == " + str(xdata[0]*1000))
                    if current_points[i].x() == xdata[len(xdata)-1] * 1000 or (
                            i > 0 and current_points[i - 1].x() < xdata[len(xdata)-1] * 1000
                            < current_points[i].x()):
                        end_index = i
                        # print("update_data: start_index found approximative match.")
                        break

            if start_index < 0 or end_index < 0:
                return

            # Decimate, if needed
            xdata, ydata = self.decimate(xdata, ydata)

            # Check if we have the same number of points for that range. If not, remove and replace!
            target_points = current_points[start_index:end_index]
            if len(target_points) != len(xdata):
                points = []
                for i, value in enumerate(xdata):
                    # TODO improve
                    points.append(QPointF(value*1000, ydata[i]))

                new_points = current_points[0:start_index] + points[0:len(points)-1] + \
                             current_points[end_index:len(current_points)-1]

                current_series.replace(new_points)
                new_points.clear()

                # self.xvalues[series_id] = np.array(xdata)

        return

    @classmethod
    def set_title(cls, title):
        # print('Setting title: ', title)
        # self.chart.setTitle(title)
        return

    @staticmethod
    def series_to_polyline(xdata, ydata):
        """Convert series data to QPolygon(F) polyline

        This code is derived from PythonQwt's function named
        `qwt.plot_curve.series_to_polyline`"""

        # print('series_to_polyline types:', type(xdata[0]), type(ydata[0]))
        size = len(xdata)
        polyline = QPolygonF(size)

        # for i in range(0, len(xdata)):
        #   polyline[i] = QPointF(xdata[i] - xdata[0], ydata[i])
        for i, data in enumerate(xdata):
            polyline[i] = QPointF(data - xdata[0], ydata[i])

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
        self.set_title("Simple example with %d curves of %d points (OpenGL Accelerated Series)"
                        % (self.ncurves, npoints))

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.selecting:
            current_pos = e.pos()
            if self.interaction_mode == GraphInteractionMode.SELECT:
                if current_pos.x() < self.initialClick.x():
                    start_x = current_pos.x()
                    width = self.initialClick.x() - start_x
                else:
                    start_x = self.initialClick.x()
                    width = current_pos.x() - self.initialClick.x()
                self.selectionBand.setGeometry(QRect(start_x, self.chart.plotArea().y(), width, self.chart.plotArea().height()))
            if self.interaction_mode == GraphInteractionMode.MOVE:
                new_pos = current_pos - self.initialClick
                self.chart.scroll(-new_pos.x(), new_pos.y())
                self.initialClick = current_pos

    def mousePressEvent(self, e: QMouseEvent):
        # Handling rubberbands
        # super().mousePressEvent(e)
        self.selecting = True
        self.initialClick = e.pos()
        if self.interaction_mode == GraphInteractionMode.SELECT:
            self.selectionBand.setGeometry(QRect(self.initialClick.x(), self.chart.plotArea().y(), 1,
                                             self.chart.plotArea().height()))
            self.selectionBand.show()

        if self.interaction_mode == GraphInteractionMode.MOVE:
            QGuiApplication.setOverrideCursor(Qt.ClosedHandCursor)
            self.labelValue.setVisible(False)

    def mouseReleaseEvent(self, e: QMouseEvent):
        # Handling rubberbands
        clicked_x = self.mapToScene(e.pos()).x()

        if self.interaction_mode == GraphInteractionMode.SELECT:
            self.selectionBand.hide()
            if clicked_x == self.mapToScene(self.initialClick).x():
                self.setCursorPosition(clicked_x, True)
            else:
                mapped_x = self.mapToScene(self.initialClick).x()
                if self.initialClick.x() < clicked_x:
                    self.setSelectionArea(mapped_x, clicked_x, True)
                else:
                    self.setSelectionArea(clicked_x, mapped_x, True)

        if self.interaction_mode == GraphInteractionMode.MOVE:
            QGuiApplication.restoreOverrideCursor()

        self.selecting = False

    def clearSelectionArea(self, emit_signal = False):
        self.scene().removeItem(self.selection_rec)
        self.selection_rec = None

        if emit_signal:
            self.clearedSelectionArea.emit()

    def setSelectionArea(self, start_pos, end_pos, emit_signal=False):
        selection_brush = QBrush(QColor(153, 204, 255, 128))
        selection_pen = QPen(Qt.transparent)
        self.scene().removeItem(self.selection_rec)
        self.selection_rec = self.scene().addRect(start_pos, self.chart.plotArea().y(), end_pos - start_pos,
                                                  self.chart.plotArea().height(), selection_pen,
                                                  selection_brush)
        if emit_signal:
            self.selectedAreaChanged.emit(self.chart.mapToValue(QPointF(start_pos, 0)).x(),
                                          self.chart.mapToValue(QPointF(end_pos, 0)).x())

    def setSelectionAreaFromTime(self, start_time, end_time, emit_signal = False):
        # Convert times to x values
        if isinstance(start_time, datetime.datetime):
            start_time = start_time.timestamp()*1000
        if isinstance(end_time, datetime.datetime):
            end_time = end_time.timestamp()*1000

        start_pos = self.chart.mapToPosition(QPointF(start_time, 0)).x()
        end_pos = self.chart.mapToPosition(QPointF(end_time, 0)).x()

        self.setSelectionArea(start_pos, end_pos)

    def setCursorPosition(self, pos, emit_signal=False):
        # print (pos)
        pen = self.cursor.pen()
        pen.setColor(Qt.cyan)
        pen.setWidthF(1.0)
        self.cursor.setPen(pen)
        # On Top
        self.cursor.setZValue(100.0)

        area = self.chart.plotArea()
        x = pos
        y1 = area.y()
        y2 = area.y() + area.height()

        # self.cursor.set
        self.cursor.setLine(x, y1, x, y2)
        self.cursor.show()

        xmap_initial = self.chart.mapToValue(QPointF(pos, 0)).x()
        display = ''
        # '<i>' + (datetime.datetime.fromtimestamp(xmap + self.reftime.timestamp())).strftime('%d-%m-%Y %H:%M:%S') +
        # '</i><br />'
        ypos = 10
        last_val = None
        for i in range(self.ncurves):
            # Find nearest point
            idx = (np.abs(self.xvalues[i] - xmap_initial)).argmin()
            ymap = self.chart.series()[i].at(idx).y()
            xmap = self.chart.series()[i].at(idx).x()
            if i == 0:
                display += "<i>" + (datetime.datetime.fromtimestamp(xmap_initial/1000)).strftime('%d-%m-%Y %H:%M:%S:%f') + \
                           "</i>"

            # Compute where to display label
            if last_val is None or ymap > last_val:
                last_val = ymap
                ypos = self.chart.mapToPosition(QPointF(xmap, ymap)).y()
            if display != '':
                display += '<br />'

            display += self.chart.series()[i].name() + ': <b>' + '%.3f' % ymap + '</b>'

        self.labelValue.setText(display)
        self.labelValue.setGeometry(pos, ypos, 100, 100)
        self.labelValue.adjustSize()
        self.labelValue.setVisible(True)

        if emit_signal:
            self.cursorMoved.emit(xmap_initial)

        self.update()

    def setCursorPositionFromTime(self, timestamp, emit_signal=False):
        # Find nearest point
        if isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.timestamp()
        pos = self.get_pos_from_time(timestamp)
        self.setCursorPosition(pos, emit_signal)

    def get_pos_from_time(self, timestamp):
        px = timestamp
        idx1 = (np.abs(self.xvalues[0] - px)).argmin()
        x1 = self.chart.series()[0].at(idx1).x()
        pos1 = self.chart.mapToPosition(QPointF(x1, 0)).x()
        idx2 = idx1 + 1
        if idx2 < len(self.chart.series()[0]):
            x2 = self.chart.series()[0].at(idx2).x()
            pos2 = self.chart.mapToPosition(QPointF(x2, 0)).x()
            x2 /= 1000
            x1 /= 1000
            pos = (((px - x1) / (x2 - x1)) * (pos2 - pos1)) + pos1
        else:
            pos = pos1
        return pos

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)

        # Update cursor height
        area = self.chart.plotArea()
        line = self.cursor.line()
        self.cursor.setLine(line.x1(), area.y(), line.x2(), area.y() + area.height())

    def zoom_in(self):
        self.chart.zoomIn()

    def zoom_out(self):
        self.chart.zoomOut()

    def zoom_area(self):
        if self.selection_rec:
            zoom_rec = self.selection_rec.rect()
            zoom_rec.setY(0)
            zoom_rec.setHeight(self.chart.plotArea().height())
            self.chart.zoomIn(zoom_rec)
            self.clearSelectionArea(True)

    def zoom_reset(self):
        self.chart.zoomReset()

    def get_displayed_start_time(self):
        min_x = self.chart.mapToScene(self.chart.plotArea()).boundingRect().x()
        xmap = self.chart.mapToValue(QPointF(min_x, 0)).x()
        return datetime.datetime.fromtimestamp(xmap/1000)

    def get_displayed_end_time(self):
        max_x = self.chart.mapToScene(self.chart.plotArea()).boundingRect().x()
        max_x += self.chart.mapToScene(self.chart.plotArea()).boundingRect().width()
        xmap = self.chart.mapToValue(QPointF(max_x, 0)).x()
        return datetime.datetime.fromtimestamp(xmap / 1000)

    @property
    def is_zoomed(self):
        return self.chart.isZoomed()


class OpenIMUBarGraphView(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.chart = QChart()
        self.setChart(self.chart)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.series = QBarSeries(self)
        self.categoryAxis = QBarCategoryAxis(self)
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)

    def set_title(self, title):
        # print('Setting title: ', title)
        self.chart.setTitle(title)

    def set_category_axis(self, categories):
        self.categoryAxis.append(categories)

    def add_set(self, label, values):
        # print('adding bar set')
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
    from PyQt5.QtWidgets import QMainWindow
    # from PyQt5.QtCore import Qt

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

    window = create_imu_view()
    # window2 = create_bar_view()

    sys.exit(app.exec_())
