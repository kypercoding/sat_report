from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt

import os

from frame_switch.window_frame import set_window_frame

import menu_frames.main_frame as mf


def delete_file(window):
    response = QMessageBox.question(window, 'PyQt5 message', "Are you sure you want to delete?", QMessageBox.Yes | QMessageBox.No)

    if response == QMessageBox.No:
        return

    file = str(QFileDialog.getOpenFileName()[0])

    # BUG REPORT: doing this snippet of code
    # ensures that the program crashes (incidentally
    # the converse is the opposite
    if file is not None and file != "":
        os.remove(file)


class DeleteFrame:
    def __init__(self, window):
        label_str = """
        Pressing the button below will open a file chooser, please be sure
        to choose the desired file that which you wish to delete forever. 
        """

        label = QLabel(label_str)
        label.setAlignment(Qt.AlignCenter)

        button = QPushButton("Select File")
        
        button.clicked.connect(lambda: delete_file(window))

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


    @staticmethod
    def switch_to_delete_frame(window):
        frame = DeleteFrame(window).get_frame()

        set_window_frame(window, frame, "Delete Database...")
