import os

import chardet
import pandas as pd


def add_background():
    """
    Adding the backround signal column which corresponds to the average of REF columns
    """
    csv_path = f"{os.getcwd()}/Cycles_csv"
    csv_files = [f  for f in os.listdir(csv_path) if f.endswith('.xlsx')]
    csv_files.sort()
            
    for cycle_f in csv_files :
            title_i = cycle_f
            path_i = f"{os.getcwd()}/Cycles_csv/{title_i}"
            
            #Find the encoding of the file 
            with open(path_i, "rb") as f :
                result = chardet.detect(f.read(1000))
                enc = result['encoding'] #The encoding of the file.
            cycle_f = pd.read_csv(path_i, sep = None, engine = 'python', encoding=enc)# Reading the csv file

            ref_columns = [col for col in cycle_f.columns.tolist() if("ref" in col.lower())]
            cycle_f["Backround"] = cycle_f[ref_columns].mean(axis=1).round(6)
            cycle_f.to_csv(path_i, index=False)

