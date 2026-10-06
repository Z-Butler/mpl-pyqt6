from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QLineEdit, QWidget, QGridLayout, QPushButton

class CanvasSettings(QWidget):

    values_changed = pyqtSignal(str, str)

    def __init__(self, axis: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.axis = axis.title()
        self._build_ui()

    def _build_ui(self):
        self.title_label = QLabel(f"{self.axis} Configuration")
        self.axis_input_label = QLabel(f"{self.axis} Axis Label:")
        self.axis_input = QLineEdit()
        self.axis_input.returnPressed.connect(self.update_canvas)

        self.submit_button = QPushButton(f"Change {self.axis} Axis Label")
        self.submit_button.clicked.connect(self.update_canvas)

        layout = QGridLayout(self)
        layout.addWidget(self.title_label, 0, 0)
        layout.addWidget(self.axis_input_label, 1, 0)
        layout.addWidget(self.axis_input, 1, 1)
        layout.addWidget(self.submit_button, 1, 2)

    def update_canvas(self):
        new_label = str(self.axis_input.text())
        self.values_changed.emit(self.axis, new_label)
        self.axis_input.clear()



class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, x_axis: str = "X", y_axis: str = "Y"):
        self.x_axis = x_axis
        self.y_axis = y_axis
        fig = Figure()
        self.axes = fig.add_subplot()
        super().__init__(fig)
        self.setParent(parent)

    def plot(self, x, y):
        self.axes.clear()
        self.axes.plot(x, y, marker="o")
        self.axes.set_xlabel(xlabel=self.x_axis)
        self.axes.set_ylabel(ylabel=self.y_axis)
        self.draw()

    def set_labels(self, axis: str, new_label: str):
        if axis == "X":
            self.x_axis = new_label
            self.axes.set_xlabel(self.x_axis)
        elif axis == "Y":
            self.y_axis = new_label
            self.axes.set_ylabel(self.y_axis)
        self.draw()

