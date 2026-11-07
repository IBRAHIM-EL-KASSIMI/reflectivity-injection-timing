import os

import numpy as np

from .columns import get_columns


def rows_to_remove(raises : dict):

    signal_columns = get_columns()[1:]

    time_step = 3 # Sampling period
    csv_path = f"{os.getcwd()}/Cycles_csv"
    csv_files = [f  for f in os.listdir(csv_path) if f.endswith('.xlsx')]
    csv_files.sort()


    to_transform = {} # key : file name | value : dictionnary colum_ame : rows_to_delete 
    for cycle in csv_files:
        file_raises_list = raises[cycle]
        origin = np.nanmin(file_raises_list)
        columns_to_remove = {}
        for i in range(len(signal_columns)):
            column_rise = file_raises_list[i]
            if np.isnan(column_rise) or np.isnan(origin):
                columns_to_remove[signal_columns[i]] = 0
            else:
                if int((column_rise-origin)/time_step) >= 7:# Si le nombre de points translatés est supérieur à 7 on ne transaltae pas la courbe.
                    columns_to_remove[signal_columns[i]] = 0
                else:
                    columns_to_remove[signal_columns[i]] = int((column_rise-origin)/time_step)

        to_transform[cycle] = columns_to_remove
        cycle_min = f"{cycle}_min"
        to_transform[cycle_min] = origin # We add a key called name_cycle_min with the origin associatied so we can translate the x axes
    return to_transform