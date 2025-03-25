from PyQt5 import QtWidgets, uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

from ProcessingWindFlow import reader

class ProcessingFlow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.position_arr, self.column_time, self.column_speed, self.column_arr = [],[],[],[]
        self.dates = []

        self.setup_ui()

        self.open_button.clicked.connect(self.read_file)
        self.compose_button.clicked.connect(self.compose_graphic)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvasLayout.addWidget(self.canvas)


    def to_plot(self):
        self.figure.clear()
        fig = self.figure.add_subplot(111)
        mean_speed = [float(np.mean(item_s)) for item_s in self.column_speed]
        std_speed = [float(np.std(item_s)) for item_s in self.column_speed]
        fig.errorbar(mean_speed, self.position_arr, xerr=std_speed, fmt='o', ecolor='r', capsize=5, label='Данные с ошибками')
        fig.plot(mean_speed, self.position_arr)
        fig.set_title(str(self.file_path))  # Название графика
        fig.set_xlabel("Velocity")  # Подпись оси X
        fig.set_ylabel("Position")
        fig.grid()
        self.canvas.draw()


    def to_plot_general(self):
        self.figure.clear()
        fig = self.figure.add_subplot(111)
        speed_2d_arr = [[float(np.mean(item_s)) for item_s in speed] for speed in self.column_speed]
        for pos_item, item in zip(self.position_arr, speed_2d_arr):
            plt.plot(item, pos_item)
            plt.scatter(item, pos_item)
        fig.set_title("Compose graphic")
        fig.set_xlabel('Speed')
        fig.set_ylabel('Position')
        fig.grid()
        self.canvas.draw()



    def read_file(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open_data", "All Files(*);;Text Files(*.txt)", "")
        if self.file_path:
            self.position_arr, self.column_time, self.column_speed, self.column_arr = reader(self.file_path)
            self.to_plot()


    def compose_graphic(self):
        self.file_path,_ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open_data", "All Files(*);;Text Files(*.txt)", "")
        if self.file_path:
            self.position_arr = []; self.column_time = []; self.column_speed = []; self.column_arr = []
            for path in self.file_path:
               data = reader(path)
               self.position_arr.append(data[0]); self.column_time.append(data[1]); self.column_speed.append(data[2]); self.column_arr.append(data[3])
        self.to_plot_general()





    def setup_ui(self):
        try:
           uic.loadUi("processing_wind_flow.ui", self)
        except Exception as e:
            print(e)
