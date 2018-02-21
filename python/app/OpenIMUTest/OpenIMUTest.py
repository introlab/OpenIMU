from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Charts import IMUChartView
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent=parent)
        self.centralWidget = QWidget(self)
        self.centralLayout = QVBoxLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)

        # Testing chart
        self.chartView = None
        self.add_chart_view(test_data=True)

        self.resize(640,480)
        self.show()

    def add_chart_view(self, test_data=False):
        self.chartView = IMUChartView(self.centralWidget)
        self.centralLayout.addWidget(self.chartView)
        if test_data is True:
            self.chartView.add_test_data()


# Main
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())