import numpy as np

import Processing_wind_flow
import Data_loader
import Normalize_data
import Appr_data


#const_normal = 10

#name_of_files = [ "F27_data_arr.dat", "F30_data_arr.dat", "F32_data_arr.dat", "F35_data_arr.dat", "F37_data_arr.dat", "F40_data_arr.dat", "F42_data_arr.dat", "F45_data_arr.dat", "F47_data_arr.dat", "F50_data_arr.dat"]

#num_of_files = [27,30,32,35,37,40,42,45,47,50]

# def get_value(r_input):
#     data = {
#         5: 2.78, 6: 2.57, 7: 2.45, 8: 2.37, 9: 2.31, 10: 2.26,
#         11: 2.23, 12: 2.20, 13: 2.18, 14: 2.16, 15: 2.15,
#         16: 2.13, 17: 2.12, 18: 2.11, 19: 2.10, 20: 2.093,
#         25: 2.064, 30: 2.045, 35: 2.032, 40: 2.023, 45: 2.016,
#         50: 2.009, 60: 2.001, 70: 1.996, 80: 1.991, 90: 1.987,
#         100: 1.984, 120: 1.980
#     }
#
#     if r_input <= 20:
#         return data.get(r_input, 2.78)
#
#     keys = sorted(data.keys())
#     closest_key = min(keys, key=lambda x: abs(x - r_input))
#     return data[closest_key]


def processing_the_result(limit_of_thikness, limit_of_time, amount, normalize_const,file_path):
    try:
       sorted_points, sorted_times, unsorted_points, unsorted_times = Data_loader.load_file(file_path)  # разделяем данные на разные массивы
       average_times = Data_loader.funk_average_times(amount, sorted_times)  # также делаем со временем и находим среднее
       time_mask = np.array([limit_of_time > time for time in average_times])
       average_times = (np.array(average_times)[time_mask])

       mask_sorted_points = [np.array([limit_of_thikness > item for item in sub_list_points]) for sub_list_points in sorted_points]
       sorted_points = [np.array(arr)[mask_temp] for arr, mask_temp in zip(sorted_points, mask_sorted_points)]
       average_points = Data_loader.funk_average_points(amount, sorted_points)

       normalize_data, value_data = Normalize_data.to_normalize_list_data(normalize_const, average_points)  # нормируем lgyy

       y_funk_of_probability_list, x_funk_of_probability_list, check_wait_list, dispersion_list, sigma_list, nu_list = Appr_data.to_get_funk_of_prob_for_all(normalize_data)

       check_wait_list_correct = [Normalize_data.to_return_data(check_wait, value[0], value[1], normalize_const) for check_wait, value in zip(check_wait_list, value_data)]

       check_wait = np.array(check_wait_list_correct)[time_mask]


       dispersion = np.array(dispersion_list)[time_mask]

       sigma = np.array(sigma_list)[time_mask]
       nu = np.array(nu_list)[time_mask]

       return (check_wait,dispersion), (average_times, average_points), (unsorted_times, unsorted_points), (nu, sigma), (sorted_points, sorted_times)
    except Exception as e:
        return ([],[]),([],[]),([],[]),([],[]),([],[])


#def processing_the_result(file_path, limit_of_thikness, limit_of_time, amount_of_array):
#    unsorted_times, unsorted_points, sorted_time, sorted_points = load_file(file_path)
#   sorted_points = average_points(sorted_points, amount_of_array)
#    sorted_time = average_time(sorted_time, amount_of_array)
#
#    point_mask = [np.array([limit_of_thikness > temp_item for temp_item in item]) for item in points]
#    points = [np.array(arr)[mask_temp] for arr, mask_temp in zip(points, point_mask)]
#    time_mask = np.array([limit_of_time > time for time in times])
#    times = times[time_mask]
#    normalize_points = [to_normalize_data(item)[0] for item in points]  # Value of points
#    min_max_normalize_points = [to_normalize_data(item)[1] for item in points]  # Value of max and min in each array
#    funk_of_res_for_all_arrays = [to_get_funk_of_prob(normal, val_normal) for normal, val_normal in zip(normalize_points, min_max_normalize_points)]

#    check_wait = [item[2] for item in funk_of_res_for_all_arrays]
#    check_wait = np.array(check_wait)[time_mask]
#    dispersion = [item[3] for item in funk_of_res_for_all_arrays]
#    dispersion = np.array(dispersion)[time_mask]
#   sigma = [item[4] for item in funk_of_res_for_all_arrays]
 #   sigma = np.array(sigma)[time_mask]
 #   nu = [item[5] for item in funk_of_res_for_all_arrays]
 #   nu = np.array(nu)[time_mask]
#
#    return times, dispersion, check_wait, points, times_c, points_c, sigma, nu, curr_name




# def liner_appr_of_end(file_path_, path_to_save, amount_of_arr):
#     appr_coeff_b = []
#     list_iter = [int(ind) for ind in range(3,amount_of_arr)]
#     for amount in list_iter:
#        time, _, check_wait, *_, sigma,nu, local_name = processing_the_result(file_path_, 10,10,amount)
#        try:
#           tm_0, tm_1, tm_2 = time[0], time[1], time[2]
#           ch_w0, ch_w1, ch_w2 = check_wait[0], check_wait[1],check_wait[2]
#           tm_list = [tm_0,tm_1,tm_2]
#           ch_list = [ch_w0,ch_w1,ch_w2]
#           params = liner_func_fit(tm_list,ch_list)
#           a, b = params[0]
#        except IndexError:
#            try:
#               tm_0, tm_1 = time[0], time[1]
#               ch_w0, ch_w1  = check_wait[0], check_wait[1]
#               a = (ch_w1 - ch_w0)/(tm_1 - tm_0)
#               b = ch_w0 - tm_0 * a
#            except IndexError:
#                list_iter_curr = [int(ind) for ind in range(3, amount)]
#                plt.plot(list_iter_curr, appr_coeff_b)
#                plt.title("Начальная толщина пленки от количества массивов" + file_path_)
#                plt.grid()
#                plt.savefig(path_to_save + str(local_name) + ".pdf")
#                plt.close()
#                print("The program ended early")
#                return appr_coeff_b
#        appr_coeff_b.append(b)
#     plt.plot(list_iter,appr_coeff_b)
#     plt.title("Начальная толщина пленки от количества массивов" + file_path_)
#    plt.grid()
#    plt.savefig(path_to_save + str(local_name) + ".pdf")
#    plt.close()
#    return appr_coeff_b

# def plot_error(file_path_):
#    *_, sigma_,nu_,_ = processing_the_result(file_path_, 10,10,5)
#    x_list_ = np.arange(0, 10, 0.01)
#    sigma_ = [sigma_]
#    nu_ = [nu_]
#    print(sigma_)
#
#    for sig, n in zip(sigma_,nu_):
#        y_list_ = [erf_func(x,sig,n) for x in x_list_]
#        plt.figure(figsize=(40, 30))
#        plt.plot(x_list_,y_list_)
#        plt.show()
#
#
# def plot_liner_appr_of_end(path_of_arr, path_file_to_save, amount_of_averaging):
#    num = 3 #minimal arr_of_appr
#    h0_list = [liner_appr_of_end(name, path_file_to_save, amount_of_averaging) for name in path_of_arr]
#    h0_list_sorted = [[curr_list[index] for curr_list in h0_list] for index in range(0,len(h0_list[0]))]
#    for item in h0_list_sorted:
#       plt.plot(num_of_files, item)
#       plt.scatter(num_of_files,item)
#       plt.grid()
#       plt.savefig(path_file_to_save + "file_" + str(num) + ".pdf")
#       plt.close()
#       num += 1
#    return h0_list_sorted,

#plot_liner_appr_of_end(name_of_files, "/home/mikhailm/Documents/Python_Science_App/Начальная толщина от количества массивов/",6)