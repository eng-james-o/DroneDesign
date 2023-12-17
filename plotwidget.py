# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget


class propPlotter(PlotWidget):
    def __init__(self, parent):
        PlotWidget.__init__(self)
