from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox
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

        # options for plots
        options = {
            "Composite": {"name": "composite", "limits": [100, 1700]},
            "Evidenced-Based Reading/Writing": {"name": "ebrw", "limits": [100, 900]},
            "Math": {"name": "math", "limits": [100, 900]},
            "Heart of Algebra": {"name": "hoa", "limits": [0, 16]},
            "Problem Solving and Data Analysis": {"name": "psda", "limits": [0, 16]},
            "Passport to Advanced Math": {"name": "pam", "limits": [0, 16]},
            "Expression of Ideas": {"name": "eoi", "limits": [0, 16]},
            "Standard English Conventions": {"name": "sec", "limits": [0, 16]},
            "Words in Context": {"name": "wic", "limits": [0, 16]},
            "Command of Evidence": {"name": "coe", "limits": [0, 16]}
        }

        # list view for viewing plots
        list_of_plots = QComboBox()

        # options for list widget
        for option in options:
            list_of_plots.addItem(option)

        # list widget detecting change in plot
        list_of_plots.textActivated.connect(lambda: self.plot(db_url, window, options, list_of_plots, figure, canvas))

        menu_button = QPushButton("Return to SAT Menu")
        menu_button.clicked.connect(lambda: sm.SATMainFrame.switch_to_sat_menu(window, db_url))
   
        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(toolbar)
           
        # adding canvas to the layout
        layout.addWidget(canvas)
        
        # adding push button to the layout
        layout.addWidget(list_of_plots)
        layout.addWidget(menu_button)

        self.plot(db_url, window, options, list_of_plots, figure, canvas)

        self._frame = QFrame()
        self._frame.setLayout(layout)

    
    def get_frame(self):
        return self._frame


    def plot(self, db_url, window, options, list_view, figure, canvas):
        data_dict = get_sat_data(db_url, window)

        type = list_view.currentText()

        code = options[type]["name"]
        limits = options[type]["limits"]

        dates = data_dict['dates']
        scores = data_dict[code]

        # clearing old figure
        figure.clear()
   
        # create an axis
        ax = figure.add_subplot(111)
   
        # plot data
        ax.plot(dates, scores, '*:', label=type)

        ax.set_title("{} Score Progress".format(type))

        ax.set_ylim(top=limits[1], bottom=limits[0])

        ax.tick_params(axis='x', rotation=90)

        ax.legend()

        figure.tight_layout()

        # refresh canvas
        canvas.draw()

    
    @staticmethod
    def switch_to_view_progress(window, db_url):
        frame = SATProgressFrame(window, db_url).get_frame()

        set_window_frame(window, frame, "View SAT Progress...")