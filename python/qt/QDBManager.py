from PySide6.QtCore import QObject, Signal

from libopenimu.db.DBManager import DBManager
from libopenimu.models.Group import Group
from libopenimu.models.Participant import Participant


class QDBManager(DBManager, QObject):
    """
    Qt wrapper for DBManager to provide signals
    """

    groupUpdated = Signal(Group)
    participantUpdated = Signal(Participant)

    def __init__(self, filename, overwrite=False, echo=False, newfile=False):
        QObject.__init__(self)
        DBManager.__init__(self, filename, overwrite, echo, newfile)

    def notify_group_update(self, group):
        self.groupUpdated.emit(group)

    def notify_participant_update(self, participant):
        self.participantUpdated.emit(participant)
