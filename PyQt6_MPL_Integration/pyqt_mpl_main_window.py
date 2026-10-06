import sys
from mpl_canvas import PlotCanvas, CanvasSettings
from number_panel import NumberInputPanel
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt MatPlotLib Integration")
        self._build_ui()

    def _build_ui(self):
        self.x_panel = NumberInputPanel("X")
        self.y_panel = NumberInputPanel("Y")
        self.x_axis_config = CanvasSettings("X")
        self.y_axis_config = CanvasSettings("Y")
        self.canvas1 = PlotCanvas()
        # Replot whenever either list changes
        self.x_panel.values_changed.connect(self.update_plot)
        self.y_panel.values_changed.connect(self.update_plot)

        self.x_axis_config.values_changed.connect(self.update_canvas)
        self.y_axis_config.values_changed.connect(self.update_canvas)

        layout = QGridLayout(self)
        layout.addWidget(self.x_panel, 0, 0)
        layout.addWidget(self.x_axis_config, 1, 0)
        layout.addWidget(self.y_panel, 0, 1)
        layout.addWidget(self.y_axis_config, 1, 1)
        layout.setHorizontalSpacing(40)  # Adds spacing between X and Y panels.
        layout.addWidget(self.canvas1, 2, 0, 1, 3)

    def update_plot(self, _values=None):
        x, y = self.x_panel.values, self.y_panel.values
        if x and len(x) == len(y):
            self.canvas1.plot(x, y)

    def update_canvas(self, axis: str, new_label: str):
        self.canvas1.set_labels(axis, new_label)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
