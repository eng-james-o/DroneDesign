class propPlotter:
    def __init__(self,widget):
        self.parent = widget
        self._lines = dict()

    def draw(self, x, y, df, lbl, grid=True,axis=1):
        if axis == 1:
            plot = self.plot(x, y, df, lbl)
        else:
            plot = self.plot2(x, y, df, lbl)
        self.tight()
        self.show()
        return plot

    def reset(self):
        #print('reset called')
        self.clear_canvas()
        self._lines = dict()
        self.parent.canvas.axes2 = self.parent.canvas.axes.twinx()
        self.parent.second_axis=True
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
        #pass
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
