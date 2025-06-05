from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar
import matplotlib
import matplotlib.style as style

style.use('seaborn-darkgrid')
matplotlib.use('QT5Agg')

class MplCanvas(Canvas):
    def __init__(self): #parent=None, width=5, height=4, dpi=100
        self.fig = Figure()
        self.fig.set_tight_layout(True)
        #figsize=(width, height), dpi=dpi
        self.axes = self.fig.add_subplot(111)
        #self.axes.set_xlabel('velocity')
        #self.axes.set_ylabel('thrust')
        Canvas.__init__(self, self.fig)
        Canvas.updateGeometry(self)

class MplWidget(QWidget):
    def __init__(self, parent):#parent=None
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QVBoxLayout()
        self.toolbar = NavToolbar(self.canvas, self)
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.second_axis =False
        '''top=0.95, bottom=0.15, left=0.16, right=0.95, hspace=0.2, wspace=0.2'''

    def tight(self):
        self.canvas.fig.set_tight_layout(True)

    def new_ax(self):
        self.canvas.axes2 = self.canvas.axes.twinx()
        self.second_axis = True

    def plot2(self,xa,ya, data_frame=None,label_str=None):
        return self.canvas.axes2.plot(xa,ya,data=data_frame,label=label_str,color='tab:green')

    def plot(self,xa,ya, data_frame=None,label_str=None):
        '''if data_frame is specified: it is assumed to be propeller plot
        it returns the 2D line object and draw is called elsewhere'''
        if isinstance(data_frame, pd.core.frame.DataFrame): # plot using dataframe
            #print(data_frame)
            return self.canvas.axes.plot(xa,ya,data=data_frame,label=label_str)
        else:#else plot normal x series vs y series
            return self.canvas.axes.plot(xa,ya)

    def clear_canvas(self):
        '''clear canvas'''
        #print('clear canvas')
        self.canvas.axes.clear()

    def clear_canvas2(self):
        #print('clear canvas 2')
        self.canvas.axes2.clear()

    def show_plot(self):
        '''call draw on canvas'''
        self.canvas.draw()

    def legend(self, *args, **kwargs):
        '''create legend and pass arguments as is'''
        self.canvas.axes.legend(*args, **kwargs)
        # if axes2 is defined already, add legend
        try:
            self.canvas.axes2.legend(*args, **kwargs)
        except AttributeError:
            #print('second axis not defined')
            pass
    def label(self, xlabel, ylabels):
        self.canvas.axes.set_xlabel(str(xlabel))

    def grid(self, *args, **kwargs):
        '''toggle grid and pass arguments as is'''
        self.canvas.axes.grid(*args, **kwargs)
