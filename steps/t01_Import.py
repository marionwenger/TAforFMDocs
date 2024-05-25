from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f


def import_documents(data_years, data_input_version_id, start_time, printing_steps: bool = False) -> pd.DataFrame:
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

    # export_columns = ['ID_FM', 'fName_Vorname_Kind', 'ID_Fall', 'fAnmeldedatum', 'filename', 'TextMBSVisionLength',
    #                   'TextMBSVision']  # Version kleines Test File
    export_doc_columns = ['ID_FM', 'ID_Fall', 'fAnmeldedatum', 'filename', 'TextMBSVisionLength', 'TextMBSVision']
    fm_doc_exports = pd.DataFrame(columns=export_doc_columns)

    with open(file_path_data, "r", encoding='utf-8') as file:  # did not work: 'iso-8859-1'      ?'latin-1'
        f.print_steps('with opened', printing_steps)
        soup = BeautifulSoup(file, "lxml")  # 'html.parser' is too slow
        f.print_steps('soup cooked', printing_steps)

    f.print_steps('with closed', printing_steps)
    rows = soup.find_all("tr")
    counter = 0
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 1:
            counter = counter + 1
            row_data = [cell.get_text(strip=True) for cell in cells]
            fm_doc_exports.loc[len(fm_doc_exports)] = row_data
            if counter % 5000 == 0:
                f.print_steps(f'{counter} rows imported in {f.get_running_time(start_time, 3)}'
                              , printing_steps)

    f.print_steps('documents in pandas dataframe', printing_steps)

    # Display the DataFrame
    f.print_steps(fm_doc_exports.head(), printing_steps)
    # Shows the first few rows to confirm the data is imported correctly

    return fm_doc_exports


def process_documents(fm_doc_exports: pd.DataFrame, input_seed: int, printing_steps: bool = False) -> pd.DataFrame:
    f.print_steps('process of documents', printing_steps)

    fm_doc_exports.rename(
        columns={"ID_Fall": "id", 'fAnmeldedatum': 'year', 'filename': 'name', 'TextMBSVisionLength': 'length',
                 'TextMBSVision': 'contents'}, inplace=True)
    fm_doc_exports.drop(['ID_FM'], axis=1, inplace=True)  # dismiss child ID

    fm_doc_exports['name'] = fm_doc_exports['name'].astype(str)
    fm_doc_exports['contents'] = fm_doc_exports['contents'].astype(str)
    # The object dtype is how pandas stores strings in dataframes. If for some particular reason you absolutely can't
    # have that data as an object dtype, you're going to have to save it to something other than a dataframe.
    # Values in rows are strings nevertheless!
    fm_doc_exports['year'] = fm_doc_exports.apply(f.get_and_check_year_from_FM_date, args=('%d/%m/%Y', 2), axis=1)

    # %% anonymize with TA id
    fm_doc_exports['id'] = fm_doc_exports.id.apply(f.generate_ta_id)  # id is the random seed for each row
    fm_doc_exports = fm_doc_exports.sample(frac=1, ignore_index=True, random_state=input_seed)
    fm_doc_exports.set_index('id', inplace=True)

    return fm_doc_exports


def import_diaglists(data_years, data_input_version_id, start_time, printing_steps: bool = False) -> pd.DataFrame:
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
            # TODO NOW (I) encode utf-8
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
    for row in rows:
        counter = counter + 1
        new_row = row
        extension: list = ['' for i in range(max_columns - len(row))]
        new_row.extend(extension)  # Extend the row to match the max length
        flattened_rows.append(new_row)
        if counter % 3000 == 0:
            f.print_steps(f'{counter} rows imported in {f.get_running_time(start_time, 3)}'
                          , printing_steps)

    # Create DataFrame
    fm_diaglist_exports = pd.DataFrame(flattened_rows, columns=new_headers)

    return fm_diaglist_exports


def process_diaglists(fm_diaglist_exports: pd.DataFrame, printing_steps: bool = False) -> pd.DataFrame:
    f.print_steps('process of diagnoses lists', printing_steps)

    fm_diaglist_exports.rename(
        columns={"ID_Fall": "id", 'fDiagnosen': 'diag_list'}, inplace=True)
    fm_diaglist_exports.drop(['Datum'], axis=1, inplace=True)

    # TODO NOW (II) anonymize with TA id - same ID as docs...
    # fm_diaglist_exports.rename(columns={"ID_Fall": "id"})
    # fm_diaglist_exports['id'] = fm_diaglist_exports.apply(f.generate_ta_id)
    # fm_diaglist_exports.set_index('id', inplace=True)

    # TODO NOW (III) classify diagnoses & 1-hot encoding (see also R code for Vergleich...)

    return fm_diaglist_exports
