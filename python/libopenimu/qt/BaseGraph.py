from PySide6.QtCore import Signal


class GraphInteractionMode:
    SELECT = 0
    MOVE = 1


class BaseGraph:
    cursorMoved = Signal(float)                 # Cursor position (timestamp value)
    selectedAreaChanged = Signal(float, float)  # Start-timestamp, end-timestamp
    clearedSelectionArea = Signal()

    def __init__(self, parent=None):
        super().__init__()
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


