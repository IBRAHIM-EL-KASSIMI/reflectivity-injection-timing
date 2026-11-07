import os

import chardet
import pandas as pd


def x_transform(rows_to_remove:dict):
    csv_files = [f  for f in os.listdir(os.getcwd()+"/Cycles_csv") if f.endswith('.xlsx')]
    csv_files.sort()


    for cycle_title in csv_files :
        path_i = f"{os.getcwd()}/Cycles_csv/{cycle_title}"
        #Detecting the encoding
        with open(path_i, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.
        
        cycle_f = pd.read_csv(path_i, sep=None, engine='python', encoding=enc)
        
        origine = rows_to_remove[f"{cycle_title}_min"]
        cycle_f["Time(s)"] = cycle_f["Time(s)"] - origine

        columns_to_remove = rows_to_remove[cycle_title]
        for col, n in columns_to_remove.items():
            if col in cycle_f.columns:  # Ensure the column exists
                cycle_f[col] = cycle_f[col].iloc[n:].reset_index(drop=True)

        cycle_f.to_csv(f"{os.getcwd()}/Cycles_csv/{cycle_title}", index=False)
       
    