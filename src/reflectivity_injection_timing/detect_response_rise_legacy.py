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


def detect_response_rise_legacy(N=50):
    
  
    rises_dic = {}


    csv_files = [f  for f in os.listdir(f"{os.getcwd()}/Cycles_csv") if f.endswith('.csv')]
    csv_files.sort() # List of the csv files of cycles.
    
    
    cycle_i = 1 #Number of the current cycle 

    for cycle_f in csv_files :
        
        title_i = cycle_f # Title of the cycle i.
        path_i = f"Cycles_csv/{title_i}" # Path of the cycle i.
        
        #Find the encoding of the file 
        with open(path_i, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.

        cycle_f = pd.read_csv(path_i, sep = ";", encoding=enc) # Reading the file 

        start_i = cycles_timeline.cycles_timeline()[cycle_i][0]  #The start given in "KineticsComments.txt"
        
        
        preinj_window = cycle_f[(cycle_f[cycle_f.columns[0]] >= start_i) & (cycle_f[cycle_f.columns[0]] <= start_i+29)]

        rise_window  = cycle_f[(cycle_f[cycle_f.columns[0]] >= start_i+30) & (cycle_f[cycle_f.columns[0]] <= start_i+70)]

        
        preinj_list_i = [preinj_window[col].to_numpy() for col in preinj_window.columns]
        
        # Making lists of signals during preinjection and rising periods
        rise_window_list_i = [rise_window[col].to_numpy() for col in rise_window.columns] #The interval during which we assume that the rise will occur.
        
        rising_times = np.array([]) #The rising times for a cycle.
        
        for s in range(1,len(preinj_list_i)): #Treating the signals (s for signal).
            column = preinj_list_i[s]

            max = np.max(np.abs(np.diff(column)))

            rise_index = np.argmax(np.abs(np.diff(rise_window_list_i[s])) > 2*max)
            


            if rise_index == 0:
                np.append(rising_times, np.nan)
            else:
                rise_time = start_i + 3*rise_index #3 corresponds to the time step.
                rising_times = np.append(rising_times,rise_time)
        
        avg_raise_t = np.nanmean(rising_times) #This value will be used for non rising signals.
        
        for s in range(len(rising_times)):
            if np.isnan(rising_times[s]):
                rising_times[s] = avg_raise_t
            else:
                pass
        rises_dic[title_i] = rising_times
        cycle_i += 1 


        
