import numpy as np


class NormalizeData:
    def __init__(self, data, n_const):
        self.n_const = n_const
        self.data = data
        self.normalize_data = self.to_normalize_list_data(data)

    def __to_normalize_data(self, sublist_sorted_points):
        try:
            max_value = float(np.max(sublist_sorted_points))
            min_value = float(np.min(sublist_sorted_points))
            normal_list = np.array(
                [(item - min_value) / (max_value - min_value) * self.n_const for item in sublist_sorted_points])
            return normal_list, (min_value, max_value)
        except Exception as e:
            print(e); return None, (None, None)

    def to_normalize_list_data(self, list_sorted_points):
        self.normalize_data = [self.to_normalize_data(points) for points in list_sorted_points]
        return self.normalize_data

    def __to_return_data(self, sub_normalize_list):
        try:
            normal_list = sub_normalize_list[0];
            min_value, max_value = sub_normalize_list[1]
            returned_list = [item * (max_value - min_value) / self.n_const + min_value for item in normal_list]
            return returned_list
        except Exception as e:
            print(e)

    def to_return_list_of_data(self, normalize_list):
        return [self.to_return_data(normalize_sublist) for normalize_sublist in normalize_list]
