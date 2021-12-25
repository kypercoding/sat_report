from PyQt5.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QListView
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from db_management.db import get_sat_data

from frame_switch.window_frame import set_window_frame

import sat_frames.sat_main_frame as sm


class SATEditFrame:
    def __init__(self, window, db_url):
        data = get_sat_data(db_url, window)

        list_view = QListView()

        dates = data['dates']
        composite = data['composite']
        ebrw = data['ebrw']
        math = data['math']

        list_items = []

        list_items.append(QStandardItem("{} | {} | {} | {}".format("Date and time taken", "Composite", "EBRW", "Math")))

        for i in range(len(dates)):
            list_items.append(QStandardItem("{} | {} | {} | {}".format(dates[i], composite[i], ebrw[i], math[i])))
        
        model = QStandardItemModel(list_view)

        for item in list_items:
            model.appendRow(item)
        
        list_view.setModel(model)

        menu_button = QPushButton("Return to SAT Menu")
        menu_button.clicked.connect(lambda: sm.SATMainFrame.switch_to_sat_menu(window, db_url))

        layout = QVBoxLayout()
        layout.addWidget(menu_button)
        layout.addWidget(list_view)

        self._frame = QFrame()
        self._frame.setLayout(layout)

    
    def get_frame(self):
        return self._frame


    @staticmethod
    def switch_to_edit_frame(db_url, window):
        frame = SATEditFrame(window, db_url).get_frame()

        set_window_frame(window, frame, "Delete SAT Entries")
    