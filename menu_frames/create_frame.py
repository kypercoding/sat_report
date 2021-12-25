from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt

from frame_switch.window_frame import set_window_frame

from db_management.db import make_db_file

import menu_frames.main_frame as mf
import sat_frames.sat_main_frame as sm


def create_sqlite_file(line_edit, window):
    if line_edit.text() == '':
        QMessageBox.about(window, "Error!", "Please put a name for the file!")
        return

    directory = str(QFileDialog.getExistingDirectory())

    path = make_db_file(line_edit.text(), directory)

    if path is not None:
        sm.SATMainFrame.switch_to_sat_menu(window, path)


class CreateFrame:
    def __init__(self, window):
        label_str = """
        Pressing the button below will open a directory chooser, please be sure
        to choose the desired directory in which you wish to save your
        SAT database.
        """

        label = QLabel(label_str)
        label.setAlignment(Qt.AlignCenter)

        line_edit = QLineEdit()

        button = QPushButton("Select Directory")
        button.clicked.connect(lambda: create_sqlite_file(line_edit, window))

        home_button = QPushButton("Return Home")
        home_button.clicked.connect(lambda: mf.MainFrame.switch_to_main_menu(window))

        items = QVBoxLayout()

        items.addWidget(label)
        items.addWidget(button)
        items.addWidget(line_edit)
        items.addWidget(home_button)

        self._frame = QFrame()
        self._frame.setLayout(items)


    def get_frame(self):
        return self._frame


    @staticmethod
    def switch_to_create_frame(window):
        frame = CreateFrame(window).get_frame()

        set_window_frame(window, frame, "Create Database...")