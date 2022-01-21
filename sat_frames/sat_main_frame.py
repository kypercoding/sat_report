from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt

from frame_switch.window_frame import set_window_frame

import sat_frames.add_sat_frame as af
import sat_frames.delete_sat_frame as ds
import sat_frames.sat_progress_frame as sp
import menu_frames.main_frame as mf


class SATMainFrame:
    def __init__(self, window, db_url):

        label_str = """
        Below is a list of the options:
        - Add SAT --> adds SAT practice test to student record
        - View and Delete SAT --> views and deletes SAT practice test from student record
        - View Progress --> creates simple graphs that track student progress
        """
        
        label = QLabel(label_str)
        label.setAlignment(Qt.AlignCenter)

        add_button = QPushButton("Add SAT")
        delete_button = QPushButton("View/Delete SAT Records")
        view_button = QPushButton("View Progress")
        return_button = QPushButton("Return to Main Menu")

        add_button.clicked.connect(lambda: af.AddSATFrame.switch_to_add_sat(window, db_url))
        delete_button.clicked.connect(lambda: ds.SATEditFrame.switch_to_edit_frame(db_url, window))
        view_button.clicked.connect(lambda: sp.SATProgressFrame.switch_to_view_progress(window, db_url))
        return_button.clicked.connect(lambda: mf.MainFrame.switch_to_main_menu(window))

        items = QVBoxLayout()

        items.addWidget(label)
        items.addWidget(view_button)
        items.addWidget(add_button)
        items.addWidget(delete_button)
        items.addWidget(return_button)

        self._frame = QFrame()
        self._frame.setLayout(items)


    def get_frame(self):
        return self._frame


    @staticmethod
    def switch_to_sat_menu(window, db_url):
        frame = SATMainFrame(window, db_url).get_frame()
        
        set_window_frame(window, frame, "SAT Main Menu...")