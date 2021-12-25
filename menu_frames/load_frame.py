from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt

import os

import menu_frames.main_frame as mf

import sat_frames.sat_main_frame as sm

from frame_switch.window_frame import set_window_frame


def get_file(window):
    dialog = QFileDialog()
    dialog.setNameFilter("Files (*.sqlite)")

    file = QFileDialog.getOpenFileName()[0]

    if file is not None and file != "":
        sm.SATMainFrame.switch_to_sat_menu(window, file)


class LoadFrame:
    def __init__(self, window):
        label_str = """
        Pressing the button below will open a file chooser, please be sure
        to choose the desired database in which you wish to edit or view your
        SAT data. 
        """

        label = QLabel(label_str)
        label.setAlignment(Qt.AlignCenter)

        button = QPushButton("Select File")
        button.clicked.connect(lambda: get_file(window))

        home_button = QPushButton("Return Home")
        home_button.clicked.connect(lambda: mf.MainFrame.switch_to_main_menu(window))

        items = QVBoxLayout()

        items.addWidget(label)
        items.addWidget(button)
        items.addWidget(home_button)

        self._frame = QFrame()
        self._frame.setLayout(items)


    def get_frame(self):
        return self._frame


    def switch_to_load_frame(window):
        frame = LoadFrame(window).get_frame()

        set_window_frame(window, frame, "Load Database...")