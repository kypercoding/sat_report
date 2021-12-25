from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt


def set_window_frame(window, frame, window_msg):
    window.setWindowTitle(window_msg)
    window.setCentralWidget(frame)
    screen_dims = QDesktopWidget().screenGeometry()

    window.resize(screen_dims.width() // 2, screen_dims.height() // 2)