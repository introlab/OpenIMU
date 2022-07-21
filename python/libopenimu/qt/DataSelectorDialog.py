from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot
from resources.ui.python.DataSelectorDialog_ui import Ui_DataSelectorDialog

from libopenimu.qt.DataSelector import DataSelector

from libopenimu.db.DBManager import DBManager
from libopenimu.models.Recordset import Recordset


class DataSelectorDialog(QDialog):

    def __init__(self, db_manager: DBManager, allow_only_one_participant=False, show_results=False, parent=None):
        QDialog.__init__(self, parent=parent)
        self.UI = Ui_DataSelectorDialog()
        self.UI.setupUi(self)
        self.data_selector = DataSelector(db_manager=db_manager, allow_only_one_participant=allow_only_one_participant,
                                          show_results=show_results, parent=self)
        self.UI.wdgDataSelector.layout().addWidget(self.data_selector)

        self.dbMan = db_manager
        self.update_buttons_states(False)

        self.UI.btnCancel.clicked.connect(self.cancel_clicked)
        self.UI.btnOK.clicked.connect(self.ok_clicked)
        self.data_selector.dataIsValid.connect(self.on_data_selector_is_valid)

    def update_buttons_states(self, state: bool):
        self.UI.btnOK.setEnabled(state)

    @Slot()
    def cancel_clicked(self):
        self.reject()

    @Slot()
    def ok_clicked(self):
        self.accept()

    @Slot(bool)
    def on_data_selector_is_valid(self, valid: bool):
        self.update_buttons_states(valid)

    def get_selected_recordsets(self) -> list[Recordset]:
        return self.data_selector.get_selected_recordsets()
