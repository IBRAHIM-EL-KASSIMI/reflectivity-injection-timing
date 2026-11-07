import os
from datetime import date

import pandas as pd


def combine_workbook():
    run_date = date.today()
    csv_path = "Sep_Cycles_csv"

    cycles_files = [f for f in os.listdir(csv_path) if f.endswith(".xlsx")]
    cycles_files = sorted(cycles_files)

    final_file_path = f"Analysed_Data_{run_date}.xlsx"


    with pd.ExcelWriter(final_file_path, engine="openpyxl") as final_file:
        # Creating an empty sheet
        #pd.DataFrame().to_excel(final_file, sheet_name="EmptySheet")

        for i in range(len(cycles_files)):
            cycle_path = f"Sep_Cycles_csv/{cycles_files[i]}"
            cycle = pd.read_csv(cycle_path)
            cycle = pd.DataFrame(cycle)
            cycle_sheet_name = cycles_files[i]
            cycle.to_excel(final_file, sheet_name=cycle_sheet_name, index=False)
    
    