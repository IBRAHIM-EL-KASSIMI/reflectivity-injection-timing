import os

import chardet
import pandas as pd


def difference_signals():
    """
    Substracting the bacround signal from each column
    """
    csv_path = f"{os.getcwd()}/Sep_Cycles_csv"
    csv_files = [f  for f in os.listdir(csv_path) if f.endswith('.xlsx')]
    csv_files.sort()
            
    for cycle_f in csv_files :
            title_i = cycle_f
            path_i = f"{os.getcwd()}/Sep_Cycles_csv/{title_i}"
            
            #Find the encoding of the file 
            with open(path_i, "rb") as f :
                result = chardet.detect(f.read(1000))
                enc = result['encoding'] #The encoding of the file.

            cycle_f = pd.read_csv(path_i, sep = None, engine = 'python', encoding=enc)# Reading the csv file
        
            cycle_f[" "] = None # Adding an empty column to seperate columns and columns-backround

            for column in cycle_f.columns.tolist():
                if column == "Time(s)":
                    cycle_f[f"{column}_bis"]  = cycle_f[column]
                else:
                    cycle_f[f"{column}_bis"]  = cycle_f[column] - cycle_f["Backround"]   
            cycle_f.to_csv(path_i, index=False)

            


