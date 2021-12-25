from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QDateTime

from db_management.db import add_sat_score

from frame_switch.window_frame import set_window_frame

import sat_frames.sat_main_frame as sm


def add_sat(db_url, window, line_edits, date_time_edit):

    params = {
        'datetime': date_time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss.zzz"),
        'composite': line_edits[0].text(),
        'ebrw': line_edits[1].text(),
        'math': line_edits[2].text(),
        'hoa': line_edits[3].text(),
        'psda': line_edits[4].text(),
        'pam': line_edits[5].text(),
        'eoi': line_edits[6].text(),
        'sec': line_edits[7].text(),
        'wic': line_edits[8].text(),
        'coe': line_edits[9].text()
    }

    add_sat_score(db_url, params, window)


class AddSATFrame:
    def __init__(self, window, db_url):

        main_text = """
        Please input the following information for the
        SAT practice test.
        Note that the subscores are not required for input.
        """

        main_label = QLabel(main_text)
        main_label.setAlignment(Qt.AlignCenter)

        date_time_label = QLabel("Date and Time Taken")

        date_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        date_time_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss.zzz")

        labels = [
            "Composite Score",
            "Evidence-Based Reading and Writing Score",
            "Math Score",
            "Heart of Algebra Subscore",
            "Problem Solving and Data Analysis Subscore",
            "Passport to Advanced Math Subscore",
            "Expression of Ideas Subscore",
            "Standard English Conventions Subscore",
            "Words in Context Subscore",
            "Command of Evidence Subscore"
        ]

        line_edits = []

        for label in labels:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(label)
            line_edits.append(line_edit)

        button = QPushButton("Add SAT Practice Test")
        button.clicked.connect(lambda: add_sat(db_url, window, line_edits, date_time_edit))

        menu_button = QPushButton("Return to SAT Menu")
        menu_button.clicked.connect(lambda: sm.SATMainFrame.switch_to_sat_menu(window, db_url))

        layout = QVBoxLayout()

        layout.addWidget(main_label)
        layout.addWidget(date_time_label)
        layout.addWidget(date_time_edit)

        for line_edit in line_edits:
            layout.addWidget(line_edit)

        layout.addWidget(button)
        layout.addWidget(menu_button)

        self._frame = QFrame()
        self._frame.setLayout(layout)
    

    def get_frame(self):
        return self._frame


    @staticmethod
    def switch_to_add_sat(window, db_url):
        frame = AddSATFrame(window, db_url).get_frame()
        
        set_window_frame(window, frame, "Add SAT...")