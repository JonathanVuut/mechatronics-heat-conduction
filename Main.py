from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QAbstractSpinBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        banner = QFrame()
        banner.setObjectName("emblem_banner")
        banner_layout = QVBoxLayout(banner)
        emblem = QLabel("✦  THE FORGE  ✦")
        emblem.setObjectName("emblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(emblem)
        layout.addWidget(banner)

        title = QLabel("Heat Conduction Simulation")
        title.setObjectName("about_title")
        title.setWordWrap(True)
        layout.addWidget(title)

        details = QVBoxLayout()
        details.setSpacing(10)
        for label_text, value_text in (
            ("STUDENT", "Jonathan Freedman"),
            ("COURSE", "Introduction to Mechatronics"),
        ):
            row = QVBoxLayout()
            label = QLabel(label_text)
            label.setObjectName("eyebrow")
            value = QLabel(value_text)
            value.setObjectName("about_value")
            row.addWidget(label)
            row.addWidget(value)
            details.addLayout(row)
        layout.addLayout(details)

        link = QLabel(
            '<a href="https://github.com/JonathanVuut/mechatronics-heat-conduction">'
            "View project on GitHub</a>"
        )
        link.setObjectName("github_link")
        link.setOpenExternalLinks(True)
        link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        layout.addWidget(link)


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Graph Window")
        self.resize(820, 480)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.figure = Figure(facecolor="#121116")
        self.axes = self.figure.add_subplot(111)
        self.axes.set_facecolor("#121116")
        self.axes.set_xlabel("Time (s)", color="#a39c8e")
        self.axes.set_ylabel("Temperature (°C)", color="#a39c8e")
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self.axes.tick_params(colors="#a39c8e")
        self.axes.grid(color="#2e293a", linewidth=0.7, alpha=0.7)
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        for spine in ("left", "bottom"):
            self.axes.spines[spine].set_color("#5c5365")
        self.figure.tight_layout(pad=2.0)

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch=1)

        controls = QVBoxLayout()
        controls.setSpacing(12)
        controls.addStretch()

        self.body_selector = QComboBox()
        self.body_selector.addItems(["Body 1", "Body 2"])
        controls.addWidget(self.body_selector)

        draw_button = QPushButton("Draw")
        draw_button.clicked.connect(self.draw_graph)
        controls.addWidget(draw_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_graph)
        controls.addWidget(clear_button)

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_csv)
        controls.addWidget(export_button)
        controls.addStretch()
        layout.addLayout(controls)

    def draw_graph(self):
        pass

    def clear_graph(self):
        pass

    def export_csv(self):
        pass


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heat Transfer")
        self.setMinimumSize(960, 580)
        self.resize(1100, 640)
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.current_time = 0.0
        self.body1 = None
        self.body2 = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        header = QVBoxLayout()
        header.setSpacing(4)
        eyebrow = QLabel("THERMAL STUDY  /  MECHATRONICS")
        eyebrow.setObjectName("eyebrow")
        header.addWidget(eyebrow)
        title = QLabel("Heat Conduction")
        title.setObjectName("main_title")
        header.addWidget(title)
        layout.addLayout(header)

        panels = QHBoxLayout()
        panels.setSpacing(24)
        panels.addWidget(
            self._create_body_panel(
                "left",
                "BODY 01  /  EMBER",
                "left_body_box",
                200,
                self.left_temperature_changed,
            ),
            stretch=1,
        )
        panels.addWidget(self._create_center_panel())
        panels.addWidget(
            self._create_body_panel(
                "right",
                "BODY 02  /  STEEL",
                "right_body_box",
                0,
                self.right_temperature_changed,
            ),
            stretch=1,
        )
        layout.addLayout(panels, stretch=1)

    def _create_body_panel(self, side, title, box_name, temperature, on_change):
        panel = QFrame()
        panel.setObjectName("body_card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(22, 22, 22, 22)
        panel_layout.setSpacing(14)

        heading = QLabel(title)
        heading.setObjectName("section_title")
        heading_layout = QHBoxLayout()
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.addWidget(heading)
        panel_layout.addLayout(heading_layout)

        panel_layout.addStretch()

        body_row = QHBoxLayout()
        body_row.setContentsMargins(0, 0, 0, 0)
        body_row.setSpacing(16)

        slider = QSlider(Qt.Orientation.Vertical)
        slider.setObjectName(f"{side}_temperature_slider")
        slider.setRange(0, 200)
        slider.setValue(temperature)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(50)
        slider.setFixedHeight(120)
        slider.valueChanged.connect(on_change)
        body_box = QFrame()
        body_box.setObjectName(box_name)
        body_box.setFixedHeight(120)
        body_box.setMinimumWidth(100)

        if side == "left":
            body_row.addWidget(slider)
            body_row.addWidget(body_box, stretch=1)
        else:
            body_row.addWidget(body_box, stretch=1)
            body_row.addWidget(slider)
        panel_layout.addLayout(body_row)

        panel_layout.addStretch()

        fields_layout = QVBoxLayout()
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(14)

        fields = (
            ("temperature", "Temp.", 0, 200, float(temperature), " °C", True),
            ("mass", "Mass", 0.01, 1000, 10.0, " kg", False),
            ("heat_capacity", "H. Cap.", 0.01, 100, 0.40, " J/kg°C", False),
        )
        for field_name, label_text, minimum, maximum, value, suffix, read_only in fields:
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setObjectName("field_label")
            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f"{side}_{field_name}_spinbox")
            spin_box.setRange(minimum, maximum)
            spin_box.setValue(value)
            spin_box.setSuffix(suffix)
            spin_box.setDecimals(2)
            spin_box.setReadOnly(read_only)
            if read_only:
                spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
                spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin_box.setMinimumWidth(130)
                spin_box.setMinimumHeight(34)
            row.addWidget(label)
            row.addWidget(spin_box, stretch=1)
            fields_layout.addLayout(row)

        panel_layout.addLayout(fields_layout)
        return panel

    def _create_center_panel(self):
        panel = QFrame()
        panel.setObjectName("center_card")
        panel.setMinimumWidth(190)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 22, 0, 22)
        panel_layout.setSpacing(16)

        heading = QLabel("TRANSFER")
        heading.setObjectName("section_title")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(heading)

        conductivity_label = QLabel("Conductivity")
        conductivity_label.setObjectName("field_label")
        conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(conductivity_label)

        self.conductivity_spinbox = QDoubleSpinBox()
        self.conductivity_spinbox.setObjectName("numeric_input")
        self.conductivity_spinbox.setRange(0.01, 100.0)
        self.conductivity_spinbox.setValue(1.0)
        self.conductivity_spinbox.setSuffix(" J/s°C")
        self.conductivity_spinbox.setDecimals(2)
        self.conductivity_spinbox.setMaximumWidth(180)
        panel_layout.addWidget(
            self.conductivity_spinbox,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        panel_layout.addStretch(1)
        connector = QFrame()
        connector.setObjectName("connector_bar")
        connector.setFixedHeight(10)
        connector_layout = QHBoxLayout()
        connector_layout.setContentsMargins(20, 0, 20, 0)
        connector_layout.addWidget(connector)
        panel_layout.addLayout(connector_layout)
        panel_layout.addStretch(2)

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        self.start_button.setObjectName("start_button")
        self.start_button.toggled.connect(self.start_stop_button_method)
        panel_layout.addWidget(self.start_button)

        graphs_button = QPushButton("Graphs")
        graphs_button.clicked.connect(self.open_graphs)
        panel_layout.addWidget(graphs_button)

        about_button = QPushButton("About")
        about_button.clicked.connect(self.open_about)
        panel_layout.addWidget(about_button)
        return panel

    def left_temperature_changed(self):
        pass

    def right_temperature_changed(self):
        pass

    def start_stop_button_method(self, checked):
        pass

    def timer_method(self):
        pass

    def open_graphs(self):
        self.graph_window.show()

    def open_about(self):
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication([])
    stylesheet = Path(__file__).with_name("style.qss").read_text(encoding="utf-8")
    app.setStyleSheet(stylesheet)
    window = HeatTransfer()
    window.show()
    app.exec()
