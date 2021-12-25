from typing import Text
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.sip import delete

from sys import argv, stderr, exit

import menu_frames.main_frame as mf


# main menu for SAT Report, containing three buttons:
# 1. Create Database
# 2. Load Database
# 3. Delete Database

try:
    # creates QApplication
    app = QApplication(argv)

    # creates window for application
    window = QMainWindow()

    mf.MainFrame.switch_to_main_menu(window)
    
    window.show()

    exit(app.exec_())

except Exception as ex:
    print(ex, file=stderr)
    exit(2)
