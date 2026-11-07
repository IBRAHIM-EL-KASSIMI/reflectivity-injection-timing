import os

import chardet
import pandas as pd

from .column_order import get_ordered_columns


def reorder_columns():
    """
    Changing columns orders based on the order given by the client.
    """
    current_dir = os.getcwd()
    csv_files_path = current_dir+"/Sep_Cycles_csv"

    csv_files = os.listdir(csv_files_path)
    ordered_columns = get_ordered_columns()
    for file in csv_files:
        cycle_path = f"{csv_files_path}/{file}"
        #Find the encoding of the file 
        with open(cycle_path, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.
        cycle_f = pd.read_csv(cycle_path, sep = None, engine='python', encoding = enc)
        cycle_f = cycle_f[ordered_columns]
        cycle_f.to_csv(cycle_path, index=False)