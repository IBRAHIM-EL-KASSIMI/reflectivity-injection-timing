import os

import chardet
import pandas as pd


def align_cycle_starts():
    csv_files = [f  for f in os.listdir(os.getcwd()+"/Cycles_csv") if f.endswith('.xlsx')]
    csv_files.sort()


    for cycle_title in csv_files :
        path_i = f"{os.getcwd()}/Cycles_csv/{cycle_title}"
        #Detecting the encoding
        with open(path_i, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.

        cycle_f = pd.read_csv(path_i, sep=None, engine='python', encoding=enc)

        cycle_f = cycle_f[(cycle_f[cycle_f.columns[0]]) >= -100]
        cycle_f.to_csv(path_i, index = False)

