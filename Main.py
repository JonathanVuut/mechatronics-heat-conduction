from Body import Body
from pathlib import Path
import csv
import os

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractSpinBox,
    QApplication,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFrame,
    QFormLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
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
        times = self.main_window.time_history
        if not times:
            return

        selected = self.body_selector.currentText()
        if selected == "Body 1":
            temps = self.main_window.body1_temp_history
            self.axes.plot(times, temps, color="#e74c3c", linewidth=2, label="Body 1")
        else:
            temps = self.main_window.body2_temp_history
            self.axes.plot(times, temps, color="#3498db", linewidth=2, label="Body 2")

        self.axes.set_xlim(0, max(times))
        self.axes.set_ylim(0, 210)
        self.axes.legend(facecolor="#1a1821", edgecolor="#2e293a", labelcolor="#ece6d8")
        self.canvas.draw()

    def clear_graph(self):
        self.axes.clear()
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
        self.canvas.draw()

    def export_csv(self):
        times = self.main_window.time_history
        t1_list = self.main_window.body1_temp_history
        t2_list = self.main_window.body2_temp_history
        if not times:
            return

        file_path = Path(__file__).with_name("heat_transfer_data.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time (s)", "Body 1 Temperature (C)", "Body 2 Temperature (C)"])
            for i in range(len(times)):
                writer.writerow([round(times[i], 2), round(t1_list[i], 4), round(t2_list[i], 4)])

        os.startfile(file_path)


class MaterialWindow(QWidget):
    MATERIALS = (
        ("Copper", 385.00, "$9.20", "Heat exchangers, electrical wiring, busbars"),
        ("Aluminum (6061)", 897.00, "$2.60", "Aerospace frames, heat sinks, automotive parts"),
        ("Carbon Steel", 490.00, "$0.85", "Structural beams, pressure vessels, heavy machinery"),
        ("Stainless Steel (304)", 500.00, "$3.40", "Chemical reactors, food processing, medical tools"),
        ("Cast Iron", 460.00, "$0.75", "Engine blocks, brake rotors, furnace grates"),
        ("Titanium (Ti-6Al-4V)", 526.00, "$35.00", "Turbine blades, aerospace fasteners, implants"),
        ("Brass", 380.00, "$6.50", "Valves, bearings, marine fittings, radiators"),
        ("Industrial Water", 4184.00, "$0.01", "Cooling loops, boilers, thermal energy storage"),
    )

    def __init__(self, main_window, target_body):
        super().__init__(main_window, Qt.WindowType.Window)
        self.main_window = main_window
        self.target_body = target_body
        self.setWindowTitle("The Foundry Archive — Material Codex")
        self.setMinimumSize(760, 440)
        self.resize(1000, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        banner = QFrame()
        banner.setObjectName("codex_banner")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(20, 16, 20, 16)
        banner_layout.setSpacing(6)

        emblem = QLabel("✦  THE FOUNDRY ARCHIVE  ✦")
        emblem.setObjectName("codex_emblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(emblem)

        title = QLabel("Industrial Material Codex")
        title.setObjectName("codex_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(title)

        subtitle = QLabel(
            "Select an alloy or substance to load its thermal capacity into the forge"
        )
        subtitle.setObjectName("codex_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        banner_layout.addWidget(subtitle)
        layout.addWidget(banner)

        self.material_table = QTableWidget(0, 4)
        self.material_table.setObjectName("material_table")
        self.material_table.setHorizontalHeaderLabels(
            (
                "Material",
                "Heat Capacity (J/kg°C)",
                "Price ($/kg)",
                "Industrial Applications",
            )
        )
        self.material_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.material_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.material_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.material_table.setAlternatingRowColors(True)
        self.material_table.setWordWrap(True)
        self.material_table.setShowGrid(False)
        self.material_table.verticalHeader().setVisible(False)
        self.material_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        for material in (*self.MATERIALS, *self.main_window.custom_materials):
            self._append_material_row(material)
        self.material_table.resizeRowsToContents()
        self.material_table.setMinimumHeight(220)
        self.material_table.itemDoubleClicked.connect(self.apply_material)
        layout.addWidget(self.material_table, stretch=1)

        actions = QHBoxLayout()
        actions.addStretch()
        self.custom_material_button = QPushButton("Add Custom Material")
        self.custom_material_button.setObjectName("add_custom_material_button")
        self.custom_material_button.clicked.connect(self.add_custom_material)
        actions.addWidget(self.custom_material_button)

        self.apply_button = QPushButton("Apply Material")
        self.apply_button.setObjectName("apply_material_button")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.apply_material)
        actions.addWidget(self.apply_button)
        layout.addLayout(actions)
        self.material_table.itemSelectionChanged.connect(self._selection_changed)
        if self.main_window.custom_materials:
            self.material_table.selectRow(self.material_table.rowCount() - 1)

    def _append_material_row(self, material, select=False):
        name, heat_capacity, price, applications = material
        row = self.material_table.rowCount()
        self.material_table.insertRow(row)
        values = (name, f"{heat_capacity:.2f}", price, applications)
        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            if column == 1:
                item.setData(Qt.ItemDataRole.UserRole, heat_capacity)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            elif column == 2:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.material_table.setItem(row, column, item)

        self.material_table.resizeRowsToContents()
        if select:
            self.material_table.selectRow(row)
            self.material_table.scrollToItem(self.material_table.item(row, 0))

    def _selection_changed(self):
        self.apply_button.setEnabled(self.material_table.currentRow() >= 0)

    def apply_material(self):
        row = self.material_table.currentRow()
        if row < 0:
            return

        material_name = self.material_table.item(row, 0).text()
        heat_capacity = self.material_table.item(row, 1).data(
            Qt.ItemDataRole.UserRole
        )
        if self.target_body == "left":
            self.main_window.left_heat_capacity_spinbox.setValue(heat_capacity)
            self.main_window.left_heading_label.setText(
                f"BODY 01 / {material_name}"
            )
        else:
            self.main_window.right_heat_capacity_spinbox.setValue(heat_capacity)
            self.main_window.right_heading_label.setText(
                f"BODY 02 / {material_name}"
            )
        self.close()

    def add_custom_material(self):
        dialog = QDialog(self)
        dialog.setObjectName("custom_material_dialog")
        dialog.setWindowTitle("Add Custom Material")
        dialog.setMinimumWidth(520)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        banner = QFrame()
        banner.setObjectName("codex_banner")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(18, 14, 18, 14)
        banner_layout.setSpacing(6)

        emblem = QLabel("✦  FORGE ENTRY  ✦")
        emblem.setObjectName("codex_emblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(emblem)

        title = QLabel("Add a Custom Material")
        title.setObjectName("codex_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(title)
        layout.addWidget(banner)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(14)

        name_input = QLineEdit()
        name_input.setObjectName("custom_material_name")
        name_input.setPlaceholderText("e.g. Nickel Alloy")
        name_label = QLabel("Material Name")
        name_label.setObjectName("custom_field_label")
        form.addRow(name_label, name_input)

        capacity_input = QDoubleSpinBox()
        capacity_input.setObjectName("custom_capacity_spinbox")
        capacity_input.setRange(0.01, 10000.0)
        capacity_input.setValue(500.0)
        capacity_input.setDecimals(2)
        capacity_input.setSuffix(" J/kg°C")
        capacity_label = QLabel("Heat Capacity")
        capacity_label.setObjectName("custom_field_label")
        form.addRow(capacity_label, capacity_input)

        price_input = QDoubleSpinBox()
        price_input.setObjectName("custom_price_spinbox")
        price_input.setRange(0.00, 10000.0)
        price_input.setValue(5.0)
        price_input.setDecimals(2)
        price_input.setPrefix("$")
        price_input.setSuffix(" /kg")
        price_label = QLabel("Price")
        price_label.setObjectName("custom_field_label")
        form.addRow(price_label, price_input)

        applications_input = QLineEdit()
        applications_input.setObjectName("custom_material_applications")
        applications_input.setPlaceholderText("Industrial applications")
        applications_label = QLabel("Industrial Applications")
        applications_label.setObjectName("custom_field_label")
        form.addRow(applications_label, applications_input)
        layout.addLayout(form)

        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancel_custom_material_button")
        cancel_button.clicked.connect(dialog.reject)
        actions.addWidget(cancel_button)

        add_button = QPushButton("Add")
        add_button.setObjectName("add_custom_material_confirm_button")
        add_button.setEnabled(False)
        add_button.clicked.connect(dialog.accept)
        name_input.textChanged.connect(
            lambda name: add_button.setEnabled(bool(name.strip()))
        )
        actions.addWidget(add_button)
        layout.addLayout(actions)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        name = name_input.text().strip()
        if not name:
            return

        material = (
            name,
            capacity_input.value(),
            f"${price_input.value():.2f}",
            applications_input.text().strip(),
        )
        self.main_window.custom_materials.append(material)
        for material_window in self.main_window.material_windows.values():
            if material_window is not self:
                material_window._append_material_row(material, select=True)
        self._append_material_row(material, select=True)


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
        self.pulse_pos = 0.0
        self.custom_materials = []
        self.body1 = None
        self.body2 = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        self.material_windows = {}
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
        self.left_temperature_changed()
        self.right_temperature_changed()

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

        material_button = QPushButton("Select Material")
        material_button.setObjectName("material_button")
        material_button.clicked.connect(lambda: self.open_material_window(side))
        panel_layout.addWidget(material_button)
        if side == "left":
            self.left_heading_label = heading
            self.left_material_button = material_button
        else:
            self.right_heading_label = heading
            self.right_material_button = material_button

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
            self.left_temperature_slider = slider
            self.left_body_box = body_box
            body_row.addWidget(slider)
            body_row.addWidget(body_box, stretch=1)
        else:
            self.right_temperature_slider = slider
            self.right_body_box = body_box
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
            ("heat_capacity", "H. Cap.", 0.01, 10000.0, 0.40, " J/kg°C", False),
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
            if side == "left" and field_name == "temperature":
                self.left_temperature_spinbox = spin_box
            elif side == "left" and field_name == "mass":
                self.left_mass_spinbox = spin_box
            elif side == "left" and field_name == "heat_capacity":
                self.left_heat_capacity_spinbox = spin_box
            elif side == "right" and field_name == "temperature":
                self.right_temperature_spinbox = spin_box
            elif side == "right" and field_name == "mass":
                self.right_mass_spinbox = spin_box
            elif side == "right" and field_name == "heat_capacity":
                self.right_heat_capacity_spinbox = spin_box
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
        self.connector = QFrame()
        self.connector.setObjectName("connector_bar")
        self.connector.setFixedHeight(10)
        connector_layout = QHBoxLayout()
        connector_layout.setContentsMargins(20, 0, 20, 0)
        connector_layout.addWidget(self.connector)
        panel_layout.addLayout(connector_layout)
        panel_layout.addStretch(2)

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        self.start_button.setObjectName("start_button")
        self.start_button.toggled.connect(self.start_stop_button_method)
        panel_layout.addWidget(self.start_button)

        clear_button = QPushButton("Clear")
        clear_button.setObjectName("clear_simulation_button")
        clear_button.clicked.connect(self.clear_simulation)
        panel_layout.addWidget(clear_button)

        graphs_button = QPushButton("Graphs")
        graphs_button.clicked.connect(self.open_graphs)
        panel_layout.addWidget(graphs_button)

        about_button = QPushButton("About")
        about_button.clicked.connect(self.open_about)
        panel_layout.addWidget(about_button)
        return panel

    def clear_simulation(self):
        self.timer.stop()
        self.start_button.setChecked(False)
        self.start_button.setText("Start")
        self.set_inputs_enabled(True)

        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.current_time = 0.0
        self.pulse_pos = 0.0

        self.left_temperature_slider.setValue(200)
        self.left_temperature_spinbox.setValue(200.0)
        self.left_mass_spinbox.setValue(10.0)
        self.left_heat_capacity_spinbox.setValue(0.40)
        self.left_heading_label.setText("BODY 01  /  EMBER")

        self.right_temperature_slider.setValue(0)
        self.right_temperature_spinbox.setValue(0.0)
        self.right_mass_spinbox.setValue(10.0)
        self.right_heat_capacity_spinbox.setValue(0.40)
        self.right_heading_label.setText("BODY 02  /  STEEL")

        self.conductivity_spinbox.setValue(1.00)
        self.body1 = Body(10.0, 0.40, 200.0)
        self.body2 = Body(10.0, 0.40, 0.0)
        self.connector.setStyleSheet("")
        self.graph_window.clear_graph()

    def open_material_window(self, target_body):
        window = self.material_windows.get(target_body)
        if window is None:
            window = MaterialWindow(self, target_body)
            self.material_windows[target_body] = window
        window.show()
        window.raise_()
        window.activateWindow()

    def update_body_color(self, box, temperature):
        red = int((temperature / 200.0) * 255)
        if red > 255:
            red = 255
        if red < 0:
            red = 0
        box.setStyleSheet(f"background-color: rgb({red}, 30, 35);")

    def left_temperature_changed(self):
        temp = self.left_temperature_slider.value()
        self.left_temperature_spinbox.setValue(temp)
        self.update_body_color(self.left_body_box, temp)

    def right_temperature_changed(self):
        temp = self.right_temperature_slider.value()
        self.right_temperature_spinbox.setValue(temp)
        self.update_body_color(self.right_body_box, temp)

    def set_inputs_enabled(self, enabled):
        self.left_temperature_slider.setEnabled(enabled)
        self.right_temperature_slider.setEnabled(enabled)
        self.left_mass_spinbox.setEnabled(enabled)
        self.right_mass_spinbox.setEnabled(enabled)
        self.left_heat_capacity_spinbox.setEnabled(enabled)
        self.right_heat_capacity_spinbox.setEnabled(enabled)
        self.conductivity_spinbox.setEnabled(enabled)
        self.left_material_button.setEnabled(enabled)
        self.right_material_button.setEnabled(enabled)

    def start_stop_button_method(self, checked):
        if checked:
            self.start_button.setText("Stop")
            self.pulse_pos = 0.0
            self.time_history = []
            self.body1_temp_history = []
            self.body2_temp_history = []
            self.current_time = 0.0

            self.body1 = Body(
                self.left_mass_spinbox.value(),
                self.left_heat_capacity_spinbox.value(),
                self.left_temperature_spinbox.value(),
            )
            self.body2 = Body(
                self.right_mass_spinbox.value(),
                self.right_heat_capacity_spinbox.value(),
                self.right_temperature_spinbox.value(),
            )

            self.time_history.append(self.current_time)
            self.body1_temp_history.append(self.body1.temperature)
            self.body2_temp_history.append(self.body2.temperature)

            self.set_inputs_enabled(False)
            self.timer.start(100)
        else:
            self.timer.stop()
            self.start_button.setText("Start")
            self.connector.setStyleSheet("")
            self.set_inputs_enabled(True)

    def timer_method(self):
        dt = 0.1
        conductivity = self.conductivity_spinbox.value()

        i1 = conductivity * (self.body2.temperature - self.body1.temperature)
        i2 = conductivity * (self.body1.temperature - self.body2.temperature)

        q1 = i1 * dt
        q2 = i2 * dt

        t1 = self.body1.add_heat(q1)
        t2 = self.body2.add_heat(q2)

        self.current_time += dt
        self.time_history.append(self.current_time)
        self.body1_temp_history.append(t1)
        self.body2_temp_history.append(t2)

        self.left_temperature_spinbox.setValue(t1)
        self.right_temperature_spinbox.setValue(t2)
        self.left_temperature_slider.blockSignals(True)
        self.left_temperature_slider.setValue(int(round(t1)))
        self.left_temperature_slider.blockSignals(False)
        self.right_temperature_slider.blockSignals(True)
        self.right_temperature_slider.setValue(int(round(t2)))
        self.right_temperature_slider.blockSignals(False)
        self.update_body_color(self.left_body_box, t1)
        self.update_body_color(self.right_body_box, t2)

        temperature_difference = abs(t1 - t2)
        self.pulse_pos = (self.pulse_pos + 0.05) % 1.0
        pulse_position = self.pulse_pos
        trail_start = max(0.0, pulse_position - 0.12)
        trail_end = min(1.0, pulse_position + 0.12)
        opacity = int(min(temperature_difference / 200.0, 1.0) * 255)
        gradient_x1, gradient_x2 = (0, 1) if t1 >= t2 else (1, 0)
        iron_color = "#68616a"
        pulse_color = (
            "#ff7b29"
            if opacity == 255
            else f"rgba(255, 123, 41, {opacity})"
        )
        self.connector.setStyleSheet(
            "QFrame#connector_bar {"
            f"background: qlineargradient(x1: {gradient_x1}, y1: 0, "
            f"x2: {gradient_x2}, y2: 0, stop: 0 {iron_color}, "
            f"stop: {trail_start:.3f} {iron_color}, "
            f"stop: {pulse_position:.3f} {pulse_color}, "
            f"stop: {trail_end:.3f} {iron_color}, "
            f"stop: 1 {iron_color});"
            "border: 1px solid #8b765d;"
            "border-radius: 4px;"
            "}"
        )
        if temperature_difference < 0.05:
            self.start_button.setChecked(False)
    

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
