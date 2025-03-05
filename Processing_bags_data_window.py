import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

class ProccesingFlow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()



    def setup_ui(self):
        try:
            uic.loadUi("proccesing_bag_data.ui",self)
        except Exception as e:
            print(e)
