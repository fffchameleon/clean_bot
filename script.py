import pygsheets
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import subprocess

name_to_id = {
        # 112
        "敬淇":"848511725980483594",
        "晏瑄":"825242239398838322",
        "昭融":"725632233108406292",
        "志翔":"732971917891338271",
        "宥成":"784514869608448070",
        "子凡":"904797191586070569",
        # 113
        "偉銓":"681366003262816267",
        "育棠":"584774630359826433",
        "禎圻":"535283333869862932",
        "松憶":"855824395682840607",
        "若綾":"867407732084047923"
    }

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
    
    return date, sweep + tag_discord_id(sweep), mop + tag_discord_id(mop)

def tag_discord_id(name):
    return (dcid := name_to_id.get(name)) and (f"<@{dcid}>" if dcid is not None else "")

if __name__ == "__main__":
    get_cleaner()