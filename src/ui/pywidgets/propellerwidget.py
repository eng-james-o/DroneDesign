from PyQt5.QtWidgets import QWidget
import pandas as pd
#from collections import OrderedDict
#import scipy.interpolate
#import scipy.optimize

from PyQt5.uic import loadUiType

prop_ui, _ = loadUiType(r'src\ui\prop_graph.ui')

class propeller(prop_ui,QWidget):
    def __init__(self, parent):
        super(propeller,self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

    def receive(self, dictionary, PropellerName):
        '''receive df_dictionary and propeller name from main
        serves as entry point into propeller widget'''
        self.rpm_dict = dictionary# store dictionary
        #firstly create the extra dictionary needed
        self.create_dictionaries(dictionary) #create dictionaries of J and V
        self.bind()

        self.PropellerName = PropellerName
        self.labelPropeller.setText(self.PropellerName)

        #prepare to plot and obtain values
        #self.clear_canvas()#clear canvas in preparation for plotting
        self.select_x_axis()
        self.draw()

    def draw(self):
        self.clear_canvas()
        self.plot()
        self.widget.grid(True)
        self.legend()
        self.show_plot()

    def InitUI(self, option):
        '''called after select_param because dictionaries must be ready'''
        if option == ' J':#using the rpm_dictionary
            #plot vs adv ratio on the x-axis
            self.rpm_available = list(self.rpm_dict.keys())
            self.rpm_available.sort()
            #initialize to the first rpm value
            self.rpm = self.rpm_available[0]
            self.Slider.setValue(0)
            #set the label to the current rpm dataframe in use
            self.labelVar.setText(str(self.rpm)+' rpm')
            self.label.setText('Eff, Cp, Ct vs J')
        elif option == 'rpm':#using the j_dictionary
            #plot vs rpm on the x-axis
            self.j_available = list(self.j_dict.keys())#remember to call the correct dictionary
            self.j_available = [int(item) for item in self.j_available]
            self.j_available.sort()
            #initialize to the first j value
            self.j = self.j_available[0]
            self.Slider.setValue(0)
            #set the label to the current j dataframe in use
            self.labelVar.setText(str(self.j)+' advance ratio')
            self.label.setText('Eff, Cp, Ct vs rpm')

    def bind(self):
        '''use number of rpm (or var) points inside dataframe to populate slider maximum
        and connect slider and button events'''
        self.Slider.sliderReleased.connect(self.update_var)
        #self.Slider.valueChanged.connect(self.update_var)

        self.Slider.setMaximum(len(self.available_rpm)-1)

        self.radioButtonRpm.clicked.connect(self.radiobutton)
        self.radioButtonJ.clicked.connect(self.radiobutton)

    def create_dictionaries(self, df_dict):
        '''receive df_dict with rpm keys and create df_dict with J keys and dictioanry with V keys'''
        #self.rpm_dict is the same as self.dictionary
        '''or perhaps upon reading the data in main.get_data_to_dataframe
        read all the files into  single data frame with rpm column
        such that you can make plots from slices based on rpm
        it could avoid too many loops to convert into different dataframes'''

        self.j_dict = dict()
        #available_j = self.rpm_dict[' J'].to_list()
        self.available_j = self.rpm_dict[1000][' J'].to_list()
        self.available_rpm = list(self.rpm_dict.keys())
        self.available_rpm.sort()
        self.rpm = self.available_rpm[0]
        self.j = self.available_j[0]

        #for each value in available_j: the unique values of j
        for j in self.available_j:
            #create new dataframe for each j
            j_df = pd.DataFrame()
            #find means to call the values from each rpmtable for j
            for index,df in enumerate(df_dict):
                #slice each rpm dataframe and find where J = current j in iteration
                row = df_dict[df][:][df_dict[df][' J']==j]
                #r=row.values.tolist() #gives the row as a list
                #d=OrderedDict(r)
                #add the current row to the current j dataframe
                j_df = j_df.append(row,ignore_index=True)# not working as expected

            j_df.sort_values('rpm',inplace=True,ignore_index=True)
            self.j_dict[j] = j_df
            #print(j_df.head())
        #print(self.j_dict[0.53])

    def select_param(self):
        '''returns self.x, (self.y), dataframe, labels to use for plot'''
        '''it will select one of the dictionaries already created and
        put the appropriate slicing --- not yet implemented'''
        self.y = [' Pe', ' Thrust',' Torque',' Power']
        #implement returning the dataframe and labels as well

    def select_x_axis(self):
        '''return string as x_axis based on which radiobutton is checked'''
        pre = self.x
        if self.radioButtonRpm.isChecked():
            self.x = 'rpm'
            #the dataframes will have keys as rpm
        elif self.radioButtonJ.isChecked():
            self.x = ' J'
            #the dataframes will have keys as J
        #print('self.x = ',self.x)
        new = self.x
        #if pre != new: #if option has changed
            #self.InitUI(self.x)
        self.InitUI(self.x)

    def radiobutton(self):
        self.select_x_axis()
        self.widget.clear_canvas2()
        self.draw()

    def plot(self):
        '''plot function implemented in MplWidget
        using x,y, data_frame, label after clearing canvas first'''
        if self.widget.second_axis == False:
            self.widget.new_ax()
        if self.x == ' J':
            self.Thrust = self.widget.plot('V',' Thrust',data_frame=self.rpm_dict[self.rpm],label_str='Thrust') #
            #self.PWR = self.widget.plot('V',' PWR',data_frame=self.rpm_dict[self.rpm],label_str='Power')
            self.Torque = self.widget.plot('V',' Torque',data_frame=self.rpm_dict[self.rpm],label_str='Torque') #
            self.Pe = self.widget.plot2('V',' Pe',data_frame=self.rpm_dict[self.rpm],label_str='Pe')
            self.widget.canvas.axes2.tick_params(axis='y',labelcolor='tab:green')
        elif self.x == 'rpm':
            self.Thrust = self.widget.plot(self.x,' Thrust',data_frame=self.j_dict[self.j],label_str='Thrust') #
            #self.PWR = self.widget.plot(self.x,' PWR',data_frame=self.j_dict[self.j],label_str='Power')
            self.Torque = self.widget.plot(self.x,' Torque',data_frame=self.j_dict[self.j],label_str='Torque') #
            self.Pe = self.widget.plot2(self.x,' Pe',data_frame=self.j_dict[self.j],label_str='Pe')
            self.widget.canvas.axes2.tick_params(axis='y',labelcolor='tab:green')
        self.widget.tight()

    def legend(self):
        #self.widget.canvas.axes.legend()#(self.Pe,self.Thrust,self.Torque),('Pe','Thrust','Torque')
        self.widget.legend()

    def show_plot(self):
        #self.widget.canvas.draw()
        self.widget.show_plot()

    def clear_canvas(self):
        '''clear canvas of MplWidget'''
        #self.widget.canvas.axs.cla()
        self.widget.clear_canvas()

    def update_var(self):
        '''obtain the current value of the slider, return the appropriate var
        and change the plot to the new var'''
        if self.x ==' J':
            self.rpm = self.available_rpm[self.Slider.value()]
            self.labelVar.setText(str(self.rpm)+' rpm')
        elif self.x == 'rpm':
            self.j = self.available_j[self.Slider.value()]
            self.labelVar.setText('adv ratio :'+str(self.j))
        self.widget.clear_canvas2()
        self.draw()

