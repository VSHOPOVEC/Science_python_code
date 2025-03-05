import numpy as np
from scipy.optimize import curve_fit
import math as mt
from scipy.special import erf

class ApproximateFunk:
    def __init__(self, arr_data_x, arr_data_y):
        self.arr_data_x = arr_data_x
        self.arr_data_y = arr_data_y
        self.params = []
        self.y_funk_of_probability = None
        self.x_funk_of_probability = None


    @staticmethod
    def erf_func(x, sigma, nu):
        eps = 0.00000000001
        return 1 / 2 + 1 / 2 * erf(np.log(x + eps) - nu) / (sigma * np.sqrt(2))

    @staticmethod
    def liner_func(x, a, b):
        return a * x + b

    @staticmethod
    def exp_func(x, a, b):
        return a * np.exp(x) + b

    def exp_func_fit(self, data_x, data_y):
        try:
            params = curve_fit(self.exp_func, data_x, data_y)
            self.params = params
        except Exception as e: print(e)

    def liner_func_fit(self, data_x, data_y):
        try:
           params = curve_fit(self.liner_func, data_x, data_y)
           self.params = params
        except Exception as e: print(e)

    def erf_func_fit(self, data_x, data_y):
        params = curve_fit(self.erf_func, data_x, data_y)
        sigma_fit, nu_fit = params[0]; sigma, nu = float(sigma_fit), float(nu_fit)
        try:
            check_wait = mt.exp(nu + (sigma ** 2) / 2); dispersion = (mt.exp(sigma ** 2) - 1) * mt.exp(2 * nu + sigma ** 2)
            self.params = (check_wait, dispersion, sigma, nu) #posle do vipolnenie programmi nujno normirovat', f posle vernut' obratno
        except Exception as e: print(e); self.params =  [0, 0, sigma, nu]

    def to_get_funk_of_prob(self, normalize_data): #IN ARGS HAVE TO BE NORMALIZE DATA
        bins = 100
        n_data = normalize_data
        max_value = max(normalize_data)
        edges = np.linspace(0, max_value, num=bins)
        num_points_into_interval = np.histogram(n_data, bins=edges)[0]
        total_sum_of_points = np.sum(num_points_into_interval)
        probability_to_be_in_interval = num_points_into_interval / total_sum_of_points
        self.y_funk_of_probability = np.cumsum(probability_to_be_in_interval); self.x_funk_of_probability = edges[:-1]
        self.erf_func_fit(self.x_funk_of_probability, self.y_funk_of_probability)