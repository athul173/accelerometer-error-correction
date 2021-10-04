import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import nmw_autocalibration
import calculations
import statistics
from mpl_toolkits import mplot3d

chunks = pd.read_csv('./Data/GT3X+ (01 day)RAW.csv', chunksize=300,
                     header=None)


def py_plotter(data):
    print("Starting Plotting")
    # chunks.plot()
    # plt.show()
    # initial_array = [[0, 0]]
    # for chunk in chunks.itertuples():
    #     print(chunk)
    #     y = math.sqrt(math.pow(
    #         chunk[1], 2) + math.pow(chunk[2], 2) + math.pow(chunk[3], 2))
    # # adder = pd.DataFrame([[chunk[0], y]], columns=["Time", "Acceleration"])
    #     initial_array.append([chunk[0], y])
    # df.append(adder, ignore_index=True)

    # df = pd.DataFrame({"Time": b[:, 0], "Acceleration": b[:, 1]})
    # print(df)
    # plot_array = np.array(initial_array)
    # plt.plot(plot_array[:, 0], plot_array[:, 1], 'o')
    # plt.xlabel('Time')
    # plt.ylabel("|Acceleration|")
    # plt.show()
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    zdata = []
    xdata = []
    ydata = []
    for column in data:
        if column == 'x':
            xdata.append(data[column])
        if column == 'y':
            ydata.append(data[column])
        if column == 'z':
            zdata.append(data[column])
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
    plt.show()


# def slope_finder():
#     length = np.random.random(10)
#     length.sort()
#     time = np.random.random(10)
#     time.sort()
#     slope, intercept = np.polyfit(np.log(length), np.log(time), 1)
#     print(slope)
#     plt.loglog(length, time, '--')
#     plt.show()


def non_movement_windows():
    max_std = 0.03473971042611789
    nmw_array = []
    for chunk in pd.read_csv('./Data/GT3X+ (01 day)RAW.csv', chunksize=300,
                             header=None):
        x_std = pd.DataFrame.std(chunk[0])
        y_std = pd.DataFrame.std(chunk[1])
        z_std = pd.DataFrame.std(chunk[2])
        if x_std < max_std and y_std < max_std and z_std < max_std:
            for i in chunk.itertuples():
                nmw_array.append([i[1], i[2], i[3]])

    # removing values used for initialization
    nmw_array.pop(0)

    # removing all non-zero values used
    nmw_data = pd.DataFrame(nmw_array, columns=['x', 'y', 'z'])
    nmw_data = nmw_data.loc[(nmw_data != 0).any(axis=1)]
    return nmw_data


coefficients = [0.5313294223962942,
                0.6198650701454193,
                0.5774567860341174,
                - 5.470634997090046e-11,
                - 7.208322062797556e-11,
                - 5.924211764451586e-11]
# nmw_autocalibration.curve_fitting(non_movement_windows())


def final_method():
    nmw_data = non_movement_windows()
    linear_transformed_data = []
    for tuples in nmw_data.itertuples():
        new_tuple = [tuples[1]*coefficients[3] + coefficients[0], tuples[2] *
                     coefficients[4] + coefficients[1], tuples[3]*coefficients[5] + coefficients[2]]
        linear_transformed_data.append(new_tuple)
    linear_transformed_data = pd.DataFrame(
        linear_transformed_data, columns=['x', 'y', 'z'])
    # old_mod = calculations.find_mod(nmw_data)
    # new_mod = calculations.find_mod(linear_transformed_data)
    # old_mean = statistics.mean(old_mod)
    # new_mean = statistics.mean(new_mod)
    # old_std = statistics.stdev(old_mod)
    # new_std = statistics.stdev(new_mod)
    py_plotter(linear_transformed_data)


final_method()
