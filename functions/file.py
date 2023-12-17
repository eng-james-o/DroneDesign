from .text import strip
import re

SPACE = '\s+'
rpm = r'PROP RPM = (\d+)' #to mark beginning of a table in the file
nan = '-NaN'

def load(filename):
    '''open the full file and load it into a list of lines'''
    with open(filename) as file_wrapper:
        file_str = file_wrapper.read()

    #list of lines, each line is a single string
    file_str_list = file_str.split(sep='\n')
    
    #remove blank lines
    file_str_list = [re.sub('-NaN',' NaN',line) for line in file_str_list]
    file_str_list = [re.sub(SPACE,' ',strip(line)) for line in file_str_list if not line.isspace()]
    
    del file_str_list[-1]#delete trailing empty space
    
    return file_str_list

def match(file_contents, propfile=None):
    '''find matches of rpm in a file and load into a list'''
    matches = list()
    for line in file_contents:
        match = re.search(rpm, line)
        if match:
            matches.append((file_contents.index(line), match.group(1)))
    return matches
