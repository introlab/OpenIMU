from random import randrange

from PySide6.QtWidgets import QDialog, QWidget, QFrame
from PySide6.QtGui import QMouseEvent, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QBasicTimer

from resources.ui.python.AboutScreen_ui import Ui_AboutScreen


class AboutScreen(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.UI = Ui_AboutScreen()
        self.UI.setupUi(self)
        self.UI.stackedMain.setCurrentIndex(0)

        self.UI.btnOK.clicked.connect(self.accept)

        self.UI.lblAboutTitle.mouseReleaseEvent = self.about_label_mouse_release

    def about_label_mouse_release(self, event: QMouseEvent):
        if event.button() == Qt.RightButton or event.button() == Qt.LeftButton:
            if self.UI.stackedMain.currentIndex() != 1:
                self.UI.stackedMain.setCurrentIndex(1)
                if self.UI.wdgFun.layout().count() > 0:
                    self.UI.wdgFun.layout().removeWidget(self.UI.wdgFun.layout().itemAt(0))
                snake = Snake()
                snake.setFocus()
                self.UI.wdgFun.layout().addWidget(snake)


# Based on https://github.com/mlisbit/pyqt_snake
class Snake(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.score = 0
        self.highscore = 0
        self.lastKeyPress = ""
        self.x = 12
        self.y = 36
        self.lastKeyPress = ''
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x - 12, self.y], [self.x - 24, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.FoodPlaced = False
        self.speed = 100

        self.setFocusPolicy(Qt.StrongFocus)

        self.init_ui()

    def init_ui(self):
        self.new_game()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(300, 300)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.score_board(qp)
        self.place_food(qp)
        self.draw_snake(qp)
        self.score_text(event, qp)
        if self.isOver:
            self.game_over(event, qp)
        elif self.isPaused:
            qp.setPen(QColor(0, 255, 0))
            qp.setFont(QFont('Decorative', 10))
            qp.drawText(event.rect(), Qt.AlignCenter, self.tr('-- PAUSED --'))
        qp.end()

    def keyPressEvent(self, e):
        if not self.isPaused:
            # print "inflection point: ", self.x, " ", self.y
            if e.key() == Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                self.direction("UP")
                self.lastKeyPress = 'UP'
            elif e.key() == Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
                self.direction("DOWN")
                self.lastKeyPress = 'DOWN'
            elif e.key() == Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
                self.direction("LEFT")
                self.lastKeyPress = 'LEFT'
            elif e.key() == Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
                self.direction("RIGHT")
                self.lastKeyPress = 'RIGHT'
            elif e.key() == Qt.Key_P:
                self.pause()
        elif e.key() == Qt.Key_P:
            self.start()
        elif e.key() == Qt.Key_Space:
            self.new_game()
        elif e.key() == Qt.Key_Escape:
            self.close()

    def new_game(self):
        self.score = 0
        self.x = 12
        self.y = 36
        self.lastKeyPress = 'RIGHT'
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x - 12, self.y], [self.x - 24, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = False
        self.isOver = False
        self.FoodPlaced = False
        self.speed = 100
        self.start()

    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    def direction(self, direction):
        if direction == "DOWN" and self.check_status(self.x, self.y + 12):
            self.y += 12
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif direction == "UP" and self.check_status(self.x, self.y - 12):
            self.y -= 12
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif direction == "RIGHT" and self.check_status(self.x + 12, self.y):
            self.x += 12
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif direction == "LEFT" and self.check_status(self.x - 12, self.y):
            self.x -= 12
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])

    def score_board(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(25, 80, 0, 160))
        qp.drawRect(0, 0, 290, 24)

    def score_text(self, event, qp):
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(8, 17, "SCORE: " + str(self.score))
        qp.drawText(195, 17, "HIGHSCORE: " + str(self.highscore))

    def game_over(self, event, qp):
        self.highscore = max(self.highscore, self.score)
        qp.setPen(QColor(255, 0, 0))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.tr("GAME OVER"))
        qp.setFont(QFont('Decorative', 8))
        qp.drawText(80, 170, self.tr("Press 'Space' to play again"))

    def check_status(self, x, y):
        if y > 288 or x > 288 or x < 0 or y < 24:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.y == self.foody and self.x == self.foodx:
            self.FoodPlaced = False
            self.score += 1
            return True
        # elif self.score >= 573:
        #     print("you win!")

        self.snakeArray.pop()

        return True

    # places the food when theres none on the board
    def place_food(self, qp):
        if not self.FoodPlaced:
            self.foodx = randrange(24) * 12
            self.foody = randrange(2, 24) * 12
            if not [self.foodx, self.foody] in self.snakeArray:
                self.FoodPlaced = True
        # qp.setBrush(QColor(80, 180, 0, 160))
        qp.setBrush(Qt.yellow)
        qp.drawRect(self.foodx, self.foody, 12, 12)

    # draws each component of the snake
    def draw_snake(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(255, 80, 0, 255))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], 12, 12)

    # game thread
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.direction(self.lastKeyPress)
            self.repaint()
        else:
            QFrame.timerEvent(self, event)
