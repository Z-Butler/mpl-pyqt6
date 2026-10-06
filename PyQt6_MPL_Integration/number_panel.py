from itertools import batched
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QGridLayout

class NumberInputPanel(QWidget):
    """Reusable panel for collecting a list of numbers for one variable."""

    values_changed = pyqtSignal(list)

    def __init__(self, name: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.name = name
        self.values: list[float] = []
        self._build_ui()
        self.show_values()

    def _build_ui(self):
        self.title_label = QLabel(f"{self.name} variable configuration:")
        self.input_label = QLabel(f"Add {self.name.lower()} value:")

        self.input = QLineEdit()
        self.input.setFixedWidth(145)
        self.input.setPlaceholderText("Please enter a number")
        self.input.returnPressed.connect(self.add_value)

        self.status_label = QLabel("")
        self.display_label = QLabel("")

        self.submit_button = QPushButton(f"Submit {self.name.lower()} value")
        self.submit_button.setFixedWidth(145)
        self.submit_button.clicked.connect(self.add_value)

        self.clear_button = QPushButton(f"Clear {self.name.lower()} values")
        self.clear_button.clicked.connect(self.clear_values)

        self.remove_value_button = QPushButton(f"Remove {self.name.lower()} value")
        self.remove_value_button.setFixedWidth(145)
        self.remove_value_button.clicked.connect(self.remove_value)

        # User Interactive Layout
        input_grid = QGridLayout()
        input_grid.setContentsMargins(0, 0, 0, 0)
        input_grid.addWidget(self.title_label, 0, 0, 1, 2)
        input_grid.addWidget(self.input_label, 1, 0)
        input_grid.addWidget(self.input, 1, 1)
        input_grid.addWidget(self.status_label, 2, 0, 1, 2)
        input_grid.addWidget(self.submit_button, 3, 0)
        input_grid.addWidget(self.remove_value_button, 3, 1)
        input_grid.addWidget(self.clear_button, 4, 0, 1, 2)
        input_grid.setRowStretch(5, 1)

        # List View Layout
        display_grid = QGridLayout()
        display_grid.setContentsMargins(0, 0, 0, 0)
        display_grid.addWidget(
            self.display_label, 0, 0, Qt.AlignmentFlag.AlignTop
        )
        display_grid.setRowStretch(1, 1)
        display_grid.setColumnStretch(0, 1)

        # Root Layout
        root = QGridLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addLayout(input_grid, 0, 0)
        root.addLayout(display_grid, 0, 1)
        root.setColumnStretch(1, 1)

    def add_value(self):
        """Handle a submit: parse, store, then refresh the UI."""
        try:
            value = float(self.input.text())
        except ValueError:
            self.show_error("Error: Enter a valid number")
        else:
            self.values.append(value)
            self.status_label.setText(f"Added {value}")
            self.show_values()
            self.values_changed.emit(self.values)
        finally:
            self.input.clear()

    def remove_value(self):
        """Handle a submit: remove the value from the list."""
        try:
            position_str, value_str = self.input.text().split(", ")
            position = int(position_str)
            value = float(value_str)
        except ValueError:
            self.show_error("Enter 'position, value'")
        else:
            if 0 <= position < len(self.values) and self.values[position] == value:
                del self.values[position]
                self.status_label.setText(f"Removed {value} at position {position}")
                self.show_values()
                self.values_changed.emit(self.values)
            else:
                self.show_error("Value not found at position")
        finally:
            self.input.clear()

    def show_values(self):
        pairs = [str(p) for p in enumerate(iterable=self.values)]

        lines = []
        for chunk in batched(iterable=pairs, n=5):
            lines.append(", ".join(chunk))

        self.display_label.setText(
            f"({len(self.values)}) {self.name} variables: \n" + "\n".join(lines)
        )

    def show_error(self, message: str):
        self.status_label.setText(message)

    def clear_values(self):
        if not self.values:
            self.status_label.setText("No values to clear")
            return
        self.status_label.setText(f"Cleared {len(self.values)} values")
        self.values = []
        self.show_values()
        self.values_changed.emit(self.values)
