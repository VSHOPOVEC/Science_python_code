import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from sqlalchemy.sql.coercions import expect
from Processing_bags_data_window import ProccesingFlow

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
        pass

    def processing_proccesing_bags_data(self):
        self.sub_window = ProccesingFlow()
        self.sub_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
