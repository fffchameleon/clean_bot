import pygsheets
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import subprocess


def get_row_variable():
    with open('cur_row.conf', 'r') as file:
        row_variable = int(file.readline().strip())
    return row_variable

def update_row_variable(row_variable):
    with open('cur_row.conf', 'w') as file:
        file.write(str(row_variable))
        
def get_cleaner():
    load_dotenv()
    gc = pygsheets.authorize(service_file='../sheet_key.json')
    sht = gc.open_by_url(os.getenv("SHEET_URL"))

    wks = sht[7]

    df = pd.DataFrame(wks.get_all_values())
    row_variable = get_row_variable()
    date = (df[0][row_variable])
    sweep = (df[1][row_variable])
    mop = (df[2][row_variable])

    print("sweep:", sweep, "mop:", mop)    
    update_row_variable(row_variable + 1)
    
    return date, sweep, mop

if __name__ == "__main__":
    get_cleaner()