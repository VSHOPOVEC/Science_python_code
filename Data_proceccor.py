import re
import numpy as np
from sympy.stats import Expectation


class DataProcessor:
    def __init__(self, normalize_const, amount_of_arr, file_path):
        self.unsorted_times = []
        self.unsorted_points = []
        self.sorted_times = []
        self.sorted_points = []
        self.average_points = []
        self.average_time = []
        self.amount_of_arr = amount_of_arr
        self.file_path = file_path

    def to_process_data(self):
        self.load_file()
        self.funk_average_points()
        self.funk_average_time()

    def load_file(self):
        try:
            with open(self.file_path) as file:
                lines = file.readlines()
                self.unsorted_times = []
                self.unsorted_points = []
                pattern = r'\s*?(?P<name>\b\d+\.\d+e[-,+]\d+\b|\bNaN\b)\s+'
                for line in lines:
                    sub_list = re.findall(pattern, line)
                    if sub_list[0] != 'NaN' and sub_list[2] != 'NaN':
                        self.unsorted_times.append(sub_list[0])
                        self.unsorted_points.append(float(sub_list[2]))

                temp_dict = {}
                for time, point in zip(self.unsorted_times, self.unsorted_points):
                    if time not in temp_dict:
                        temp_result = []
                        temp_dict[time] = temp_result
                        temp_result.append(point)
                    else:
                        temp_dict[time].append(point)
                times = list(temp_dict.keys())
                self.sorted_points = list(temp_dict.values())
                self.sorted_times = [float(time) for time in times]
        except Exception as e:
            print(e)

    def funk_average_points(self):
        len_time_arr = len(self.sorted_points) - 1
        self.average_points = list(
            np.concatenate([self.sorted_points[index1] for index1 in range(index2, self.amount_of_arr + index2)]).tolist()
            for index2 in range(0, len_time_arr - self.amount_of_arr)
        )

    def funk_average_time(self):
        len_time_arr = len(self.sorted_times) - 1
        temp_list_time = [np.mean(self.sorted_times[0 + index: self.amount_of_arr + index]) for index in
                          range(0, len_time_arr - self.amount_of_arr)]
        self.average_time = np.array([float(x) for x in temp_list_time])
