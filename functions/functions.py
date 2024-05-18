import os
import random
import string

import pandas as pd


def print_steps(object_to_be_printed: object, printing_steps: bool = False) -> None:
    if printing_steps:
        print(object_to_be_printed)


def save_to_csv(data: pd.DataFrame, folder_name: str, file_name: str, saving_to_csv: bool = True,
                printing_steps: bool = False) \
        -> None:
    if saving_to_csv:
        file_path_csv = os.path.join(folder_name, f'{file_name}.csv')
        data.to_csv(file_path_csv)
        print_steps('saved ' + file_path_csv, printing_steps)


def generate_ta_id(input_seed: int) -> str:
    random.seed(input_seed)
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'TA-{random_chars}'
