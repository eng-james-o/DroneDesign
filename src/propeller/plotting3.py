#using pyqtcharts or pyqtgraph
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
#import pandas as pd

#treat the values in the dataframe
from propeller.dataframe import clean

#plotting functions
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#from data import save_propeller

from PyQt5.uic import loadUiType
prop_ui, _ = loadUiType(r"src\ui\prop_graph.ui")

class propeller(prop_ui, QWidget):
    def __init__(self, parent):
        super(propeller, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        #self.plotter = PlotWidget()
        self.readyBox.setVisible(False)

    def receive(self, df, PropName):
        '''receive the full dataframe from main'''
        self.df = df
        #print('received')
        #use the clean function to clean up the dataframe
        #it does not handle missing values
        clean(self.df)
        #store the name of the current propeller for reference
        self.propeller_name = PropName
        #
        self.InitUI()

    def InitUI(self):
        #get the value of the radiobutton
        #the radiobutton is the x-axis to be plotted
        self.radioButtonJ.setChecked(True)
        self.RADIOBTN = 'rpm' if self.radioButtonRpm.isChecked() else 'J'
        #
        self.x = self.RADIOBTN
        #
        self.z = 'rpm' if self.x=='J' else 'J'
        #set the variable used to populate the slider
        self.var = self.variable()

        self.Slider.setMinimum(0)
        self.Slider.setMaximum(len(self.var) -1)
        self.Slider.setValue(0)
        #set text of lineEdit to the first value in the list
        self.lineEditDfvar.setText(str(self.var[0]))

        #get current slider position and use for slicing
        self.value = self.var[0]

        #plot the first graph
        #self.plotter.reset()
        #p1 = self.widget.plot(self.x, 'Thrust', self.df[self.df[self.z]==self.value])

        self.p1 = self.widget.plot(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Thrust'].tolist())
        self.p2 = self.widget.plot(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Pe'].tolist())
        #print(self.df[self.df[self.z]==self.value]["Thrust"])

        #plot2 = self.plotter.draw(self.x, 'Pe', self.df[self.df[self.z]==self.value], 'Efficiency',2)
        #self.plotter.legend(plot1, plot2)

        #bind events, to be done after populating the slider
        self.handle_events()
        #
        self.labelPropeller.setText(self.propeller_name)
        self.readyBox.setText('Ready')
        self.readyBox.setCheckState(1)
        self.readyBox.setVisible(True)
        QtCore.QTimer.singleShot(7000, self.hide_readybox)

        #set the text of the labels to the correct value
        if self.radioButtonRpm.isChecked():#plotting against rpm
            self.x = 'rpm'
            self.label.setText('Eff, Cp, Ct vs rpm')
            self.labelDfVar2.setText('J')#or velocity
            self.labelDfVar.setText('adv ratio')

        if self.radioButtonJ.isChecked():#plotting against j
            self.x = 'J'
            self.label.setText('Eff, Cp, Ct vs J')
            self.labelDfVar2.setText('rpm')
            self.labelDfVar.setText('rpm')

    def hide_readybox(self):
        self.readyBox.setVisible(False)

#--------------------MAIN FUNCTIONS------------------------------

    def handle_events(self):
        #self.Slider.sliderMoved.connect(self.update_variable)
        #the values that sliderMoved() returns is not direct indices

        self.Slider.valueChanged.connect(self.update_variable)
        #or write function to check what was done to the slider and
        #allow the appropriate action, remember to use sliderMoved()

        self.radioButtonRpm.clicked.connect(self.radiobutton)
        self.radioButtonJ.clicked.connect(self.radiobutton)

    def update_variable(self):
        '''get the current value from the slider to the lineEdit'''
        self.value = self.var[self.Slider.value()]
        self.lineEditDfvar.setText(str(self.value))

        #handle plotting, based on what radiobutton is selected
        #p1 = self.widget.plot(self.x, 'Thrust', self.df[self.df[self.z]==self.value])
        self.p1.setData(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Thrust'].tolist())
        self.p2.setData(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Pe'].tolist())
        #print(p1,p2)
        #self.plotter.show()
        #plot2 = self.plotter.draw(self.x, 'Pe', self.df[self.df[self.z]==self.value], 'Efficiency',2)
        #self.plotter.legend(plot1, plot2)

    def radiobutton(self):
        '''select the x-axis to be used, from the radiobuttons'''
        initial_radiobutton = self.RADIOBTN #store previous value

        #get what radiobutton is checked
        if self.radioButtonRpm.isChecked(): #plotting against rpm
            self.RADIOBTN = 'rpm'
        else:
            self.RADIOBTN = 'J'

        #check if radiobutton was changed by comparing old and new
        if initial_radiobutton == self.RADIOBTN:
            #nothing was changed
            pass
        else:
            #'changed from {} to {}'.format(initial_radiobutton,self.RADIOBTN))
            if self.radioButtonRpm.isChecked():#plotting against rpm
                self.x = 'rpm'
                self.label.setText('Eff, Cp, Ct vs rpm')
                self.labelDfVar2.setText('J')#or velocity
                self.labelDfVar.setText('adv ratio')

            if self.radioButtonJ.isChecked():#plotting against j
                self.x = 'J'
                self.label.setText('Eff, Cp, Ct vs J')
                self.labelDfVar2.setText('rpm')
                self.labelDfVar.setText('rpm')
            #
            self.var = self.variable()
            self.z = 'rpm' if self.x=='J' else 'J'
            #
            #------------VERY IMPORTANT-----------------------
            #since the radiobutton was changed, reset the slider
            #as well as the lineEdit, could this be a QAction instead
            self.widget.clear()

            self.Slider.setMinimum(0)
            self.Slider.setMaximum(len(self.var) -1)
            self.Slider.setValue(0)
            self.lineEditDfvar.setText(str(self.var[0]))
            #you can replace the line above with a call to update_variable()
            #this should be a cleaner solution

            #self.plotter.reset()
            #self.plotter = propPlotter(self.widget)
            #p1 = self.widget.plot(self.x, 'Thrust', self.df[self.df[self.z]==self.value])

            #self.widget.clear()
            self.p1 = self.widget.plot(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Thrust'].tolist())
            self.p2 = self.widget.plot(self.df[self.df[self.z]==self.value][self.x].tolist(), self.df[self.df[self.z]==self.value]['Pe'].tolist())

            #self.plotter.show()
            #plot2 = self.plotter.draw(self.x, 'Pe', self.df[self.df[self.z]==self.value], 'Efficiency',2)
            #self.plotter.legend(plot1, plot2)

    def variable(self):
        '''return the list of avai_rpm or avai_j
        if x = rpm, then return avai_j for individual DFs'''
        try:
            if self.x == 'rpm':#plotting against rpm
                #return self.df[:][self.df['rpm'] == rpm]['J'].unique()
                return list(self.df['J'].unique()) #avai_j
            elif self.x == 'J':
                return list(self.df['rpm'].unique()) #avai_rpm
        except NameError:
            #self.x has not been defined
            self.radiobutton()

#------------miscellaneous functions---------------------------

    def save(self):
        '''save the current propeller: name and dataframe'''
        #save_propeller(self.df, self.propeller_name)
        pass

#------------dataframe functions-------------------------------

#make dataframe functions into another module to import
#    P = Cp * rho * n**3 * D**5
#    T = Ct * rho * n**2 * D**4
#    J = V/n*D
#    eff = T*V/ Q*w
#    eff = Ct*J/Cp

#------------plotting functions--------------------------------

#make plotting functions into another module to import
