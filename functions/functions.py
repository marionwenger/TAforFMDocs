import os
import random
import string
import time
import warnings
from datetime import datetime

import pandas as pd
from pandas import isna


def print_steps(object_to_be_printed: object, printing_steps: bool) -> None:
    if printing_steps:
        print(object_to_be_printed)


def save_to_csv(data: pd.DataFrame, folder_name: str, file_name: str, saving_index: bool, saving_to_csv: bool,
                printing_steps: bool) -> None:
    if saving_to_csv:
        file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
        data.to_csv(file_path_csv, index=saving_index)
        print_steps('saved ' + file_path_csv, printing_steps)


def read_from_csv(folder_name: str, file_name: str, printing_steps: bool) -> pd.DataFrame:
    file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
    print_steps('read ' + file_path_csv, printing_steps)
    return pd.read_csv(file_path_csv)


def generate_ta_id(id: int, test_on: bool, test_case_ids: list[int]) -> str:
    if id == 0:
        return ''
    elif isna(id):
        raise Exception(f"generate_ta_id: id isna")
    random.seed(id)  # 'id' is the random seed for each row
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # test #
    if test_on:
        for case_id in test_case_ids:
            if id == case_id:
                print(f'generate_ta_id: id = {id}, ta_id = TA-{random_chars}')
    return f'TA-{random_chars}'


def get_running_time(start_time, digits: int) -> str:
    return print_time(time.time() - start_time, digits)


def get_and_check_year_from_FM_date(row: pd.Series, date_format, column_nr: int) -> int:
    fm_date = row.iloc[column_nr]
    if not fm_date or isna(fm_date):
        return 0
    else:
        string_date = str(fm_date)
        string_date = string_date.replace(".", "/")  # verschiedene Formate präsent
        date_int = int(datetime.strptime(string_date, date_format).year)
        if date_int < 2013 or date_int > int(time.strftime("%Y")):
            date_int = 0
        return date_int


# TODO LATER include check if there is a column called 'id'...(or include code step renaming given column to 'id')
def anonymize_and_index(df: pd.DataFrame, random_seed: int,
                        test_on: bool, test_case_ids: list[int]) -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        # SettingWithCopyWarning:
        # A value is trying to be set on a copy of a slice from a DataFrame.
        # Try using .loc[row_indexer,col_indexer] = value instead"
        df['id'] = df.id.apply(generate_ta_id, args=[test_on, test_case_ids])  # id is the random seed for each row
    df = df.sample(frac=1, ignore_index=True, random_state=random_seed)  # random seed is only used for reordering
    df.set_index('id', inplace=True)
    return df


def print_time(time_units, digits: int) -> str:
    unit_text = 'second(s)'
    if time_units >= 86400:  # > day --> substract all days...
        time_this_day = time_units % 86400
        return print_time_this_day(time_this_day, digits)
    elif time_units >= 3600:
        time_units = time_units / 3600
        unit_text = 'hour(s)'
    elif time_units >= 60:
        time_units = time_units / 60
        unit_text = 'minute(s)'

    return str(round(time_units, digits)) + ' ' + str(unit_text)


def print_time_this_day(time_units, digits: int) -> str:
    two_hours = 7200  # other time zone
    return print_time(time_units + two_hours, digits) + ' since the beginning of today'


def prepare_contents_for_concatenation(row: pd.Series) -> str:
    name = row.iloc[1]
    contents = row.iloc[3]
    return name + ' ' + contents + ' '


def convert_to_int(value) -> int:
    try:
        # Try to convert to integer
        return int(value)
    except ValueError:
        # If conversion fails, return:
        return 0
        # The value is either a date or an empty string without attached diagnoses...
