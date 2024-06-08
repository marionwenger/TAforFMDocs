import time
import warnings
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f


# TODO LATER generalize methods import and process, so that there is less duplication...
def import_documents(data_input_version_id, start_time, digits: int,
                     printing_steps: bool) -> pd.DataFrame:
    start_time_import = time.time()
    f.print_steps('import of documents', printing_steps)

    # Load the HTML file
    # file_path_data = Path(f'data/kleines_Test_File.htm')
    # 0.406 seconds
    # 112 Zeilen, Faktor ~500 zur kompletten Tabelle
    # file_path_data = Path(f'data/mittleres_Test_File.htm')
    # 22.589 seconds
    # 11000 Zeilen, Faktor ~5 zur kompletten Tabelle, Faktor ~100 zum Testfile
    file_path_data = Path(f'data/I_doc_exports_{data_input_version_id}.htm')
    # 209.541 seconds / 218.644 seconds - added printout while parsing / 477.247 seconds - changed to UTF-8 /
    # 8.74 minutes (break point included)
    f.print_steps('filepath is ' + str(file_path_data), printing_steps)

    export_doc_columns = ['ID_FM', 'ID_Fall', 'fAnmeldedatum', 'filename', 'TextMBSVisionLength', 'TextMBSVision']
    fm_doc_exports = pd.DataFrame(columns=export_doc_columns)

    with open(file_path_data, "r", encoding='utf-8') as file:  # did not work: 'iso-8859-1'      ?'latin-1'
        f.print_steps('with opened', printing_steps)
        soup = BeautifulSoup(file, "lxml")  # 'html.parser' is too slow
        f.print_steps('soup cooked', printing_steps)

    f.print_steps('with closed', printing_steps)
    rows = soup.find_all("tr")
    counter = 0
    f.print_steps(f'started importing rows after {f.get_running_time(start_time, digits)}', printing_steps)
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 1:
            counter = counter + 1
            row_data = [cell.get_text(strip=True) for cell in cells]
            fm_doc_exports.loc[len(fm_doc_exports)] = row_data
            if counter % 5000 == 0:
                f.print_steps(f'{counter} rows imported after {f.get_running_time(start_time, digits)}'
                              , printing_steps)
    f.print_steps(f'imported all rows after {f.get_running_time(start_time, digits)}', printing_steps)
    f.print_steps(f'import took {f.get_running_time(start_time_import, digits)}', printing_steps)
    f.print_steps('documents in pandas dataframe', printing_steps)
    f.print_steps(fm_doc_exports.head(), printing_steps)
    fm_doc_exports.drop(['ID_FM'], axis=1, inplace=True)  # dismiss child ID

    return fm_doc_exports


def process_documents(fm_doc_exports: pd.DataFrame, random_seed: int, printing_steps: bool,
                      test_on: bool, test_case_ids: list[int]) -> pd.DataFrame:
    f.print_steps('process of documents', printing_steps)

    fm_doc_exports.rename(
        columns={"ID_Fall": "id", 'fAnmeldedatum': 'year', 'filename': 'name', 'TextMBSVisionLength': 'length',
                 'TextMBSVision': 'contents'}, inplace=True)

    # id --> type string
    fm_doc_exports = f.anonymize_and_index(fm_doc_exports, random_seed, test_on, test_case_ids)
    # year (second column) --> type int
    fm_doc_exports['year'] = fm_doc_exports.apply(f.get_and_check_year_from_FM_date, args=('%d/%m/%Y', 0), axis=1)
    fm_doc_exports['name'] = fm_doc_exports['name'].astype(str)
    fm_doc_exports['length'] = fm_doc_exports['length'].astype(int)
    fm_doc_exports['contents'] = fm_doc_exports['contents'].astype(str)

    return fm_doc_exports


def import_diaglists(data_input_version_id, start_time, digits: int,
                     printing_steps: bool) -> pd.DataFrame:
    start_time_import = time.time()
    f.print_steps('import of diagnoses lists', printing_steps)

    file_path_data = Path(f'data/I_diaglist_exports_{data_input_version_id}.htm')
    f.print_steps('filepath is ' + str(file_path_data), printing_steps)

    with open(file_path_data, "r", encoding='utf-8') as file:
        f.print_steps('with opened', printing_steps)
        soup = BeautifulSoup(file, "html.parser")  # lxml?
        f.print_steps('soup cooked', printing_steps)

    f.print_steps('with closed', printing_steps)

    # Parse the HTML content using BeautifulSoup
    table = soup.find('table')

    # Extract headers
    headers = [th.get_text() for th in table.find_all('th')]

    # Extract rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # tr = table row
        row = []
        for td in tr.find_all('td'):  # td = table data = value in one column
            # Split the cell content on <br> tags
            cell_content = str(td).split(';')  # values between semicolons only in the last column
            # Strip any HTML tags and whitespace from each value
            cell_content = [BeautifulSoup(val, 'html.parser').get_text(strip=True) for val in cell_content]
            while "" in cell_content:
                cell_content.remove("")
            row = row + cell_content
        rows.append(row)

    # Find the maximum length of rows which varies because of the concatenated values
    max_columns = max(len(row) for row in rows)

    # Create column names for the split values in the last column
    new_headers = headers[:len(headers) - 1] + [f"diag_{i}" for i in range(1, (max_columns - (len(headers) - 1)) + 1)]

    # Flatten the rows to match the new headers
    flattened_rows = []
    counter = 0
    f.print_steps(f'started importing rows after {f.get_running_time(start_time, digits)}', printing_steps)
    for row in rows:
        counter = counter + 1
        new_row = row
        extension: list = ['' for i in range(max_columns - len(row))]
        new_row.extend(extension)  # Extend the row to match the max length
        flattened_rows.append(new_row)
        if counter % 3000 == 0:
            f.print_steps(f'{counter} rows imported after {f.get_running_time(start_time, digits)}'
                          , printing_steps)
    f.print_steps(f'imported all rows after {f.get_running_time(start_time, digits)}', printing_steps)
    f.print_steps(f'import took {f.get_running_time(start_time_import, digits)}', printing_steps)
    fm_diaglist_exports = pd.DataFrame(flattened_rows, columns=new_headers)
    f.print_steps('diagnoses lists in pandas dataframe', printing_steps)
    f.print_steps(fm_diaglist_exports.head(), printing_steps)

    return fm_diaglist_exports


def process_diaglists(fm_diaglist_exports: pd.DataFrame, random_seed: int, printing_steps: bool,
                      test_on: bool, test_case_ids: list[int]) -> pd.DataFrame:
    f.print_steps('process of diagnoses lists', printing_steps)

    fm_diaglist_exports.rename(
        columns={"ID_Fall": "id", 'fDiagnosen': 'diag_list'}, inplace=True)
    fm_diaglist_exports.drop(['Datum'], axis=1, inplace=True)

    fm_diaglist_exports['id'] = fm_diaglist_exports['id'].apply(f.convert_to_int)
    fm_diaglist_exports = fm_diaglist_exports.loc[fm_diaglist_exports['id'] != 0]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        # SettingWithCopyWarning:
        # A value is trying to be set on a copy of a slice from a DataFrame.
        # Try using .loc[row_indexer,col_indexer] = value instead"
        for i in range(1, fm_diaglist_exports.shape[1] - 1):
            fm_diaglist_exports[f'diag_{i}'] = fm_diaglist_exports[f'diag_{i}'].astype(str)

    fm_diaglist_exports = f.anonymize_and_index(fm_diaglist_exports, random_seed, test_on, test_case_ids)

    # TODO NOW classify diagnoses & 1-hot encoding (see also R code for Vergleich...)

    return fm_diaglist_exports
