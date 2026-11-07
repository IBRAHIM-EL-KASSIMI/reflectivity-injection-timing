#Create a liste of coulums starting with time(s)
import os

import chardet


def get_columns():
    current_dir = os.getcwd()
    spot_file = next(
        (name for name in os.listdir(current_dir) if "spot" in name.lower()),
        None,
    )
    if spot_file is None:
        raise FileNotFoundError(f"No spot file found in {current_dir}.")

    with open(spot_file, "rb") as f :
        result = chardet.detect(f.read(1000))
        enc = result['encoding'] #The encoding of the file.

    with open(spot_file, 'r',encoding=enc, errors='ignore') as file:
        lines = file.readlines()
    colums = ["Time(s)"]
    for i in range(1, len(lines)):
        colum_number_name = lines[i].split("\t")[1]
        name_list  = colum_number_name.split("-")[1:] 
        name = "-".join(name_list).replace(",", ".")
        colums.append(name)

    counts = {} # Colums titles and their frequencies.
    colums_2 = [] # Some REF colums have the same name, so wen need to differentiate between them.
    for name in colums :
        if name in counts:
            counts[name] +=1
            colums_2.append(f"{name}.{counts[name]}")
        else:
            counts[name] = 0
            colums_2.append(name)


    return colums_2