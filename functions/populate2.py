import pandas as pd
import numpy as np
#from io import StringIO
#prepare to handle missing values

def populate_df(file_str_list, matches, full_df=None):
    '''populate full_df from the file_str_list using matches (of rpm)'''
    if not full_df:
        full_df = pd.DataFrame()
    def to_csv(table):
        '''converts table (list of strings) to list of lists'''
        del table[:2]
               
        ##convert each line(string) into a list, with each cell as a string
        table_lists = [line.split(sep=' ') for line in table]
        table_lists = [list(map(float,line)) for line in table_lists]
        
        return table_lists

    def to_df(table):
        '''converts table_csv: string to dataframe'''
        #col = table[0]# com and confirm this
        col = ['V','J','Pe','Ct','Cp','PWR','Torque','Thrust']
        dataframe = pd.DataFrame(table, columns=col)
        #
        #fill up missing values with interpolation
        dataframe = dataframe.replace('-NaN', np.nan)
        dataframe = dataframe.interpolate()#make means to pass arguments
        #
        return dataframe

    def conversions(d_f, rpm_value):
        '''add rpm column to dataframes and covert from the units into SI inplace'''
        #this function call is giving errors on specific files
        #probably due to the presence of NaN in those files
        #figure out a way tp handle those kind of values
        #either using 0 or using a default value, or skipping it
        #or using the previous value, or an average between
        #the previous and the next or a means to smoothen the curve
        single_rpm_list = [rpm_value for i in range(d_f.shape[0])]
        d_f['rpm'] = single_rpm_list
        #
        #convert power from hp to w
        pwr_list = d_f['PWR'].to_list()
        d_f['PWR'] = [pwr*745.7 for pwr in pwr_list]
        #convert torque from in-lbf to Nm
        torque_list = d_f['Torque'].to_list()
        d_f['Torque'] = [torque*0.112985 for torque in torque_list]
        #convert thrust from lbf to N
        thrust_list = d_f['Thrust'].to_list()
        d_f['Thrust'] = [thrust*4.44822 for thrust in thrust_list]
        #convert velocity from mph to m/s
        velocity_list = d_f['V'].to_list()
        d_f['V'] = [velocity*0.44704 for velocity in velocity_list]

    def generate(file_list, mtches):
        '''generate each rpm,table using matches from file_str_list'''
        for index in range(len(mtches)):
            if index < len(mtches)-1:
                table = file_list[mtches[index][0] +1: mtches[index+1][0]]
            elif index == len(mtches)-1:
                table = file_list[mtches[index][0] +1 : ]
            #
            rpm = mtches[index][1]
            table = to_csv(table)
            #print(table)
            df = to_df(table)
            conversions(df, rpm)
            #
            yield df

    match = generate(file_str_list, matches)
    for df in match:
        full_df = full_df.append(df,ignore_index=True)
    #full_df.sort_values('rpm',inplace=True,ignore_index=True)
    return full_df
