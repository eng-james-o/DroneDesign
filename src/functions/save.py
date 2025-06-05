import pickle

class data:
    def __init__(*args, **kwargs):
        '''base class data for data storage in this project'''
        #store values in a dictionary, or hold references to
        #the values in the dictionary
        pass
    def params(self):
        pass
    def get_value(self, name):
        pass
    def set_value(self, name, value):
        pass

class save_motor(data):
    def __init__(self,kv, i0, R, cansize=None):
        '''storage for motor data, may store calculation results
        in the future, input cansize as xxyy'''
        self.kv = kv
        self.i0 = i0
        self.R = R
        if cansize: self.cansize = cansize #include special formatting

class save_propeller(data):
    def __init__(self,dataframe, name):
        '''storage for propeller dataframe, may store xteristic
        information about the propeller in the future'''
        self.dataframe = dataframe
        self.name = name

class save_wing(data):
    def __init__(self, span):
        '''storage for wing parameters and xteristic information
        which may include date of creation'''
        self.span = span
        #include code to compute files into xml format
    def oswald(self):
        pass

