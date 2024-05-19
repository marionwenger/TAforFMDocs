import os
import random
import string
import time
from datetime import datetime

import pandas as pd
from pandas import isna


def print_steps(object_to_be_printed: object, printing_steps: bool = False) -> None:
    if printing_steps:
        print(object_to_be_printed)


def save_to_csv(data: pd.DataFrame, folder_name: str, file_name: str, saving_to_csv: bool = True,
                printing_steps: bool = False) -> None:
    if saving_to_csv:
        file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
        data.to_csv(file_path_csv)
        print_steps('saved ' + file_path_csv, printing_steps)


def read_from_csv(folder_name: str, file_name: str, printing_steps: bool = False) -> pd.DataFrame:
    file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
    print_steps('read ' + file_path_csv, printing_steps)
    return pd.read_csv(file_path_csv)


def generate_ta_id(input_seed: int) -> str:
    random.seed(input_seed)
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'TA-{random_chars}'


def get_running_time(start_time, digits: int) -> str:
    running_time = time.time() - start_time
    time_units = running_time
    unit_text = 'seconds'
    if running_time >= 3600:
        time_units = time_units / 3600
        unit_text = 'hours'
    elif running_time >= 60:
        time_units = time_units / 60
        unit_text = 'minutes'

    return str(round(time_units, digits)) + ' ' + str(unit_text)


def get_and_check_year_from_FM_date(row: pd.Series, date_format, column_nr: int) -> int:
    fm_date = row.iloc[column_nr]
    if isna(fm_date):
        return 0
    else:
        string_date = str(fm_date)
        string_date = string_date.replace(".", "/")  # verschiedene Formate präsent
        date_int = int(datetime.strptime(string_date, date_format).year)
        if date_int < 2013 or date_int > int(time.strftime("%Y")):
            date_int = 0
        return date_int
