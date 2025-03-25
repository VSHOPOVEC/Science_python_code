import re
import numpy as np
from sympy.logic.utilities import load_file
from sympy.stats import Expectation


def load_file(file_path):
    try:
        with open(file_path) as file:
            lines = file.readlines()
            unsorted_times = []
            unsorted_points = []
            pattern = r'\s*?(?P<name>\b\d+\.\d+e[-,+]\d+\b|\bNaN\b)\s+'
            for line in lines:
                sub_list = re.findall(pattern, line)
                if sub_list[0] != 'NaN' and sub_list[2] != 'NaN':
                    unsorted_times.append(sub_list[0])
                    unsorted_points.append(float(sub_list[2]))
            temp_dict = {}
            for time, point in zip(unsorted_times, unsorted_points):
                if time not in temp_dict:
                    temp_result = []
                    temp_dict[time] = temp_result
                    temp_result.append(point)
                else:
                    temp_dict[time].append(point)
            times = list(temp_dict.keys())
            unsorted_times = list(float(time) for time in unsorted_times)
            sorted_points = list(temp_dict.values())
            sorted_times = [float(time) for time in times]
            sorted_times, sorted_points = zip(*(sorted(zip(sorted_times, sorted_points))))
        return sorted_points, sorted_times, unsorted_points, unsorted_times
    except Exception as e:
        print(e)

def funk_average_points(amount_of_arr, sorted_points):
    len_time_arr = len(sorted_points) - 1
    average_points = list(
        np.concatenate([sorted_points[index1] for index1 in range(index2, amount_of_arr + index2)]).tolist()
        for index2 in range(0, len_time_arr - amount_of_arr)
    )
    return average_points

def funk_average_times(amount_of_arr, sorted_times):
    len_time_arr = len(sorted_times) - 1
    temp_list_time = [np.mean(sorted_times[0 + index: amount_of_arr + index]) for index in
                        range(0, len_time_arr - amount_of_arr)]
    average_time = np.array([float(x) for x in temp_list_time])
    return average_time
