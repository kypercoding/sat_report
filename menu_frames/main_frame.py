from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt

import menu_frames.create_frame as cf
import menu_frames.delete_frame as df
import menu_frames.load_frame as lf

from frame_switch.window_frame import set_window_frame


class MainFrame:
    def __init__(self, window):
        # app title text
        app_name = QLabel("SAT Report")
        app_name.setAlignment(Qt.AlignCenter)

        # creates the three buttons
        create_button = QPushButton("Create Database")
        load_button = QPushButton("Load Database")
        delete_button = QPushButton("Delete Database")

        # VBox holding content vertically
        v_box = QVBoxLayout()
        v_box.addWidget(app_name)
        v_box.addWidget(create_button)
        v_box.addWidget(load_button)
        v_box.addWidget(delete_button)

        self._frame = QFrame()
        self._frame.setLayout(v_box)

        # create button leads to creation of new sqlite file
        create_button.clicked.connect(lambda: cf.CreateFrame.switch_to_create_frame(window))

        # load button leads to loading of existing sqlite file
        load_button.clicked.connect(lambda: lf.LoadFrame.switch_to_load_frame(window))

        # delete button leads to deletion of sqlite file
        delete_button.clicked.connect(lambda: df.DeleteFrame.switch_to_delete_frame(window))


    def get_frame(self):
        return self._frame

    
    @staticmethod
    def switch_to_main_menu(window):
        frame = MainFrame(window).get_frame()

        set_window_frame(window, frame, "Delete Database...")
