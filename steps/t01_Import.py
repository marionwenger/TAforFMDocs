import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f


def import_fm_exports(data_years, data_input_version_id, start_time, printing_steps: bool = False) -> \
        (pd.DataFrame, pd.DataFrame):
    f.print_steps('started with t01', printing_steps)

    # Load the HTML file
    # file_path_data = Path(f'data/kleines_Test_File.htm')
    # 0.406 seconds
    # 112 Zeilen, Faktor ~500 zur kompletten Tabelle
    # file_path_data = Path(f'data/mittleres_Test_File.htm')
    # 22.589 seconds
    # 11000 Zeilen, Faktor ~5 zur kompletten Tabelle, Faktor ~100 zum Testfile
    file_path_data = Path(f'data/I_doc_exports_{data_input_version_id}.htm')
    # 209.541 seconds / 218.644 seconds - added printout while parsing / 477.247 seconds - changed to UTF-8
    f.print_steps('filepath is ' + str(file_path_data), printing_steps)

    # export_columns = ['ID_FM', 'fName_Vorname_Kind', 'ID_Fall', 'fAnmeldedatum', 'filename', 'TextMBSVisionLength',
    #                   'TextMBSVision']  # Version kleines Test File
    export_columns = ['ID_FM', 'ID_Fall', 'fAnmeldedatum', 'filename', 'TextMBSVisionLength', 'TextMBSVision']
    fm_doc_exports = pd.DataFrame(columns=export_columns)

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
                f.print_steps(f'{counter} rows imported '
                              f'in {round((time.time() - start_time), 3)} seconds', printing_steps)

    f.print_steps('documents in pandas dataframe', printing_steps)

    # TODO IF NEEDED restrict data to given years (data_years)

    # TODO NOW stop re-running parsing, it is too time consuming...

    # %% TODO NOW import diagnoses lists (see also R code for Vergleich...)
    fm_diaglist_exports = pd.DataFrame()

    # %% anonymize with TA id
    fm_doc_exports.rename(columns={"ID_Fall": "id"})
    # fm_doc_exports['id'] = fm_doc_exports.apply(f.generate_ta_id) # TODO generate random ID for each case
    # fm_doc_exports.set_index('id', inplace=True)

    # TODO NOW adapt columns to data and rename them

    # Display the DataFrame
    f.print_steps(fm_doc_exports.head(), printing_steps)
    # Shows the first few rows to confirm the data is imported correctly

    return fm_doc_exports, fm_diaglist_exports
