# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 21:38:00 2020

@author: marti
"""

import numpy as np
import pandas as pd
import organised_data_module as od
import Data_Module as DM
import warnings
import matplotlib.pyplot as plt


def clean_seluxit_main(dataframes):
    """
    Extract and clean data from the main experiment.

    Parameters
    ----------
    dataframes : list of DataFrames
        list of dataframes from which the data needs to be extracted from.
        The DataFrames should contain data of mass, pressure, inclination, and
        temperature in that order.

    Returns
    -------
    df_list_clean : list of DataFrames
        list of DataFrames with extracted and cleaned data.

    """
    print('-----------------------------------------')
    print('Cleaning data from main experiment')
    print('-----------------------------------------\n')

    print('Constructing reference timestamps...')

    filename = 'dataframes/Experiment_seluxit_230420_modified.csv'
    df_experiment = pd.read_csv(filename, sep=';')

    mass_compare = np.zeros(len(df_experiment['mass']))
    for mass_index, mass in enumerate(
            df_experiment['mass'].to_numpy(dtype=object)):

        mass_edit = mass.replace(',', '.')
        mass_compare[mass_index] = float(mass_edit)

    timestamps = np.vstack(
        (df_experiment['starttid_UTC'][mass_compare < 1010],
         df_experiment['sluttid_UTC'][mass_compare < 1010]))

    timestamps_edit = np.full(timestamps.shape, '                       ')

    for i in range(len(timestamps_edit[0])):
        if i < 46:
            timestamps_edit[0][i] = '2020-04-23 ' + timestamps[0][i] + '.000'
            timestamps_edit[1][i] = '2020-04-23 ' + timestamps[1][i] + '.000'
        else:
            timestamps_edit[0][i] = '2020-04-24 ' + timestamps[0][i] + '.000'
            timestamps_edit[1][i] = '2020-04-24 ' + timestamps[1][i] + '.000'

    print('Resetting indexes in dataframes...')

    df_list_reset = []
    for df in dataframes:
        df_list_reset.append(df.reset_index())

    df_list_filtered = [pd.DataFrame(
        columns=df_list_reset[0].columns) for i in range(4)]

    # Filtrèr unødig masse data væk

    print('Removing unnecessary mass data...')

    k = 0
    for timestamp_index, timestamp in enumerate(df_list_reset[0]['timestamp']):
        for start_timestamp in timestamps_edit[0]:
            if start_timestamp <= timestamp <= start_timestamp[0:-4] + '.999' and timestamp != '2020-04-23 12:16:26.000' and timestamp != '2020-04-23 12:16:26.032':
                df_list_filtered[0].loc[k] = df_list_reset[0].loc[
                    timestamp_index]
                k += 1

    # Filtrèr data uden for forsøg væk

    print('Removing data outside of experiment intervals...')

    for df_index, df in enumerate(df_list_reset[1:4], 1):
        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):
            for j in range(len(timestamps_edit[0])):
                if timestamps_edit[0][j] <= timestamp <= timestamps_edit[1][j]:
                    df_list_filtered[df_index].loc[k] = df.loc[timestamp_index]
                    k += 1

    print('Removing duplicate data...')

    df_list_dupremoved = [pd.DataFrame(
        columns=df_list_filtered[0].columns) for i in range(4)]
    df_list_dupremoved[0] = df_list_filtered[0]

    for df_index, df in enumerate(df_list_filtered[1:4], 1):

        df_list_dupremoved[df_index].loc[0] = df.loc[0]
        k = 1
        for timestamp_index, timestamp in enumerate(df['timestamp'][1:], 1):
            if np.allclose(
                    df_list_dupremoved[df_index]['timestamp'].str.contains(
                        timestamp), False) is True:
                df_list_dupremoved[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Removing rogue data...\n')

    df_list_clean = [pd.DataFrame(
        columns=df_list_dupremoved[0].columns) for i in range(4)]
    df_list_clean[0] = df_list_dupremoved[0]

    for df_index, df in enumerate(df_list_dupremoved[1:4], 1):

        other_indices = [
            val for val in range(1, len(df_list_dupremoved[1:4])+1)]
        other_indices.remove(df_index)

        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):

            bool1 = False
            bool2 = False

            bool1_array = df_list_filtered[other_indices[0]]['timestamp'].str.contains(timestamp)
            bool2_array = df_list_filtered[other_indices[1]]['timestamp'].str.contains(timestamp)

            if np.allclose(bool1_array, False) is False:
                bool1 = True

            if np.allclose(bool2_array, False) is False:
                bool2 = True

            if bool1 is True and bool2 is True:
                df_list_clean[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Data cleaning done\n')

    return df_list_clean, df_list_filtered


def clean_seluxit_placement(dataframes):
    """
    Extract and clean data from placement experiment.

    dataframes : list of DataFrames
        list of dataframes from which the data needs to be extracted from.
        The DataFrames should contain data of mass, pressure, inclination, and
        temperature in that order.

    Returns
    -------
    df_list_clean : list of DataFrames
        list of DataFrames with extracted and cleaned data.

    """
    warnings.filterwarnings('ignore')

    print('-----------------------------------------')
    print('Cleaning data from placement experiment')
    print('-----------------------------------------\n')

    print('Constructing reference timestamps...')

    filename = 'dataframes/Experiment_seluxit_placement_modified.csv'
    df_experiment = pd.read_csv(filename, sep=';')

    timestamps = np.vstack(
        (df_experiment['starttid_UTC'], df_experiment['sluttid_UTC']))

    timestamps_edit = np.full(timestamps.shape, '                       ')

    for i in range(len(timestamps_edit[0])):
        timestamps_edit[0][i] = '2020-04-24 ' + timestamps[0][i] + '.000'
        timestamps_edit[1][i] = '2020-04-24 ' + timestamps[1][i] + '.000'

    print('Resetting indexes in dataframes...')

    df_list_reset = []
    for df in dataframes:
        df_list_reset.append(df.reset_index())

    df_list_filtered = [
        pd.DataFrame(columns=df_list_reset[0].columns) for i in range(4)]

    print('Removing unnecessary mass data...')

    k = 0
    for timestamp_index, timestamp in enumerate(df_list_reset[0]['timestamp']):
        for start_timestamp in timestamps_edit[0]:
            if start_timestamp <= timestamp <= start_timestamp[0:-4] + '.999':
                df_list_filtered[0].loc[k] = df_list_reset[0].loc[timestamp_index]
                k += 1

    print('Correcting mass data...')

    df_list_filtered[0][
        'data_number'].loc[df_list_filtered[0]['data_number'] == 275.4] = 275.9

    print('Removing data outside of experiment intervals...')

    for df_index, df in enumerate(df_list_reset[1:4], 1):
        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):
            for j in range(len(timestamps_edit[0])):
                if timestamps_edit[0][j] <= timestamp <= timestamps_edit[1][j]:
                    df_list_filtered[df_index].loc[k] = df.loc[timestamp_index]
                    k += 1

    print('Removing duplicate data...')

    df_list_dupremoved = [pd.DataFrame(
        columns=df_list_filtered[0].columns) for i in range(4)]
    df_list_dupremoved[0] = df_list_filtered[0]

    for df_index, df in enumerate(df_list_filtered[1:4], 1):

        df_list_dupremoved[df_index].loc[0] = df.loc[0]
        k = 1
        for timestamp_index, timestamp in enumerate(df['timestamp'][1:], 1):
            if np.allclose(
                    df_list_dupremoved[df_index]['timestamp'].str.contains(
                        timestamp), False) is True:
                df_list_dupremoved[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Removing rogue data...')

    df_list_clean = [pd.DataFrame(
        columns=df_list_dupremoved[0].columns) for i in range(4)]
    df_list_clean[0] = df_list_dupremoved[0]

    for df_index, df in enumerate(df_list_dupremoved[1:4], 1):

        other_indices = [
            val for val in range(1, len(df_list_dupremoved[1:4])+1)]
        other_indices.remove(df_index)

        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):

            bool1 = False
            bool2 = False

            bool1_array = df_list_filtered[other_indices[0]]['timestamp'].str.contains(timestamp)
            bool2_array = df_list_filtered[other_indices[1]]['timestamp'].str.contains(timestamp)

            if np.allclose(bool1_array, False) is False:
                bool1 = True

            if np.allclose(bool2_array, False) is False:
                bool2 = True

            if bool1 is True and bool2 is True:
                df_list_clean[df_index].loc[k] = df.loc[timestamp_index]
                k += 1
    
    print('Dividing dataset...\n')
    
    df_list_clean_middle = [
        pd.DataFrame(columns=df_list_clean[0].columns) for i in range(4)]
    df_list_clean_middle[0] = df_list_clean[0]
    
    df_list_clean_back = [
        pd.DataFrame(columns=df_list_clean[0].columns) for i in range(4)]
    df_list_clean_back[0] = df_list_clean[0]
    
    df_list_clean_front = [
        pd.DataFrame(columns=df_list_clean[0].columns) for i in range(4)]
    df_list_clean_front[0] = df_list_clean[0]
    
    df_list_clean_side1 = [
        pd.DataFrame(columns=df_list_clean[0].columns) for i in range(4)]
    df_list_clean_side1[0] = df_list_clean[0]
    
    df_list_clean_side2 = [
        pd.DataFrame(columns=df_list_clean[0].columns) for i in range(4)]
    df_list_clean_side2[0] = df_list_clean[0]

    middle_counter = 0
    back_counter = 0
    front_counter = 0
    side1_counter = 0
    side2_counter = 0
    
    for placement_index, placement in enumerate(df_experiment['placement']):

        if placement == 'middle':
            for df_index, df in enumerate(df_list_clean[1:4], 1):
                k = middle_counter
                for timestamp_index, timestamp in enumerate(df['timestamp']):
                    if timestamps_edit[0][placement_index] <= timestamp <= timestamps_edit[1][placement_index]:
                        df_list_clean_middle[df_index].loc[k] = df.loc[timestamp_index]
                        k += 1
            middle_counter = k
        
        elif placement == 'back':
            for df_index, df in enumerate(df_list_clean[1:4], 1):
                k = back_counter
                for timestamp_index, timestamp in enumerate(df['timestamp']):
                    if timestamps_edit[0][placement_index] <= timestamp <= timestamps_edit[1][placement_index]:
                        df_list_clean_back[df_index].loc[k] = df.loc[timestamp_index]
                        k += 1
            back_counter = k
            
        elif placement == 'front':
            for df_index, df in enumerate(df_list_clean[1:4], 1):
                k = front_counter
                for timestamp_index, timestamp in enumerate(df['timestamp']):
                    if timestamps_edit[0][placement_index] <= timestamp <= timestamps_edit[1][placement_index]:
                        df_list_clean_front[df_index].loc[k] = df.loc[timestamp_index]
                        k += 1
            front_counter = k

        elif placement == 'side1':
            for df_index, df in enumerate(df_list_clean[1:4], 1):
                k = side1_counter
                for timestamp_index, timestamp in enumerate(df['timestamp']):
                    if timestamps_edit[0][placement_index] <= timestamp <= timestamps_edit[1][placement_index]:
                        df_list_clean_side1[df_index].loc[k] = df.loc[timestamp_index]
                        k += 1
            side1_counter = k

        elif placement == 'side2':
            for df_index, df in enumerate(df_list_clean[1:4], 1):
                k = side2_counter
                for timestamp_index, timestamp in enumerate(df['timestamp']):
                    if timestamps_edit[0][placement_index] <= timestamp <= timestamps_edit[1][placement_index]:
                        df_list_clean_side2[df_index].loc[k] = df.loc[timestamp_index]
                        k += 1
        side2_counter = k
    
    
    print('Data cleaning done\n')

    return df_list_clean_middle, df_list_clean_back, df_list_clean_front, df_list_clean_side1, df_list_clean_side2


def clean_seluxit_hysteresis(dataframes):
    """
    Extract and clean data from hysteresis experiment.

    dataframes : list of DataFrames
        list of dataframes from which the data needs to be extracted from.
        The DataFrames should contain data of mass, pressure, inclination, and
        temperature in that order.

    Returns
    -------
    df_list_clean : list of DataFrames
        list of DataFrames with extracted and cleaned data.

    """
    print('-----------------------------------------')
    print('Cleaning data from hysteresis experiment')
    print('-----------------------------------------\n')

    print('Constructing reference timestamps...')

    timestamps = [['2020-04-24 12:45:53.000'], ['2020-04-24 12:49:55.000']]
    
    print('Resetting indexes in dataframes...')

    df_list_reset = []
    for df in dataframes:
        df_list_reset.append(df.reset_index())

    df_list_filtered = [pd.DataFrame(
        columns=df_list_reset[0].columns) for i in range(4)]

    print('Removing unnecessary mass data...')

    k = 0
    for timestamp_index, timestamp in enumerate(df_list_reset[0]['timestamp']):
        for start_timestamp in timestamps[0]:
            if start_timestamp <= timestamp <= start_timestamp[0:-4] + '.999':
                df_list_filtered[0].loc[k] = df_list_reset[0].loc[
                    timestamp_index]
                k += 1

    print('Removing data outside of experiment intervals...')

    for df_index, df in enumerate(df_list_reset[1:4], 1):
        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):
            for j in range(len(timestamps[0])):
                if timestamps[0][j] <= timestamp <= timestamps[1][j]:
                    df_list_filtered[df_index].loc[k] = df.loc[timestamp_index]
                    k += 1

    print('Removing duplicate data...')

    df_list_dupremoved = [pd.DataFrame(
        columns=df_list_filtered[0].columns) for i in range(4)]
    df_list_dupremoved[0] = df_list_filtered[0]

    for df_index, df in enumerate(df_list_filtered[1:4], 1):

        df_list_dupremoved[df_index].loc[0] = df.loc[0]
        k = 1
        for timestamp_index, timestamp in enumerate(df['timestamp'][1:], 1):
            if np.allclose(df_list_dupremoved[
                    df_index]['timestamp'].str.contains(
                        timestamp), False) is True:
                df_list_dupremoved[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Removing rogue data...\n')

    df_list_clean = [pd.DataFrame(
        columns=df_list_dupremoved[0].columns) for i in range(4)]
    df_list_clean[0] = df_list_dupremoved[0]

    for df_index, df in enumerate(df_list_dupremoved[1:4], 1):

        other_indices = [
            val for val in range(1, len(df_list_dupremoved[1:4])+1)]
        other_indices.remove(df_index)

        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):

            bool1 = False
            bool2 = False

            bool1_array = df_list_filtered[other_indices[0]]['timestamp'].str.contains(timestamp)
            bool2_array = df_list_filtered[other_indices[1]]['timestamp'].str.contains(timestamp)

            if np.allclose(bool1_array, False) is False:
                bool1 = True

            if np.allclose(bool2_array, False) is False:
                bool2 = True

            if bool1 is True and bool2 is True:
                df_list_clean[df_index].loc[k] = df.loc[timestamp_index]
                k += 1
    
    print('Data cleaning done\n')

    return df_list_clean


def clean_seluxit_overload(dataframes):
    """
    Extract and clean data from the overload experiment.

    Parameters
    ----------
    dataframes : list of DataFrames
        list of dataframes from which the data needs to be extracted from.
        The DataFrames should contain data of mass, pressure, inclination, and
        temperature in that order.

    Returns
    -------
    df_list_clean : list of DataFrames
        list of DataFrames with extracted and cleaned data.

    """
    print('-----------------------------------------')
    print('Cleaning data from overload experiment')
    print('-----------------------------------------\n')

    print('Constructing reference timestamps...')

    filename = 'dataframes/Experiment_seluxit_230420_modified.csv'
    df_experiment = pd.read_csv(filename, sep=';')

    mass_compare = np.zeros(len(df_experiment['mass']))
    for mass_index, mass in enumerate(
            df_experiment['mass'].to_numpy(dtype=object)):

        mass_edit = mass.replace(',', '.')
        mass_compare[mass_index] = float(mass_edit)

    timestamps = np.vstack(
        (df_experiment['starttid_UTC'][mass_compare > 1010],
         df_experiment['sluttid_UTC'][mass_compare > 1010]))

    timestamps_edit = np.full(timestamps.shape, '                       ')

    for i in range(len(timestamps_edit[0])):
        timestamps_edit[0][i] = '2020-04-23 ' + timestamps[0][i] + '.000'
        timestamps_edit[1][i] = '2020-04-23 ' + timestamps[1][i] + '.000'

    print('Resetting indexes in dataframes...')

    df_list_reset = []
    for df in dataframes:
        df_list_reset.append(df.reset_index())

    df_list_filtered = [pd.DataFrame(
        columns=df_list_reset[0].columns) for i in range(4)]

    # Filtrèr unødig masse data væk

    print('Removing unnecessary mass data...')

    k = 0
    for timestamp_index, timestamp in enumerate(df_list_reset[0]['timestamp']):
        for start_timestamp in timestamps_edit[0]:
            if start_timestamp <= timestamp <= start_timestamp[0:-4] + '.999' and timestamp != '2020-04-23 12:16:26.000' and timestamp != '2020-04-23 12:16:26.032':
                df_list_filtered[0].loc[k] = df_list_reset[0].loc[
                    timestamp_index]
                k += 1

    # Filtrèr data uden for forsøg væk

    print('Removing data outside of experiment intervals...')

    for df_index, df in enumerate(df_list_reset[1:4], 1):
        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):
            for j in range(len(timestamps_edit[0])):
                if timestamps_edit[0][j] <= timestamp <= timestamps_edit[1][j]:
                    df_list_filtered[df_index].loc[k] = df.loc[timestamp_index]
                    k += 1

    print('Removing duplicate data...')

    df_list_dupremoved = [pd.DataFrame(
        columns=df_list_filtered[0].columns) for i in range(4)]
    df_list_dupremoved[0] = df_list_filtered[0]

    for df_index, df in enumerate(df_list_filtered[1:4], 1):

        df_list_dupremoved[df_index].loc[0] = df.loc[0]
        k = 1
        for timestamp_index, timestamp in enumerate(df['timestamp'][1:], 1):
            if np.allclose(
                    df_list_dupremoved[df_index]['timestamp'].str.contains(
                        timestamp), False) is True:
                df_list_dupremoved[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Removing rogue data...\n')

    df_list_clean = [pd.DataFrame(
        columns=df_list_dupremoved[0].columns) for i in range(4)]
    df_list_clean[0] = df_list_dupremoved[0]

    for df_index, df in enumerate(df_list_dupremoved[1:4], 1):

        other_indices = [
            val for val in range(1, len(df_list_dupremoved[1:4])+1)]
        other_indices.remove(df_index)

        k = 0
        for timestamp_index, timestamp in enumerate(df['timestamp']):

            bool1 = False
            bool2 = False

            bool1_array = df_list_filtered[other_indices[0]]['timestamp'].str.contains(timestamp)
            bool2_array = df_list_filtered[other_indices[1]]['timestamp'].str.contains(timestamp)

            if np.allclose(bool1_array, False) is False:
                bool1 = True

            if np.allclose(bool2_array, False) is False:
                bool2 = True

            if bool1 is True and bool2 is True:
                df_list_clean[df_index].loc[k] = df.loc[timestamp_index]
                k += 1

    print('Data cleaning done\n')
    
    return df_list_clean


if __name__ == '__main__':

    df_list = od.import_seluxit()

    # df_list_main_cleaned, df_list_filtered = clean_seluxit_main(df_list)
    df_list_placement_middle, df_list_placement_back, df_list_placement_front, df_list_placement_side1, df_list_placement_side2 = clean_seluxit_placement(df_list)
    # df_list_overload_cleaned = clean_seluxit_overload(df_list)

    # %%
    
    data_dirty = od.unpack_to_arrays_seluxit(df_list)

    data_tuple_main = od.unpack_to_arrays_seluxit(
        df_list_filtered)
    
    data_tuple_main_cleaned = od.unpack_to_arrays_seluxit(
        df_list_main_cleaned)

    data_tuple_placement_cleaned_middle = od.unpack_to_arrays_seluxit(
        df_list_placement_middle)
    
    data_tuple_placement_cleaned_back = od.unpack_to_arrays_seluxit(
        df_list_placement_back)

    data_tuple_placement_cleaned_front = od.unpack_to_arrays_seluxit(
        df_list_placement_front)

    data_tuple_placement_cleaned_side1 = od.unpack_to_arrays_seluxit(
        df_list_placement_side1)

    data_tuple_placement_cleaned_side2 = od.unpack_to_arrays_seluxit(
        df_list_placement_side2)

    data_tuple_overload_cleaned = od.unpack_to_arrays_seluxit(
        df_list_overload_cleaned)

    # %% Remove top and bottom data
    
    data_temp = data_tuple_main_cleaned
    
    top_indices = np.where(data_temp[2][:, 1] < 40.5)[0]
    bottom_indices = np.where(data_temp[2][:, 1] > 85.5)[0]
    top_bottom_indices = np.concatenate((top_indices, bottom_indices, [3428]))

    data_top_bottom_removed = [data_temp[0]]

    for datalist in data_temp[1:4]:
        data_top_bottom_removed.append(
            np.delete(datalist, top_bottom_indices, axis=0))

    # od.plot_vs_time_init(
    #     data_top_bottom_removed[0],
    #     data_top_bottom_removed[1],
    #     data_top_bottom_removed[2],
    #     data_top_bottom_removed[3])

    # %% Plotting and saving

    data_final = data_tuple_placement_cleaned_middle

    MASS_SHORT = data_final[0]
    PRESSURE = data_final[1][:, 1]
    #INCLINATION_temp = data_final[2][:, 1]+abs(min(data_final[2][:, 1]))
    INCLINATION = (
        data_final[2][:, 1] - max(data_tuple_main_cleaned[2][:, 1]))/(
            min(data_tuple_main_cleaned[2][:, 1]) - max(data_tuple_main_cleaned[2][:, 1]))
    #INCLINATION = data_final[2][:,1]
    TEMPERATURE = data_final[3][:, 1]

    TIME = data_final[1][:, 0]
    MASS = od.extended_mass_array(MASS_SHORT[:, 1], MASS_SHORT[:, 0], TIME)

    DM.plot_vs_time(MASS, PRESSURE, INCLINATION, TEMPERATURE, TIME, time_unit = 'hours')
    # plt.savefig('datacleaning eksempler/data_main_clean.pdf')
    # Save cleaned data
    # SAVE_DATA = np.stack(
    # (TIME, MASS, PRESSURE, INCLINATION, TEMPERATURE), axis=1)
    # np.save('seluxit_overload_experiment.npy', SAVE_DATA)

    # %%
    
    data_final = data_tuple_main
    
    marksize = 1.5
    
    ax1 = plt.subplot(221)
    plt.plot(data_final[3][:, 0]/(60*60), data_final[3][:, 1], marker='o', linestyle='', markersize=marksize)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.title('Temperature')
    # plt.ylabel('°C')

    ax2 = plt.subplot(222, sharex=ax1)
    plt.plot(data_final[1][:, 0]/(60*60), data_final[1][:, 1], 'tab:orange', marker='o', linestyle='', markersize=marksize)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.title('Pressure')
    # plt.ylabel('?')

    ax3 = plt.subplot(223, sharex=ax1)
    plt.plot(data_final[2][:, 0]/(60*60), data_final[2][:, 1], 'tab:red', marker='o', linestyle='', markersize=marksize)
    plt.xlabel('Time [hours]')
    # plt.ylabel('angle')
    plt.title('Inclination')
    #plt.xticks([])

    ax4 = plt.subplot(224, sharex=ax1)
    plt.plot(data_final[0][:, 0]/(60*60), data_final[0][:, 1], 'tab:green', marker='o', linestyle='', markersize=marksize)
    plt.xlabel('Time [hours]')
    # plt.ylabel('kg')
    plt.title('Mass')
    #plt.xticks([])

    plt.tight_layout()
    
    # plt.savefig('datacleaning eksempler/data_main.pdf')
    
    
    
    
    
    
    
    
    
    





