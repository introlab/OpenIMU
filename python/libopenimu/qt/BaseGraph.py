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

    def setCursorPosition(self, pos, emit_signal=False):
        return

    def setCursorPositionFromTime(self, timestamp, emit_signal=False):
        return

    def setSelectionArea(self, start_pos, end_pos, emit_signal=False):
        return

    def setSelectionAreaFromTime(self, start_time, end_time, emit_signal=False):
        return

    def clearSelectionArea(self, emit_signal=False):
        return

    def zoom_in(self):
        return

    def zoom_out(self):
        return

    def zoom_reset(self):
        return

    def zoom_area(self):
        return

    def set_interaction_mode(self, mode = GraphInteractionMode ):
        self.interaction_mode = mode

    @property
    def is_zoomed(self):
        return False


