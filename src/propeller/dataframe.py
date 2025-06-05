#dataframe cleaning,
#handle null values
#
import numpy as np
import pandas as pd

def clean(full_df):
    #proper data types
    full_df['rpm'] = full_df['rpm'].astype(np.int64)

    #unique rpm available
    unique_rpm = full_df.rpm.unique()

    #unique j
    #unique_j = full_df.J.unique()

    #rename columns
    full_df.rename(columns=
        {'V':'v', ' J':'J',
        ' Pe':'Pe', ' PWR':'PWR',
        ' Torque':'Torque', ' Thrust':'Thrust'},
        inplace=True)

    #correct j values
    j_df = pd.DataFrame()

    for value in unique_rpm:
        #get the table for each rpm value in unique_rpm list
        single_rpm_df = full_df[:][full_df['rpm'] == value]
        #
        #store the unique values for each rpm table into a column in a new df
        j_df[str(value)] = single_rpm_df['J'].unique()
    #use the mean value of the row of j vales and concatenate to fill up the dataframe
    full_df['J'] = np.tile(j_df.mean(axis=1).round(decimals=2), j_df.shape[1])

    ### round_up_to_thousand on each value in the rpm column
    full_df['rpm'] = full_df['rpm'].round(decimals=-3)
