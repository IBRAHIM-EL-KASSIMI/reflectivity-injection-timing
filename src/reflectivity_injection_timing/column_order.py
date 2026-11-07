#Create a liste of coulums starting with time(s)
import os
import re

import chardet


def get_ordered_columns():
    colums = []
    current_dir = os.getcwd()
    spot_file = next(
        (name for name in os.listdir(current_dir) if "spot" in name.lower()),
        None,
    )
    if spot_file is None:
        raise FileNotFoundError(f"No spot file found in {current_dir}.")
    #Finding the type of encoding
    with open(spot_file, "rb") as f :
        result = chardet.detect(f.read(1000))
        enc = result['encoding'] #The encoding of the file.

    with open(spot_file, 'r',encoding=enc, errors='ignore') as file:
        lines = file.readlines()
    for i in range(1, len(lines)):
        colum_name = lines[i].split("\t")[1].replace(",", ".") 
        colums.append(colum_name)
    
    not_ordered = colums
    
    ordered = sorted(not_ordered) # [1-moleculeA, 2-moleculeB]
    ordered = sorted(not_ordered, key=lambda x: int(re.search(r'\d+', x).group()))

    ordered_colums = [] # [moleculeA, moleculeB]

    for col in ordered: # Removing the order nu
        name_list  = col.split("-")[1:] # [1,MoleculeA]
        name = "-".join(name_list)
        ordered_colums.append(name) #DO THE CHANGE AFTER THIS!

    counts = {} # Colums titles and their frequencies.
    colums_2 = [] # Some REF colums have the same name, so wen need to differentiate between them.
    for name in ordered_colums :
        if name in counts:
            counts[name] +=1
            colums_2.append(f"{name}.{counts[name]}")
        else:
            counts[name] = 0
            colums_2.append(name)


    return ["Time(s)"]+colums_2
