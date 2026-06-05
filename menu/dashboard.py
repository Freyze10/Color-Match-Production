import pandas as pd
import numpy as np

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSizePolicy, QTableView)
from PyQt6.QtCore import Qt, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

import qtawesome as fa
from css.styles import AppStyles
from table_model.model import TableModel


# ── Resolved color constants ─────────────────────────────────────────────────
_CARD_BG    = "#FFFFFF"
_CHART_CYAN = AppStyles.TEAL_500   # #14B8A6
_CHART_DARK = AppStyles.SLATE_500  # #64748B
_TEXT_LIGHT = AppStyles.SLATE_400  # #94A3B8
_TEXT_BODY  = AppStyles.TEXT_PRIMARY  # #0F172A


class MplCanvas(FigureCanvas):
    """Bridge between Matplotlib and PyQt6 — styled to match AppStyles white cards."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.fig.patch.set_facecolor(_CARD_BG)
        self.axes.set_facecolor(_CARD_BG)

        super().__init__(self.fig)


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(AppStyles.DASHBOARD_STYLESHEET)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # ── TOP SECTION: SUMMARY HIGHLIGHT ──────────────────────────────────
        top_card = QFrame()
        top_card.setObjectName("DashboardCard")
        top_card.setFixedHeight(110)
        top_layout = QHBoxLayout(top_card)

        v_box = QVBoxLayout()
        v_box.setSpacing(4)

        title = QLabel("Completed Samples This Week")
        title.setObjectName("DashTitle")

        val_box = QHBoxLayout()
        val_box.setSpacing(6)
        samples_val = QLabel("34")
        samples_val.setObjectName("DashValue")

        samples_text = QLabel("samples")
        samples_text.setObjectName("DashSubText")
        samples_text.setAlignment(Qt.AlignmentFlag.AlignBottom)

        val_box.addWidget(samples_val)
        val_box.addWidget(samples_text)
        val_box.addStretch()

        v_box.addWidget(title)
        v_box.addLayout(val_box)

        top_layout.addLayout(v_box)
        top_layout.addStretch()

        self.indicator_percent = 12
        trend_label = QLabel(f"↑ {self.indicator_percent}% from last week")
        trend_label.setObjectName("DashTrend")
        top_layout.addWidget(trend_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.main_layout.addWidget(top_card)

        # ── MIDDLE SECTION: ANALYTICS ────────────────────────────────────────
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)

        rematch_container = self._create_card("Monthly Rematches")
        self.bar_canvas = MplCanvas(self)
        rematch_container.layout().addWidget(self.bar_canvas)
        self.plot_horizontal_bar()

        donut_container = self._create_card("Sample vs Order Generated")
        self.donut_canvas = MplCanvas(self)
        donut_container.layout().addWidget(self.donut_canvas)
        self.plot_donut_chart()

        charts_layout.addWidget(rematch_container, stretch=2)
        charts_layout.addWidget(donut_container, stretch=1)
        self.main_layout.addLayout(charts_layout, stretch=3)

        # ── BOTTOM SECTION: TABLE & STATS ────────────────────────────────────
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)

        table_card = self._create_card("Recent Matches Record")
        self.table_headers = ["Employee", "Matched", "Rematches", "Success %"]
        self.table_data = [
            ["Person 1", "60", "15", "75%"],
            ["Person 2", "45", "5",  "88%"],
            ["Person 3", "30", "12", "60%"],
        ]

        self.table_view = QTableView()
        self.table_view.setObjectName("DashTable")
        self.table_model = TableModel(self.table_data, self.table_headers)
        self.table_view.setModel(self.table_model)

        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setShowGrid(False)

        table_card.layout().addWidget(self.table_view)
        bottom_layout.addWidget(table_card, stretch=3)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        self.pending_card, self.lbl_pending_val = self._create_stat_card(
            "Pending Samples", "32", "fa5s.clock")
        self.conv_card, self.lbl_conv_val = self._create_stat_card(
            "Conversion Rate", "77%", "fa5s.percentage")

        sidebar.addWidget(self.pending_card)
        sidebar.addWidget(self.conv_card)
        bottom_layout.addLayout(sidebar, stretch=1)

        self.main_layout.addLayout(bottom_layout, stretch=2)

    # ── HELPERS ──────────────────────────────────────────────────────────────

    def _create_card(self, title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("DashboardCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        lbl = QLabel(title)
        lbl.setObjectName("DashTitle")
        layout.addWidget(lbl)
        return card

    def _create_stat_card(self, title: str, val: str, icon_name: str):
        card = self._create_card(title)
        row = QHBoxLayout()
        row.setSpacing(8)

        value_lbl = QLabel(val)
        value_lbl.setObjectName("DashValue")

        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            fa.icon(icon_name, color=AppStyles.TEAL_500).pixmap(QSize(28, 28))
        )
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        row.addWidget(value_lbl)
        row.addStretch()
        row.addWidget(icon_lbl)
        card.layout().addLayout(row)
        return card, value_lbl

    # ── PLOTTING ─────────────────────────────────────────────────────────────

    def plot_horizontal_bar(self):
        df = pd.DataFrame({
            "Month":   ["Jan", "Feb", "Mar", "Apr", "May"],
            "Samples": [34, 72, 103, 64, 34],
        })

        ax = self.bar_canvas.axes
        ax.clear()

        sns.barplot(x="Samples", y="Month", data=df, ax=ax, color=_CHART_CYAN)

        ax.set_title("Monthly Rematches",
                     color=_TEXT_BODY, fontsize=10, fontweight="bold", pad=8)
        ax.tick_params(colors=_TEXT_LIGHT, labelsize=9)
        ax.set_xlabel("Total Rematch", color=_TEXT_LIGHT, fontsize=8)
        ax.set_ylabel("", color=_TEXT_LIGHT)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="x", color=_TEXT_LIGHT, linestyle="--", alpha=0.15)
        self.bar_canvas.draw()

    def plot_donut_chart(self):
        # Data: (label, value, color)
        self._donut_data = [
            ("Samples", 65.7, _CHART_CYAN),
            ("Orders",  34.3, _CHART_DARK),
        ]
        sizes  = [d[1] for d in self._donut_data]
        colors = [d[2] for d in self._donut_data]

        ax = self.donut_canvas.axes
        ax.clear()

        # Reserve space at the bottom for the legend row
        self.donut_canvas.fig.subplots_adjust(
            top=0.92, bottom=0.24, left=0.05, right=0.95)

        ax.pie(
            sizes,
            startangle=90,
            colors=colors,
            wedgeprops={"width": 0.42, "edgecolor": _CARD_BG, "linewidth": 2},
        )

        # Center text: percentage + label of the primary slice
        ax.text(0,  0.10, f"{sizes[0]:.1f}%",
                ha="center", va="center",
                fontsize=13, fontweight="bold", color=_TEXT_BODY)
        ax.text(0, -0.16, self._donut_data[0][0],
                ha="center", va="center",
                fontsize=9, color=_TEXT_LIGHT)

        ax.axis("equal")

        # ── Bottom legend: stacked vertically, right-aligned ────────────────
        # dot_x / text_x in figure coords (0=left, 1=right)
        dot_x  = 0.10   # dot sits ~10% across — leaves a tight left margin
        text_x = 0.15   # label text starts just right of the dot
        y_top  = 0.17   # y of first item
        y_step = 0.09   # gap between items

        for i, (lbl, pct, clr) in enumerate(self._donut_data):
            y = y_top - i * y_step

            self.donut_canvas.fig.text(
                dot_x, y, "●",
                ha="center", va="center",
                fontsize=10, color=clr,
            )
            self.donut_canvas.fig.text(
                text_x, y, f"{lbl} — {pct:.1f}%",
                ha="left", va="center",
                fontsize=9, color=_TEXT_BODY,
            )

        self.donut_canvas.draw()

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def refresh_stats(self, pending_val, conversion_val):
        """Update sidebar KPI values dynamically."""
        self.lbl_pending_val.setText(str(pending_val))
        self.lbl_conv_val.setText(str(conversion_val))
