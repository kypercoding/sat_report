from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from db_management.db import get_sat_data

from frame_switch.window_frame import set_window_frame

import sat_frames.sat_main_frame as sm


class SATProgressFrame:
    def __init__(self, window, db_url):
        # a figure instance to plot on
        figure = plt.figure()
   
        # this is the Canvas Widget that 
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        canvas = FigureCanvas(figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(canvas, window)

        self.plot(db_url, window, figure, canvas)
   
        # Just some button connected to 'plot' method
        button = QPushButton('Refresh')
           
        # adding action to the button
        button.clicked.connect(lambda: self.plot(db_url, window, figure, canvas))

        menu_button = QPushButton("Return to SAT Menu")
        menu_button.clicked.connect(lambda: sm.SATMainFrame.switch_to_sat_menu(window, db_url))
   
        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(toolbar)
           
        # adding canvas to the layout
        layout.addWidget(canvas)
        
        # adding push button to the layout
        layout.addWidget(button)
        layout.addWidget(menu_button)

        self._frame = QFrame()
        self._frame.setLayout(layout)

    
    def get_frame(self):
        return self._frame


    def plot(self, db_url, window, figure, canvas):
        data = get_sat_data(db_url, window)

        if data == None:
            return

        dates = data['dates']

        composite = data['composite']
        ebrw = data['ebrw']
        math = data['math']

        # clearing old figure
        figure.clear()
   
        # create an axis
        ax = figure.add_subplot(111)
   
        # plot data
        ax.plot(dates, composite, '*:', label="Composite Score")
        ax.plot(dates, ebrw, '*:', label = "EBRW Score")
        ax.plot(dates, math, '*:', label = "Math Score")

        ax.set_title("Progress Report")

        ax.set_ylim(top=1700, bottom=100)

        ax.tick_params(axis='x', rotation=90)

        ax.legend()

        figure.tight_layout()

        # refresh canvas
        canvas.draw()

    
    @staticmethod
    def switch_to_view_progress(window, db_url):
        frame = SATProgressFrame(window, db_url).get_frame()

        set_window_frame(window, frame, "View SAT Progress...")