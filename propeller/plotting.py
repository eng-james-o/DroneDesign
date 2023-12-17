#the functions defined here only work on MplWidget
'''write code to monitor the plots drawn already in an instance
of this class, such that upon calling draw when there,
it would
automatically generate a second set of axes, also, to clear the
canvas once there is a plot on it and draw is called again'''
'''shade the area where the efficiency falls within a useful
range of values and get the rpm or j for that range'''

'this class should also automatically handle the legends'
'''error handling loop to prevent crashing, and catching variables
to use for error assessment'''
'''paint the inside of searchbutton black to look like the pyplot
toolbuttons'''

class propPlotter:
    '''a class that handles the plotting for the propeller'''
    def __init__(self, widget):
        self.parent = widget
        self._lines = dict()#temporary list of lines to be drawn

#-----------fuller broader functions (wrap smaller functions)-------

    def draw(self, x, y_list, df, lbl=['Thrust','Pe'], grid=True):
        #if there is no line in the axis

        if len(self._lines) == 0:
            #there is no existing plot on the canvas
            for index,var in enumerate(y_list):
                #for each y supplied, plot and store the line
                if var == 'Pe':
                    #create new axis for the efficiency
                    if self.parent.second_axis==False:
                        #if the second axis has not been created
                        self.new_ax()
                        self.parent.second_axis=True
                    line = self.plot2(x, var, df, var)
                    self.parent.canvas.axes2.tick_params(axis='y',labelcolor='tab:green')
                else:
                    #if the variable is not efficiency
                    line = self.plot(x, var, df, var)
                self._lines[lbl[index]] = line[0]
            #print(self._lines)
        else:
            #canvas is not empty, therefore update all the lines
            for label in self._lines:
                #we need to update each line with its matching data
                line = self._lines[label]
                #print(line)
                line.set_ydata(df[label])
#after updating line, find means to update the axis too
#to adjust to accomodate the new line
            #print(self._lines)
        self.tight()
        self.legend(list(self._lines.values()), y_list)
        self.grid(grid)
        #self.show()
        return self._lines.values()

    def reset(self):
        self.clear_canvas()
        #empty the lines
        self._lines = dict()
        #print(self._lines),
        try:
            self.clear_canvas_ax2()
        except:
            pass

#-----------smaller specific functions--------------------------

    def plot(self, x_name, y_name, df, label):
        return self.parent.plot(x_name, y_name, df, label)

    def plot2(self, x_name, y_name, df, label):
        return self.parent.plot2(x_name, y_name, df, label)

    def new_ax(self):
        return self.parent.new_ax()

    def show(self):
        return self.parent.show_plot()

    def legend(self, *args, **kwargs):
        '''should allow for custom legend'''
        return self.parent.legend(*args, **kwargs)

    def grid(self, use_grid:bool):
        return self.parent.grid(use_grid)

    def tight(self):
        return self.parent.tight()

    def clear_canvas(self):
        '''clear the canvas of the widget'''
        return self.parent.clear_canvas()

    def clear_canvas_ax2(self):
        return self.parent.clear_canvas2()
