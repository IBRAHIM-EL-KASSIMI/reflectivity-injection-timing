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


def detect_response_rise_v3():
    pourcentage = 0.1180010734944325 #if the value is 11.8% of the maximum, we consider a rise  
    pourcentage = 0.01
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
        num_rows = cycle_f.shape[0]
        cycle_f.iloc[:, 0] = cycle_f.iloc[:, 0].astype(int)
        t_start_search = start_i #we are looking for the rise(or the fall) from t_start
      
        rise_times = []
        for s in range(1,num_columns): # for each signal.
            max_half_column = cycle_f.iloc[:num_rows//2, s].max()            
            rise_found = False

            j = 1

            search_try = 1
            width1 = 21 # a window of 7 (21/3) points for the first attempt.
            max_iter1 = int((1/3)*cycle_f.iloc[:,0].count())
            max_iter2 = int((cycle_f.iloc[:,0].count())//4)+ 1

            while not(rise_found):
                if j == max_iter2 and search_try == 2: # No rise/fall is detected for both tries.
                    rise_times.append(np.nan)
                    break
                elif  j < max_iter1 and search_try == 1: 
                    window = cycle_f[(cycle_f[cycle_f.columns[0]] >= t_start_search+3*j) & (cycle_f[cycle_f.columns[0]] <= t_start_search+3*j+width1)] # window of 4 points.
                    window_list = [window[col].to_numpy() for col in window.columns]
                                                                       
                    Time_window = window_list[0]
                    Y_window = window_list[s]
                    
                    slope1 = 0 # The value of the slope
                    #product_slopes = 1
                    slope2 = 0
                    for i in range(1,4):
                        slope1 += (Y_window[i]-Y_window[i-1])/(Time_window[i]-Time_window[i-1])
                        #product_slopes *= slope
                    for i in range(4,7):
                        slope2 += (Y_window[i]-Y_window[i-1])/(Time_window[i]-Time_window[i-1])
                        #product_slopes *= slope
                    angle_window1 = 300*(360/(2*np.pi))*np.arctan(slope1)
                    angle_window2 = 300*(360/(2*np.pi))*np.arctan(slope2)
                    angle_window = angle_window2-angle_window1
                    if abs(angle_window) >= 135 :
                        rise_times.append(Time_window[3])
                        rise_found = True
                    else:
                        pass
                elif j == max_iter1 and search_try == 1: # If the first try fails.
                    j = 0 
                    search_try = 2 # We move the second try.
                else: 
                    Time_window = window_list[0]
                    Y_window = window_list[s]
                    if abs(Y_window[2]/max_half_column) >= pourcentage:
                        rise_times.append(Time_window[0])
                        rise_found = True 
                    else:
                        pass 
                        

                j = j+1

        rises_dic[title_i] = rise_times
        cycle_i += 1 
    return rises_dic # Dictionnary / key : file name / value : list of rises in columns order 
