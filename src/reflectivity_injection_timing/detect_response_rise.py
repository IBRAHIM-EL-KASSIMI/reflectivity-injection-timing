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


def detect_response_rise():
    
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
            result = chardet.detect(f.read(10000))
            enc = result['encoding'] #The encoding of the file.

        cycle_f = pd.read_csv(path_i, sep = None, engine = 'python', encoding=enc)
        

        

        start_i = cycles_timeline.cycles_timeline()[cycle_i][0]  #The start given in "KineticsComments.txt"

        num_columns = cycle_f.shape[1]
        cycle_f.iloc[:, 0] = cycle_f.iloc[:, 0].astype(int)
        t_start_search = start_i #we are looking for the rise(or the fall) from t_start
      
        rise_times = []
        for s in range(1,num_columns): # for each signal.
            rise_found = False

            j = 1

            width = 9 # a window of 4 (12/3) points for the first attempt.

            max_iter = int((cycle_f.iloc[:,0].count())/3)
            search_try = 1
            max_search_try = 4
            while not(rise_found):
                if j == max_iter and search_try == max_search_try: # No rise/fall is detected for both tries.
                    rise_times.append(np.nan)
                    break
                elif  j < max_iter and search_try == 1: 
                    window = cycle_f[(cycle_f[cycle_f.columns[0]] >= t_start_search+3*j) & (cycle_f[cycle_f.columns[0]] <= t_start_search+3*(j+1)+width)] # window of 4 points.
                    window_list = [window[col].to_numpy() for col in window.columns]
                                                                       
                    Time_window = window_list[0]
                    Y_window = window_list[s]
                   
                   
                    slope1 = (Y_window[1]-Y_window[0])/(Time_window[1]-Time_window[0])
                    slope2 = (Y_window[2]-Y_window[1])/(Time_window[2]-Time_window[1])
                    slope3 = (Y_window[3]-Y_window[2])/(Time_window[3]-Time_window[2])
                    
                    slope4 = (Y_window[2]-Y_window[0])/(Time_window[2]-Time_window[0])
                    slope5 = (Y_window[3]-Y_window[1])/(Time_window[3]-Time_window[1])
                    
                    slope6 = (Y_window[3]-Y_window[0])/(Time_window[3]-Time_window[0])
                    
                    w1, w2, w3 = 0.9, 0.6, 0.3 #Weights associated with each slope w1 for slopes 1,2 and 3, w2 for slopes 4 and 5 , and w3 for slope 6
                    slope = w1*(slope1+slope2+slope3)+w2*(slope4+slope5)+w3*slope6
                    
                    angle_window = 300*(360/(2*np.pi))*np.arctan(slope)
                    if abs(angle_window) >= 350 :
                        rise_times.append(Time_window[0])
                        rise_found = True
                    else:
                        pass
                
                elif search_try == 2 and j < max_iter: # (search_try = 2 and j<max_iter2)
                    #If looking with a window of 4 points for max_iter1 we will continue looking with a window of 3 points until max_iter2
                    window = cycle_f[(cycle_f[cycle_f.columns[0]] >= t_start_search+3*j) & (cycle_f[cycle_f.columns[0]] <= t_start_search+3*(j+1)+width)] # window of 4 points.
                    window_list = [window[col].to_numpy() for col in window.columns]
                                                                       
                    Time_window = window_list[0]
                    Y_window = window_list[s]

                    Time_window = window_list[0]
                    Y_window = window_list[s]
                    

                    slope1 = (Y_window[1]-Y_window[0])/(Time_window[1]-Time_window[0])
                    slope2 = (Y_window[2]-Y_window[1])/(Time_window[2]-Time_window[1])
                    slope3 = (Y_window[3]-Y_window[2])/(Time_window[3]-Time_window[2])
                    
                    slope4 = (Y_window[2]-Y_window[0])/(Time_window[2]-Time_window[0])
                    slope5 = (Y_window[3]-Y_window[1])/(Time_window[3]-Time_window[1])
                    
                    slope6 = (Y_window[3]-Y_window[0])/(Time_window[3]-Time_window[0])
                    
                    w1, w2, w3 = 0.9, 0.6, 0.3 #Weights associated with each slope w1 for slopes 1,2 and 3, w2 for slopes 4 and 5 , and w3 for slope 6
                    slope = w1*(slope1+slope2+slope3)+w2*(slope4+slope5)+w3*slope6
                    
                    angle_window = 300*(360/(2*np.pi))*np.arctan(slope)
                    if abs(angle_window) >= 270 :
                        rise_times.append(Time_window[0])
                        rise_found = True
                    else:
                        pass
                        
                elif search_try == 3 and j < max_iter: # (search_try = 2 and j<max_iter2)
                    #If looking with a window of 4 points for max_iter1 we will continue looking with a window of 3 points until max_iter2
                    window = cycle_f[(cycle_f[cycle_f.columns[0]] >= t_start_search+3*j) & (cycle_f[cycle_f.columns[0]] <= t_start_search+3*(j+1)+width)] # window of 4 points.
                    window_list = [window[col].to_numpy() for col in window.columns]
                                                                       
                    Time_window = window_list[0]
                    Y_window = window_list[s]

                    Time_window = window_list[0]
                    Y_window = window_list[s]
                    

                    slope1 = (Y_window[1]-Y_window[0])/(Time_window[1]-Time_window[0])
                    slope2 = (Y_window[2]-Y_window[1])/(Time_window[2]-Time_window[1])
                    slope3 = (Y_window[3]-Y_window[2])/(Time_window[3]-Time_window[2])
                    
                    slope4 = (Y_window[2]-Y_window[0])/(Time_window[2]-Time_window[0])
                    slope5 = (Y_window[3]-Y_window[1])/(Time_window[3]-Time_window[1])
                    
                    slope6 = (Y_window[3]-Y_window[0])/(Time_window[3]-Time_window[0])
                    
                    w1, w2, w3 = 1.6, 0.6, 0.3 #Weights associated with each slope w1 for slopes 1,2 and 3, w2 for slopes 4 and 5 , and w3 for slope 6
                    slope = w1*(slope1+slope2+slope3)+w2*(slope4+slope5)+w3*slope6
                    
                    angle_window = 300*(360/(2*np.pi))*np.arctan(slope)
                    if abs(angle_window) >= 160 :
                        rise_times.append(Time_window[0])
                        rise_found = True
                    else:
                        pass
                
                
                elif j == max_iter : 
                    j = 0 
                    search_try += 1 # We move the second try.

                j = j+1

        rises_dic[title_i] = rise_times
        cycle_i += 1 
    return rises_dic # Dictionnary / key : file name / value : list of rises in columns order 
