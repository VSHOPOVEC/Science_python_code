
from PyQt5 import QtWidgets
from PyQt5 import uic
from Processing_bags_data_window import ProccesingBags
from Processing_wind_flow import ProcessingFlow

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.proccesing_flow.clicked.connect(self.processing_wind_flow_data)
        self.proccesing_bags.clicked.connect(self.processing_proccesing_bags_data)




    def setup_ui(self):
        try:
            uic.loadUi("entrance_window.ui",self)
        except Exception as e:
            print(e)


    def processing_wind_flow_data(self):
        self.flow_window = ProcessingFlow()
        self.flow_window.show()
        self.close()


    def processing_proccesing_bags_data(self):
        self.bag_window = ProccesingBags()
        self.bag_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
