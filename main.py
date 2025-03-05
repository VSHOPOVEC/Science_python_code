
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QDoubleSpinBox, QSpinBox, QInputDialog
import Processing_data, sys, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class MainWindow(QMainWindow):



    def __init__(self):
        super().__init__()
        self.file_path = None
        self.check_wait = None
        self.dispersion = None
        self.time = None
        self.x_line = 0.002
        self.y_line = 0.002
        self.amount_of_arr = 3

        #for_liner_appr
        self.bool_liner_appr = False
        self.a_coeff_liner_appr = None
        self.b_coeff_liner_appr = None

        #for_exp_appr
        self.bool_exp_appr = False
        self.a_coeff_exp_appr = None
        self.b_coeff_exp_appr = None
        self.c_coeff_exp_appr = None

        #for_poly

        self.bool_poly_appr = False
        self.a_coeff_poly_appr = None
        self.b_coeff_poly_appr = None
        self.c_coeff_poly_appr = None


        self.setWindowTitle("My Science App")
        self.setGeometry(0,0,1920,1080)
        self.btn1 = QPushButton("Open file", self)  # Сохраняем кнопку как атрибут класса
        self.btn2 = QPushButton("Process wind flow", self)
        self.btn3 = QPushButton("Save", self)
        self.btn4 = QPushButton("Cancel", self)


        self.btn5 = QPushButton("liner approximate", self)
        self.btn6 = QPushButton("exp approximate", self)
        self.btn7 = QPushButton("poly approximate", self)

        self.btn_process_1 = QDoubleSpinBox(self)
        self.btn_process_2 = QDoubleSpinBox(self)
        self.btn_val_amount = QSpinBox(self)

        self.btn_process_1.setDecimals(5)
        self.btn_process_2.setDecimals(5)

        self.btn_process_1.setSingleStep(10**-5)
        self.btn_process_2.setSingleStep(10**-5)

        self.btn_process_1.setValue(self.y_line)
        self.btn_process_2.setValue(self.x_line)
        self.btn_val_amount.setValue(self.amount_of_arr)




        self.btn_process_1.setPrefix("y: ")  # текст перед числом
        self.btn_process_2.setPrefix("x: ")
        self.btn_val_amount.setPrefix("Amount of arr:  ")



        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn5.setEnabled(False)
        self.btn6.setEnabled(False)
        self.btn7.setEnabled(False)

        self.figure = plt.figure()  # Создаем фигуру Matplotlib
        self.canvas = FigureCanvas(self.figure)  # Создаем холст для отображения графика

        main_layout = QVBoxLayout()
        sub_layout = QVBoxLayout()
        sub_layout2 = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn3)
        hbox.addWidget(self.btn4)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.btn_process_1)
        hbox2.addWidget(self.btn_process_2)
        hbox2.addWidget(self.btn_val_amount)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.btn5)
        vbox3.addWidget(self.btn6)
        vbox3.addWidget(self.btn7)

        sub_layout.addLayout(hbox2)
        sub_layout.addLayout(vbox)
        sub_layout.addLayout(hbox)

        sub_layout2.addLayout(vbox3, 1)
        sub_layout2.addLayout(sub_layout, 1)

        main_layout.addWidget(self.canvas)


        main_layout.addLayout(sub_layout2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Реализация кнопок
        self.btn1.clicked.connect(self.open_file)
        self.btn2.clicked.connect(self.process_the_result)
        self.btn3.clicked.connect(self.saving_result)
        self.btn4.clicked.connect(self.cancel)
        self.btn5.clicked.connect(self.appr)
        self.btn6.clicked.connect(self.exp)
        self.btn7.clicked.connect(self.poly)

        self.btn_process_1.valueChanged.connect(self.change_y)
        self.btn_process_2.valueChanged.connect(self.change_x)
        self.btn_val_amount.valueChanged.connect(self.change_arr_amount)


    def change_arr_amount(self, value):
        self.amount_of_arr = value
        self.to_plot()

    def change_x(self, value_x):
        self.x_line = value_x
        self.to_plot()

    def change_y(self, value_y):
        self.y_line = value_y
        self.to_plot()

    def open_file(self):
        # Фильтр для отображения только .dat файлов
        file_filter = "Data Files (*.dat);;All Files (*)"
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        if self.file_path:
           self.btn2.setEnabled(True)
           self.btn3.setEnabled(True)
           self.btn1.setEnabled(False)
        self.process_the_result()

    def process_the_result(self):
        self.btn5.setEnabled(True)
        self.btn6.setEnabled(True)
        self.btn7.setEnabled(True)
        self.to_plot()


    def to_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(211)
        script_result = BackEndPythonApp.processing_the_result(self.file_path, self.y_line, self.x_line, self.amount_of_arr)
        times, dispersion, check_wait, points, times_c, points_c,sigma, nu, name = script_result
        self.check_wait = check_wait
        self.dispersion = dispersion
        self.time = times

        ax.plot(times, check_wait)

        ax.axhline(y = self.y_line, xmin = 0, xmax = 1)
        ax.axvline(x = self.x_line, ymin = 0, ymax = 1)
        ax.scatter(times_c, points_c)
        ax.grid()

        ax1 = self.figure.add_subplot(212)
        ax1.plot(times, check_wait)
        if self.bool_liner_appr:
            try:
               x = np.array([0,max(self.time)])
               y = x*self.a_coeff_liner_appr + np.array([1,1])*self.b_coeff_liner_appr
               ax1.plot(x , y)
            except Exception:
                pass

        elif self.bool_exp_appr:
            try:
               x = np.arange(0,max(self.time), 0.0001)
               x_one = np.ones(np.size(x))
               y = self.a_coeff_exp_appr*(np.exp(1000*x)) + x_one*self.b_coeff_exp_appr
               ax1.plot(x, y)
            except Exception:
                pass

        elif self.bool_poly_appr:
            try:
               x = np.arange(0, max(self.time), 0.0001)
               x_one = np.full(np.size(x), self.c_coeff_poly_appr)
               y = (x ** (2*self.a_coeff_poly_appr)) + (x**(2*self.b_coeff_poly_appr + 1))  + x_one
               ax1.plot(x, y)
            except ValueError:
                pass
        ax1.grid()

        self.canvas.draw()

    def saving_result(self):
        file_filter = "PNG Files (*.png);;PDF Files (*.pdf);;All Files (*)"
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить график", "", file_filter)

        # Если пользователь отменил сохранение
        if not file_path:
            print("Сохранение графика отменено.")
            return

        try:
            # Сохраняем график в файл
            self.figure.savefig(file_path)

            directory = os.path.dirname(file_path)

            # Создаем файл .dat в той же директории
            filename, _ = QInputDialog.getText(self, "Введите название файла",
                                                "Введите название файла (без расширения):")
            dat_filepath = os.path.join(directory, filename)

            # Данные для сохранения в файл .dat
            # Введите свои данные сюда
            data_to_save = []
            if self.bool_liner_appr:
               data_to_save = [self.a_coeff_liner_appr, self.b_coeff_liner_appr]
            elif self.bool_poly_appr:
               data_to_save = [self.a_coeff_poly_appr, self.b_coeff_poly_appr, self.c_coeff_poly_appr]
            elif self.bool_exp_appr:
                data_to_save = [self.a_coeff_exp_appr, self.b_coeff_exp_appr, self.c_coeff_exp_appr]
            # Сохраняем данные в файл .dat с точностью до 6 знаков после запятой
            with open(dat_filepath, 'w') as file:
                for x in data_to_save:
                    file.write(f"{x:.6e}\n")
            print(f"График успешно сохранен в файл: {file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении графика: {e}")

    def cancel(self):
        # Сброс состояния приложения
        self.figure.clear()
        self.file_path = None  # Сбрасываем путь к файлу
        self.btn2.setEnabled(False)  # Деактивируем кнопку "Process"
        self.btn3.setEnabled(False)  # Деактивируем кнопку "Save"
        self.btn5.setEnabled(False)
        self.btn6.setEnabled(False)
        self.btn7.setEnabled(False)
        self.btn1.setEnabled(True)
        self.canvas.draw()

    def appr(self):
        param, _ = BackEndPythonApp.liner_func_fit(self.time, self.check_wait)
        self.a_coeff_liner_appr = param[0]
        self.b_coeff_liner_appr = param[1]
        self.bool_liner_appr = True
        self.bool_exp_appr = False
        self.bool_poly_appr = False
        self.to_plot()

    def exp(self):
        param,_ = BackEndPythonApp.exp_func_fit(self.time, self.check_wait)
        self.a_coeff_exp_appr = param[0]
        self.b_coeff_exp_appr = param[1]

        self.bool_exp_appr = True
        self.bool_liner_appr = False
        self.bool_poly_appr = False
        self.to_plot()


def app_func():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app_func()

