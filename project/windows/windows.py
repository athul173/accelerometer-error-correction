import pandas as pd


def threshold(chunks):
    #combinedstdarray = [[0, 0, 0]]
    #modarray = [[0]]
    max_threshold = [[0]]
    for index, chunk in enumerate(chunks):
        if index > 4850 and index < 5400:
            x_std = pd.DataFrame.std(chunk[0])
            y_std = pd.DataFrame.std(chunk[1])
            z_std = pd.DataFrame.std(chunk[2])
            windowrep = max(x_std, y_std, z_std)
        # if x_std < threshold and y_std < threshold and z_std < threshold:
            # for i in chunk.itertuples():
            #     mod = math.sqrt(math.pow(
            #         i[1], 2) + math.pow(i[2], 2) + math.pow(i[3], 2))
            #     modarray.append([mod])
            #combinedstdarray.append([x_std, y_std, z_std])
            max_threshold.append([windowrep])

    # print(*max_threshold)
    threshold = max(max_threshold)
    print("Maximum threshold is: " + str(threshold[0]))
    # plot_array = np.array(modarray[1:])
    # plt.plot(plot_array, 'o')
    # plt.xlabel('Time')
    # plt.ylabel('|Acceleration|')
    # plt.show()

    return float(threshold[0])


def nonmovement(chunks):
    max_std = threshold(chunks)
    print('Calculating non movement windows')
    nmw_array = []
    for chunk in pd.read_csv('./Data/GT3X+ (01 day)RAW.csv', chunksize=300,
                             header=None):
        x_std = pd.DataFrame.std(chunk[0])
        y_std = pd.DataFrame.std(chunk[1])
        z_std = pd.DataFrame.std(chunk[2])
        if x_std < max_std and y_std < max_std and z_std < max_std:
            for i in chunk.itertuples():
                nmw_array.append([i[1], i[2], i[3]])

    # removing all zero values used
    print("Removing all zero values")
    nmw_data = pd.DataFrame(nmw_array, columns=['x', 'y', 'z'])
    nmw_data = nmw_data.loc[(nmw_data != 0).any(axis=1)]
    return nmw_data
