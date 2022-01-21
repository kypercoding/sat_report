from PyQt5.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QListWidget
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from db_management.db import delete_sat, get_sat_data

from frame_switch.window_frame import set_window_frame

import sat_frames.sat_main_frame as sm


def reset_list(list_view, db_url, window):
    list_view.clear()

    data = get_sat_data(db_url, window)

    dates = data['dates']
    composite = data['composite']
    ebrw = data['ebrw']
    math = data['math']

    for i in range(len(dates)):
        list_view.addItem("{} | {} | {} | {}".format(dates[i], composite[i], ebrw[i], math[i]))


def delete_sat_record(list_view, db_url, window):
    if list_view.currentItem() is None:
        return

    item = list_view.currentItem()
    date = item.text().split(" | ")[0]

    delete_sat(db_url, window, date)

    reset_list(list_view, db_url, window)


class SATEditFrame:
    def __init__(self, window, db_url):
        list_view = QListWidget()

        reset_list(list_view, db_url, window)

        headers = QLabel("{} | {} | {} | {}".format("Date and time taken", "Composite", "EBRW", "Math"))

        menu_button = QPushButton("Return to SAT Menu")
        menu_button.clicked.connect(lambda: sm.SATMainFrame.switch_to_sat_menu(window, db_url))

        delete_button = QPushButton("Delete SAT")
        delete_button.clicked.connect(lambda: delete_sat_record(list_view, db_url, window))

        layout = QVBoxLayout()
        layout.addWidget(menu_button)
        layout.addWidget(delete_button)
        layout.addWidget(headers)
        layout.addWidget(list_view)

        self._frame = QFrame()
        self._frame.setLayout(layout)

    
    def get_frame(self):
        return self._frame


    @staticmethod
    def switch_to_edit_frame(db_url, window):
        frame = SATEditFrame(window, db_url).get_frame()

        set_window_frame(window, frame, "Delete SAT Entries")
    