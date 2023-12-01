from PySide6.QtWidgets import QTableWidgetItem, QWidget
from PySide6.QtCore import Slot, Signal, Qt

from libopenimu.qt.BaseGraph import BaseGraph
from resources.ui.python.TableDataViewWidget_ui import Ui_tableDataViewWidget
import numpy as np
import json
import datetime


class PromptsView(BaseGraph, QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
        BaseGraph.__init__(self)
        self.UI = Ui_tableDataViewWidget()
        self.UI.setupUi(self)

        self.UI.frameChannels.hide()

        self.question_data = {}
        self.answers = []

        self.UI.tableData.setColumnCount(5)
        self.UI.tableData.setHorizontalHeaderLabels([self.tr('Timestamp'), self.tr('ID'), self.tr('Question'),
                                                     self.tr('Answer(s)'), self.tr('Reply time')])

    def load_question_datas(self, questions: dict):
        # Load question data from settings structure
        questions_json = json.loads(questions)
        if 'prompts' in questions_json:
            for prompt in questions_json['prompts']:
                self.question_data[prompt['id']] = prompt

    def add_answer(self, times: np.ndarray, answer: dict):
        delta = times[1] - times[0]

        answer['delta'] = delta
        answer['timestamp'] = times[0]
        self.answers.append(answer)

    def refresh(self):
        # Sort answers by timestamp
        self.answers = sorted(self.answers, key=lambda item: item['timestamp'])
        self.UI.tableData.clearContents()
        self.UI.tableData.setRowCount(len(self.answers))

        row = 0
        for answer in self.answers:
            item = QTableWidgetItem(str(datetime.datetime.fromtimestamp(answer['timestamp'])))
            item.setBackground(Qt.white)
            self.UI.tableData.setItem(row, 0, item)

            item = QTableWidgetItem(str(answer['question_id']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(Qt.white)
            self.UI.tableData.setItem(row, 1, item)

            question_text = self.question_data[answer['question_id']]['question']
            item = QTableWidgetItem(question_text)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item.setBackground(Qt.white)
            self.UI.tableData.setItem(row, 2, item)

            answer_text = ', '.join(answer['answer_text'])
            item = QTableWidgetItem(answer_text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(Qt.white)
            self.UI.tableData.setItem(row, 3, item)

            item = QTableWidgetItem(str("{:.3f}".format(answer['delta'])))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(Qt.white)
            self.UI.tableData.setItem(row, 4, item)
            row += 1

        self.UI.tableData.resizeColumnsToContents()