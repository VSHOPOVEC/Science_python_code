
from PyQt5 import QtWidgets
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import Processing_data


class ApproximateWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        try:
           uic.loadUi("approximate_window.ui", self)
        except Exception as e:
            print(e)





class ProccesingBags(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.amount_of_arr = 3
        #Будет заполнено в результате выполнения программы open
        self.Data_from_file = []

        self.x_line = 0.005
        self.y_line = 0.005

        self.normalize_const = 10

        self.approximate_window = None

        self.setup_ui()


        self.open_button.clicked.connect(self.open)
        self.save_button.clicked.connect(self.save)
        self.close_button.clicked.connect(self.close)
        self.approximate_button.clicked.connect(self.approximate)
        self.bool_list_status_button = [True, False, False, False]

        self.y_doublespin.setValue(self.y_line)
        self.x_doublespin.setValue(self.x_line)

        self.set_amount_arr.setValue(self.amount_of_arr)
        self.set_amount_arr.setMinimum(3)

        self.y_doublespin.setSingleStep(10**-5)
        self.x_doublespin.setSingleStep(10**-5)

        self.y_doublespin.setDecimals(5)
        self.x_doublespin.setDecimals(5)

        self.x_doublespin.valueChanged.connect(self.change_x)
        self.y_doublespin.valueChanged.connect(self.change_y)
        self.set_amount_arr.valueChanged.connect(self.set_amount)

        self.y_doublespin.setPrefix("y: ")  # текст перед числом
        self.x_doublespin.setPrefix("x: ")

        self.figure_1 = plt.figure()
        self.figure_2 = plt.figure()
        self.graphic_1 = FigureCanvas(self.figure_1)
        self.graphic_2 = FigureCanvas(self.figure_2)

        self.canvasLayout.addWidget(self.graphic_1)
        self.canvasLayout.addWidget(self.graphic_2)
    #TECHNICAL FUNK
    def status_button(self):
        self.open_button.setEnable(self.bool_list_status_button[0])
        self.save_button.setEnable(self.bool_list_status_button[1])
        self.close_button.setEnable(self.bool_list_status_button[1])
        self.approximate_button.setEnable(self.bool_list_status_button[1])

    def find_source(self):
        try:
           self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Укажите путь")
           if self.file_path:
               self.bool_list_status_button = [not status for status in self.bool_list_status_button]
        except Exception as e:
            print(e)


    def open(self):
        self.find_source()
        self.to_plot()

    def set_amount(self, value_arr):
        self.amount_of_arr = value_arr
        self.to_plot()

    def to_plot(self):
        self.figure_1.clear()
        self.figure_2.clear()
        
        data = Processing_data.processing_the_result(self.y_line, self.x_line, self.amount_of_arr, self.normalize_const, self.file_path)

        (check_wait_list_correct, dispersion), (average_times, average_points), (unsorted_times, unsorted_points), (nu, sigma), (sorted_points, sorted_times) = data

        self.Data_from_file = [
            ("check_wait_list_correct", check_wait_list_correct), ("dispersion", dispersion), ("average_times", average_times), ("average_points", average_points), ("unsorted_times", unsorted_times),
            ("unsorted_points", unsorted_points), ("nu", nu), ("sigma", sigma), ("sorted_points", sorted_points), ("sorted_times", sorted_times)
        ]


        fig_2 = self.figure_2.add_subplot(111)
        fig_1 = self.figure_1.add_subplot(111)
        fig_1.scatter(unsorted_times, unsorted_points)
        fig_1.scatter(average_times, check_wait_list_correct)
        fig_2.scatter(average_times, check_wait_list_correct)

        fig_1.axhline(y=self.y_line, xmin=0, xmax=1)
        fig_1.axvline(x=self.x_line, ymin=0, ymax=1)

        self.graphic_2.draw()
        self.graphic_1.draw()

    def close(self):
        pass

    def approximate(self):
        self.approximate_window = ApproximateWindow()
        self.approximate_window.show()

    def save(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Saving_data", "", "All Files(*);;Text Files(*.txt)")
        if file_path:
            with open(file_path, "w+") as file:  # Используем переменную file_path вместо строки "file_path"
                for ind in range(0, len(self.Data_from_file)):
                    name, subdata = self.Data_from_file[ind]
                    file.writelines(f"\t{name}\t\n")
                    for value in subdata:
                        file.writelines(f"\t{str(value)}\t\n")
        else:
            print("")


    def change_x(self, value_x):
        self.x_line = value_x
        self.to_plot()

    def change_y(self, value_y):
        self.y_line = value_y
        self.to_plot()

    def setup_ui(self):
        try:
            uic.loadUi("proccesing_bag_data.ui",self)
        except Exception as e:
            print(e)
