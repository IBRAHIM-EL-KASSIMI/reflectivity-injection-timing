import os

import chardet
import pandas as pd


def y_transform():

    cycles_files = [f for f in os.listdir(os.getcwd()+"/Sep_Cycles_csv") if f.endswith('.xlsx')]


    for cycle_f in cycles_files:
        cycle_title = cycle_f
        cycle_path = f"{os.getcwd()}/Sep_Cycles_csv/{cycle_title}"
        with open(cycle_path, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.
        cycle_f = pd.read_csv(cycle_path, sep=None, engine='python', encoding=enc)  
        num_columns = cycle_f.shape[1]  # Number of columns in the csv file.
        for s in range(1, num_columns):
            first_30_Yi = cycle_f.iloc[0:30, s].to_numpy() 

            average_column_i = first_30_Yi.mean()

            all_Yi = cycle_f.iloc[0:, s].to_numpy()
            all_Yi = all_Yi - average_column_i # Applying the Y transformation.
            cycle_f.iloc[0:, s] = all_Yi.round(decimals=9) # Updating the column in the dataframe.
            cycle_f.to_csv(f"{os.getcwd()}/Sep_Cycles_csv/{cycle_title}", index = False) # Saving the updated dataframe to a csv file.