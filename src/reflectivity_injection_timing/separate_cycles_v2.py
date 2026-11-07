import os

import chardet

from . import columns

"""
Given the start, the end and the title of each cycle (the value return by cycles_timeline())
This function generates a csv and a txt file for eache cycle


"""


def separate_cycles(timeline,N):
    # Creating the folders for cycles files.
    if not os.path.exists("Sep_Cycles_txt"):
        os.makedirs("Sep_Cycles_txt")
    if not os.path.exists("Sep_Cycles_csv"):
        os.makedirs("Sep_Cycles_csv")

    txt_path = os.path.join(os.getcwd(), "Sep_Cycles_txt")
    csv_path = os.path.join(os.getcwd(), "Sep_Cycles_csv")

    nb_cycles = len(timeline) # The number of cycles.


    for i in range(1,nb_cycles+1): 

        title_i_txt = f"{txt_path}/{i}_{timeline[i][2]}.txt"
        title_i_csv = f"{csv_path}/{i}_{timeline[i][2]}.xlsx"
        
        with open(title_i_txt,'w') as cycle_file_txt, open(title_i_csv, 'w') as cycle_file_csv:
           
            colums = columns.get_columns() # List of columns from the spot file.
            
            header_i_txt = '\t'.join(colums)+"\n" 
            cycle_file_txt.write(header_i_txt)

            header_i_csv = ';'.join(colums)+"\n"
            cycle_file_csv.write(header_i_csv)

    data_files = [f for f in os.listdir() if ("kinetics" in f.lower() and "data" in f.lower() and "comment" not in f.lower())] # Listing all Data files 
    data_files.sort() # Sorting Data files so we heve an increasing time 
    

    for data_i in data_files:
        
        with open(data_i, "rb") as f :
            result = chardet.detect(f.read(1000))
            enc = result['encoding'] #The encoding of the file.

        with open(data_i, "r", encoding=enc) as data_file:
            i = 1 #Number of the current cycle.
            
            for line in data_file:
                if i <= nb_cycles: # We have not treated all the cycles.
                    with open(title_i_txt,'+a') as cycle_file_txt, open(title_i_csv,'+a') as cycle_file_csv:
                                
                        title_i_txt = f"{txt_path}/{i}_{timeline[i][2]}.txt"# Title of the txt file of cycle i.
                        title_i_csv = f"{csv_path}/{i}_{timeline[i][2]}.xlsx" # Title of the excel file of cycle i.
                        line_time = 60*float(line.split("\t")[0]) # Time of the current line.
                
                        line_list = line.split("\t")
                        time = int(60*float(line_list[0])) # Converting time to seconds.
                        line_list[0] = str(time)

                        line = '\t'.join(line_list) # The current line with the time in seconds.

                        line_txt = line #The line to write in the txt file.
                        line_csv = ';'.join(line.split('\t')) #The line to write in the csv file.

                            
                        start_i = -N+timeline[i][0] # Starting time of cycle i. or = -100+timeline[i][0]
                        end_i = timeline[i][1] # Ending time of cycle i.
                            
                        if start_i <= line_time < end_i:# The current line is in the cycle i.

                            cycle_file_txt.write(line_txt)
                            cycle_file_csv.write(line_csv)
                        
                        elif line_time > end_i: # If we got out of a cycle.
                            i += 1

                else: # We have treated all the cycles.
                    break