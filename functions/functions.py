import os

import pandas as pd


def print_if_debugging(text1: object, text2: object = '', text3: object = '', debugging: bool = False) -> None:
    if debugging:
        print(text1, text2, text3)


def save_to_csv(data: pd.DataFrame, folder_name: str, file_name: str, saving: bool = True, debugging: bool = False) \
        -> None:
    if saving:
        file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
        data.to_csv(file_path_csv)
        print_if_debugging('saved ' + file_path_csv, debugging)
