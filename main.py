from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtCore import QFile, QTextStream

from subprocess import PIPE, Popen
from collections import OrderedDict
from math import sqrt
import numpy as np
import io, csv, os

from sympy import Symbol, S, pi, plot, N, Piecewise
#from sympy.core.numbers import Float, Integer

rpm_pattern = '_(\d+)\.[a-zA-Z]{3}'

rpm = r'PROP RPM = (\d+)'
space = '\s+'

ui, _ = loadUiType(r"C:\Users\PC\Documents\qt_projects\dronedesign - Copy\UI\mainwindow.ui")
import BreezeStyleSheets.breeze_resources

from functions.file import load, match
from functions.populate2 import populate_df
from functions.text import strip, round_up

'''learn how to build python projects into exe and instllers
and add updates to code'''
'break up UI into different pages'
'save dataframes and other data'

class main(QMainWindow, ui):
    def __init__(self, parent=None):
        '''initialize main window'''
        super(main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI() #supposed to bind elements to events but is currently empty
        self.PROPELLER_AVAILABLE = False
        self.PROPELLER_SELECTED = False

        self.handle_buttons()# bind buttons,etc to events
        self.load_data()#load data from data class into this class to enable storage
        self.validate_lineEdits()
        self.move(20,20)
        self.show()

        #self.df_dict = dict() #data frame dictionary for propeller data intially empty

    def validate_lineEdits(self):
        '''bind all the lineEdits to qt validators'''
        pass
    def restore_actions(self):
        '''to restore app to start state maybe giving the option of clearing only graph or whole screen'''
        #main()
        #del self.widget.canvas.axes.lines[0]
        print(self.widget.canvas.axes.lines)

    def load_data(self):
        '''collect values from data class and unload them into this class'''
        self.store = data()
        self.standard = self.store.standard #a dictionary in this class
        self.__dict__.update(self.standard)

    def input_validator(self):
        pass
    def InitUI(self):
        pass
    def handle_buttons(self):
        '''connect buttons and sliders to events'''
        self.pushButtonCalculate.clicked.connect(self.calculate)
        self.pushButtonPlot.clicked.connect(self.plot_all)
        self.pushButtonPoints.clicked.connect(self.showpoints)
        self.velocitySlider.sliderReleased.connect(self.updatevlocity)
        self.velocitySlider.valueChanged.connect(self.updatevlocity)

        self.actionRestore_defaults.triggered.connect(self.restore_actions)

        self.toolButtonPropeller.clicked.connect(self.get_propeller)
        self.toolButtonExtra.clicked.connect(self.extra)

    def output(self,out,target):
        '''write out to target element (lineEdit)'''
        #try using partial here from functools to avoid rewriting target in the recursion
        if isinstance(out, str):
            target.setText(out)
        #elif isinstance(out, float) or isinstance(out, Float) or isinstance(out, Integer):
        else:
            temp = round_up(out)
            self.output(str(temp), target)

    def plot_all(self):
        '''Plot Thrust, drag and friction vs velocity
        '''
        pl = plot(self.Thrust, self.D, self.F, (self.v, 0, 12), show=False) #sympy plot
        plot_list = ["Thrust", "Drag", "Friction"]
        for index, name in enumerate(plot_list, 0 ):
            pl[index].label = name #assign names to individual plots
        pl[0].line_color = 'blue'
        pl[1].line_color = 'red'
        pl[2].line_color = 'green' #find a cleaner solution to this color implementation
        pl.legend = True
        pl.show()
    def extra(self):
        '''give option to make 3d plot of rpm v, (pe, ct and cp)'''
        if self.toolButtonExtra.isChecked():
            self.setMaximumWidth(1220) #change screen size to accomodate propeller plot
            self.setGeometry(self.x()+1, self.y()+31, 1220, self.height())
            if self.PROPELLER_AVAILABLE:
                self.labelPropellerheader.setText(self.propellerFileName)
            else:
                self.widgetP.labelPropeller.setText('select a propeller file')
        else:
            self.setMaximumWidth(820)
            self.setGeometry(self.x()+1, self.y()+31, 820, self.height())

        #print(self.widgetP.parent.parent()) gives you main
        #print(self.widgetP.parent) gives you centralwidget
        #print(self.widgetP)) gives you propeller
        #think about registering qml types

    def plot_thrust(self):
        ''' plot the indiviual thrust plot into derived widget'''
        x=np.linspace(0,15)
        y=[]
        for _ in x:
            temp_y = self.Thrust.subs({self.v : _ })
            y.append(N(temp_y))
        #self.widget.clear_canvas() uncomment this to clear canvas for  new graph
        #leave commented to plot new graph on old one

        self.thrust_plot = self.widget.plot(xa=x,ya=y)
        self.widget.grid(True, which='both', axis='both')
        self.widget.show_plot()

    def get_inputs(self):
        '''collect inputs from all lineEdits in order to make calculate function cleaner'''
        self.altitude = round_up(self.lineEditAlt.text())
        self.mass = round_up(self.lineEditMass.text())
        self.wingarea = round_up(self.lineEditWingarea.text())
        ######## note the next line : factor 0.8 is to include for 3d effects, different from oswald
        self.Clmax = round_up(self.lineEditClmax.text()) * 0.8
        self.Time = round_up(self.lineEditTime.text())
        self.Cl = round_up(self.lineEditCl.text())
        self.Cdpar = round_up(self.lineEditCdpar.text())
        self.Oswald = round_up(self.lineEditOswald.text())
        self.Ar = round_up(self.lineEditAr.text())
        self.Fcoeff = round_up(self.lineEditFcoeff.text())

    def get_airfoil(self):
        '''code toeither run xfoil, save results and use the reuired one
        or to collect xfoil results from an existing file'''
        #code to run xfoil, and keep the data and use the cl and clmax
        #os.system(r'cmd /k "cd C:\Users\PC\Downloads\XFOIL6.99 & xfoil"')
        #/k keeps the window open
        #/c closes it

        #xfoil = subprocess.run()
        process  = Popen("cmd.exe",shell=False,universal_newlines=True,
                         stdin=PIPE,stdout=PIPE,stderr=PIPE)
        commands = '@echo off\ncd C:/Users/PC/Downloads/XFOIL6.99\nxfoil\n'
        #commands2 = 'xfoil'

        out, err = process.communicate(commands)
        #a, b = process.communicate(commands2)
        print(out, '\n', err)

    def get_propeller(self):
        '''create dialog and collect propeller directory'''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        FullName, fileType = QFileDialog.getOpenFileName(self, "Select full propeller file", "C:\\Users\\PC\\Desktop\\apc_prop_files\\", "Data Files (*.dat *.csv *.txt);;All Files (*)", options=options)
        FilePath, FileName = os.path.split(FullName)
        #
        #if file has been supplied, split the filename into name and extension
        if FileName: name, extension = FileName.split(sep='.')
        if FilePath:
            self.lineEditPropellerfolder.setText(FilePath)
            self.PROPELLER_SELECTED = True
        #
        if self.PROPELLER_SELECTED:

            self.propellerFullName = r'{}'.format(FullName)
            self.propellerFileName = name
            self.propellerFilePath = r'{}'.format(FilePath)
            #
            self.get_files_to_dataframe()

    def get_files_to_dataframe(self):
        ''' load file into dataframe using external calls '''
        self.contents = load(self.propellerFullName)
        self.matches = match(self.contents)

        self.combined_df = populate_df(self.contents, self.matches)
        self.PROPELLER_AVAILABLE = True
        #call function in propeller widget
        self.widgetP.receive(self.combined_df, self.propellerFileName)
        if not self.toolButtonExtra.isChecked():
            self.toolButtonExtra.click()

    def calculate(self):
        #write code to run xfoil in background and obtain cl and cd values and if possible to keep the graphs generated
        #write code to obtain cd from openvsp
        #use small python to generate dialog that will prompt user about xfoil
        #also make small dialog that will ask user to save/display xfoil graphs

        self.get_inputs()

        #calculate required parameters
        self.density_h = self.density_sl * (((self.T_sl + self.a * self.altitude)/self.T_sl) ** (-self.g/(self.a * self.R)-1))
        self.output(self.density_h, self.lineEditDensity)

        self.weight = self.mass * self.g
        self.output(self.weight, self.lineEditWeight)

        self.wing_loading = self.weight / self.wingarea
        self.output(self.wing_loading, self.lineEditWingloading)

        self.V_stall = sqrt(self.wing_loading * 2/(self.density_h * self.Clmax))
        self.output(self.V_stall, self.lineEditVstall)

        self.V_r = 1.2 * self.V_stall  #velocity of rotation = 1.2*V_stall
        self.output(self.V_r, self.lineEditVr)

        self.Acceleration = self.V_r/self.Time
        self.output(self.Acceleration, self.lineEditAcc)

        #important variables
        half = S('1')/2
        self.v = Symbol('v')

        #drag
        self.D = half * self.density_h * self.wingarea * (self.Cdpar + (self.Cl**2)/(pi.evalf() * self.Oswald * self.Ar)) * self.v**2
        self.D_value = N(self.D.subs({self.v : 0}))
        self.output(self.D_value, self.lineEditDrag)

        #lift and friction
        self.lift = half*self.density_h*self.Cl*self.wingarea*self.v**2
        self.Reaction = self.weight - self.lift
        self.F = Piecewise((0,self.Reaction<0),((self.Reaction * self.Fcoeff),True))
        self.F_value = N(self.F.subs(self.v, 0))

        self.output(self.F_value, self.lineEditFriction)

        #free acceleration
        self.f = self.mass * self.Acceleration
        self.lineEditNetforce.setText(str(self.f))
        self.output(self.f, self.lineEditNetforce)

        #thrust
        self.Thrust = self.D + self.F + self.f
        self.Thrust_value = N(self.Thrust.subs({self.v : 0}))
        self.output(self.Thrust_value, self.lineEditThrust)

        #max friction, min drag, max thrust
        self.max_friction = self.F_value
        self.output(self.max_friction, self.lineEditFrictionmax)
        #self.Thrustmax
        #self.Dragmin

        self.plot_thrust()


        #self.get_airfoil()

    def showpoints(self):
        print('show points')
    def updatevlocity(self):
        #retrieve velocity value
        self.velocity = self.velocitySlider.value()/2.0 #slider was scaled from 0 to 30 instead of 0 to 15
        self.velocity_subs = {self.v : self.velocity}

        #calculate forces
        self.D_value = N(self.D.subs(self.velocity_subs))
        self.F_value = N(self.F.subs(self.velocity_subs))
        self.Thrust_value = N(self.Thrust.subs(self.velocity_subs))

        #update values into UI
        self.output(self.D_value, self.lineEditDrag)
        self.output(self.F_value, self.lineEditFriction)
        self.output(self.Thrust_value, self.lineEditThrust)



class data:
    def __init__(self):
        self.standard = OrderedDict(g = 9.80665,
        R = 287.0, #J/kgK
        T_sl = 288.0, #K
        a = -0.0065, #lapse rate in K/m
        #h = 100.0, #altitude in m
        density_sl = 1.225, #sea level altitude in kg/m3
        mu = 0.1)

        self.accept = list(('mass', 'AR', 'Cd_par', 'Cl', 'Cl_max', 'e', 'wing S', 'T'))
    def get(self,name):
        return self.standard[name]
    def set(self,name,value):
        self.standard[name] = value

if __name__ == "__main__":
    # set stylesheet
    app = QApplication([])

    #with open(r"C:\Users\PC\Documents\qt_projects\dronedesign\BreezeStyleSheets\dark.qss") as file:
    #    qss = file.read()
    #app.setStyleSheet(qss)
    #--------------------------any of the two works-------------
    file = QFile(r"C:/Users/PC/Documents/qt_projects/dronedesign/BreezeStyleSheets/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    #app.setStyle('Plastique')
    window = main()
    #window.show()
    app.exec_()
