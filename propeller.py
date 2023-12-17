from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout,QWidget
from PyQt5.QtWidgets import QSlider, QLabel, QRadioButton
from PyQt5.QtCore import Qt
from mplwidget import MplWidget
class propeller(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        #self.InitUI()
        #self.bind()

    def InitUI(self):
        self.header = QLabel('EFF, Ct, Cp vs RPM', self)
        self.widget = MplWidget(self)
        self.rpmSlider = QSlider(Qt.Horizontal,self)

        self.optionLayout = QHBoxLayout()
        self.option_rpm = QRadioButton('rpm')
        self.option_J = QRadioButton('J')
        self.optionLayout.addWidget(self.option_rpm)
        self.optionLayout.addWidget(self.option_J)

        self.rpm_value = QLabel(self)
        self.max_eff = QLabel(self)
        self.max_eff_J = QLabel(self)

        self.formLayout = QVBoxLayout()
        self.formLayout.addWidget(self.header)
        #self.formLayout.addChildWidget(self.widget)
        self.formLayout.addWidget(self.rpmSlider)
        self.formLayout.addLayout(self.optionLayout)

        self.setLayout(self.formLayout)
        self.bind()
    def setValues(self):
        self.rpm_value.setText('"1000" rpm')
    def getRpm(self):
        #self.rpm = self.rpm_available[self.rpmSlider.value()]
        pass
    def bind(self):
        self.rpmSlider.sliderReleased.connect(self.getRpm)
        self.rpmSlider.valueChanged.connect(self.getRpm)
        #self.rpmSlider.setMaximum(len(self.rpm_available))
