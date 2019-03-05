from PyQt5.QtCore import pyqtSignal


class GraphInteractionMode:
    SELECT = 0
    MOVE = 1


class BaseGraph:
    cursorMoved = pyqtSignal(float)                 # Cursor position (timestamp value)
    selectedAreaChanged = pyqtSignal(float, float)  # Start-timestamp, end-timestamp
    clearedSelectionArea = pyqtSignal()

    def __init__(self, parent=None):
        self.selection_rec = None
        self.interaction_mode = GraphInteractionMode.SELECT
        self.total_samples = 0

    @classmethod
    def setCursorPosition(cls, pos, emit_signal=False):
        return

    @classmethod
    def setCursorPositionFromTime(cls, timestamp, emit_signal=False):
        return

    @classmethod
    def setSelectionArea(cls, start_pos, end_pos, emit_signal=False):
        return

    @classmethod
    def setSelectionAreaFromTime(cls, start_time, end_time, emit_signal=False):
        return

    @classmethod
    def clearSelectionArea(cls, emit_signal=False):
        return

    @classmethod
    def zoom_in(cls):
        return

    @classmethod
    def zoom_out(cls):
        return

    @classmethod
    def zoom_reset(cls):
        return

    @classmethod
    def zoom_area(cls):
        return

    def set_interaction_mode(self, mode = GraphInteractionMode ):
        self.interaction_mode = mode

    @classmethod
    def get_displayed_start_time(cls):
        return None

    @classmethod
    def get_displayed_end_time(cls):
        return None

    @property
    def is_zoomed(self):
        return False


