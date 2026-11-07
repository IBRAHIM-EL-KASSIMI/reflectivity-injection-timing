import os

import chardet
import numpy as np
import pandas as pd

from . import cycles_timeline

"""
This function detects the moment when a signal rises or falls. 
We assume that during the first N measurement points(50 by default), the signal remains stable. 
If the variation in the signal exceeds the maximum variation observed during these first N points, 
we consider that the signal is changing.

"""


def detect_response_rise_v2():
    
    rises_dic = {}

    csv_path = f"{os.getcwd()}/Cycles_csv"
    csv_files = [f  for f in os.listdir(csv_path) if f.endswith('.xlsx')]
    csv_files.sort()
    
    
    cycle_i = 1 #Number of the current cycle 

    for cycle_f in csv_files :
        title_i = cycle_f
        path_i = f"{os.getcwd()}/Cycles_csv/{title_i}"
        
        #Find the encoding of the file 
        with open(path_i, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.

        cycle_f = pd.read_csv(path_i, sep = None, engine = 'python', encoding=enc)
        

        

        start_i = cycles_timeline.cycles_timeline()[cycle_i][0]  #The start given in "KineticsComments.txt"

        num_columns = cycle_f.shape[1]
        cycle_f.iloc[:, 0] = cycle_f.iloc[:, 0].astype(int)
        t_start_search = start_i+20 #we are looking for the rise(or the fall) from t_start
      
        rise_times = []
        for s in range(1,num_columns): #Treating the signals (s for signal).
            rise_found = False

            j = 1

            width1 = 9 # a window of 3 (9/3) points for the first attempt.

            max_iter1 = cycle_f.iloc[:,0].count()-width1

            while not(rise_found):
                if j == max_iter1: # No rise/fall is detected for both tries.
                    rise_times.append(np.nan)
                    break
                elif  j < max_iter1 : 
                    window = cycle_f[(cycle_f[cycle_f.columns[0]] >= t_start_search+3*j) & (cycle_f[cycle_f.columns[0]] <= t_start_search+3*j+width1)] # window of 4 points.
                    window_list = [window[col].to_numpy() for col in window.columns]
                                                                       
                    Time_window1 = window_list[0][:-1]
                    Y_window1 = window_list[s][:-1]
                    Y_window2 = window_list[s][1:]
                    slope_window1 = (Y_window1[1]-Y_window1[0])/3
                    slope_window2 = (Y_window2[1]-Y_window2[0])/3

                    angle_window1 = 300*(360/(2*np.pi))*np.arctan(slope_window1)
                    angle_window2 = 300*(360/(2*np.pi))*np.arctan(slope_window2)
                    angle_window = (angle_window1+angle_window2)/2

                    if abs(angle_window) >= 25  : # the angle is greater than 25 .
                        rise_times.append(Time_window1[0])
                        rise_found = True
                j = j+1
                    

        rises_dic[title_i] = rise_times
        cycle_i += 1 
    return rises_dic # Dictionnary / key : file name / value : list of rises in columns order 