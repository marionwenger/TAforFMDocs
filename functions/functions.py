import os
import random
import string
import time
import warnings
from datetime import datetime

import numpy as np
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


def get_warm_diaglist(row: pd.Series) -> pd.Series:  # not really one-hot, because it is the sum of one-hot vectors
    # corresponds to global variable diag_defs # TODO LATER test correspondence
    zeros = np.zeros(57, dtype=int)
    case_id: str = row[0]  # anonymized case id (string)
    new_row = pd.Series(case_id, zeros)  # TODO NOW append zeros with loop
    string_list = ''

    for column in range(1, len(row)):  # TODO LATER we needn't have separated the diagnoses into different columns,
        #  but it is easier to human-read like it is.
        #  Nevertheless, may be it should be avoided?
        string_list = string_list + ' ' + row[column]

        # TODO LATER for kispi usage update diagnose definitions here
    #  (Methode ist eine Kopie vom 'Vergleich'-Projekt mit Stand Ende November 2023)

    if "LKG" in string_list:
        new_row[1] = 1

    if "myofunktionelle Dysfunktion" in string_list:
        new_row[2] = 1

    if "Fehlbildung: Weitere" in string_list:
        new_row[3] = 1

    if "Gehirn: Weitere" in string_list or "Gehirn: andere Diagnose" in string_list:
        new_row[4] = 1

    if "Blutung" in string_list:
        new_row[5] = 1

    if "Cerebralparese" in string_list:
        new_row[6] = 1

    if "Epilepsie" in string_list:
        new_row[7] = 1

    if "kardiale Erkrankungen" in string_list:
        new_row[8] = 1

    if "Auditive Verarbeitungs- und Wahrnehmungsstörung" in string_list:
        new_row[9] = 1

    if "Fütterstörung/Essstörung" in string_list:
        new_row[10] = 1

    if "Hörstörung" in string_list:
        if "Hörstörung mit Cochlea Implantat" in string_list:
            new_row[12] = 1
        else:
            new_row[11] = 1

    if "Schluckstörung" in string_list:
        new_row[13] = 1

    if "Sehstörung" in string_list:
        new_row[14] = 1

    if "Trinkschwäche" in string_list:
        new_row[15] = 1

    if "Organisch: Weitere" in string_list:
        new_row[16] = 1

    if "Syndrom: Weitere" in string_list or "Syndrom: andere Diagnose" in string_list:
        new_row[17] = 1

    if "Trisomie 21" in string_list:
        new_row[18] = 1

    if "Störung der Feinmotorik" in string_list:
        new_row[19] = 1

    if "Störung der Grobmotorik" in string_list:
        new_row[20] = 1

    if "Störung der Oralmotorik" in string_list:
        new_row[21] = 1

    if "Entwicklungsrückstand" in string_list:
        if "Global" in string_list:
            new_row[22] = 1
        if "Kognitiv" in string_list:
            new_row[23] = 1

    if "SES expressiv mehrsprachig" in string_list:
        new_row[24] = 1

    if "SES expressiv monolingual" in string_list:
        new_row[25] = 1

    if "SES mit Komorbidität mehrsprachig" in string_list:
        new_row[26] = 1

    if "SES mit Komorbidität monolingual" in string_list:
        new_row[27] = 1

    if "SES rezeptiv mehrsprachig" in string_list:
        new_row[28] = 1

    if "SES rezeptiv monolingual" in string_list:
        new_row[29] = 1

    if "SES rezeptiv und expressiv mehrsprachig" in string_list:
        new_row[30] = 1

    if "SES rezeptiv und expressiv monolingual" in string_list:
        new_row[31] = 1

    if "SEV expressiv mehrsprachig" in string_list:
        new_row[32] = 1

    if "SEV expressiv monolingual" in string_list:
        new_row[33] = 1

    if "SEV expressiv und rezeptiv mehrsprachig" in string_list:
        new_row[34] = 1

    if "SEV expressiv und rezeptiv monolingual" in string_list:
        new_row[35] = 1

    if "Sprachentwicklung: Weitere" in string_list:
        new_row[36] = 1

    if "Erworbene Sprachstörung" in string_list:
        new_row[37] = 1

    if "Rhinolalie" in string_list:
        new_row[38] = 1

    if "Stimmstörung" in string_list:
        new_row[39] = 1

    if "Stottern, Poltern" in string_list:
        new_row[40] = 1

    if "Sprachstörung: Weitere" in string_list or "Sprache: Weitere" in string_list:
        new_row[41] = 1

    if "Aufmerksamkeitsstörung" in string_list or "AD(H)S" in string_list or "ADHS" in string_list or "ADS" in string_list:
        new_row[42] = 1

    if "Autismus" in string_list or "ASS" in string_list:
        new_row[43] = 1

    if "Emotionale/soziale Störung" in string_list:
        new_row[44] = 1

    if "Mutismus" in string_list:
        new_row[45] = 1

    if "Regulationsstörung" in string_list:
        new_row[46] = 1

    if "Verhaltensauffälligkeit" in string_list or "Verhalten: Weitere" in string_list:
        new_row[47] = 1

    if "eburt" in string_list:
        new_row[48] = 1

    if "Langzeithospitalisation" in string_list:
        new_row[49] = 1

    if "Umfeldproblematik" in string_list:
        new_row[50] = 1

    if "Risikofaktoren: Weitere" in string_list:
        new_row[51] = 1

    if "weitere Diagnosen" in string_list:
        new_row[52] = 1

    if "Dyskalkulie" in string_list:
        new_row[53] = 1

    if "Isolierte Lesestörung" in string_list:
        new_row[54] = 1

    if "Isolierte Rechtschreibstörung" in string_list:
        new_row[55] = 1

    if "Lese-Rechtschreibstörung" in string_list or "Dyslexie" in string_list:
        new_row[56] = 1

    if "Umschriebene Entwicklungsstörungen schulischer Fertigkeiten" in string_list or "Schule: Weitere" in string_list:
        new_row[57] = 1

    return pd.Series(new_row)
