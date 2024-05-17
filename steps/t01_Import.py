from io import StringIO
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f


def import_fm_exports(debugging: bool = False) -> pd.DataFrame:
    f.print_if_debugging('started with t01', debugging)

    # Load the HTML file
    # file_path_data = Path(f'data/I_exports_{data_input_version_id}.htm')
    file_path_data = Path(f'data/kleines_Test_File.htm')  # TODO NOW replace with original file
    f.print_if_debugging('filepath is', file_path_data, debugging)

    # Read the HTML content
    with open(file_path_data, 'r', encoding='iso-8859-1') as file:  # did not work: 'utf-8' and 'latin-1'
        f.print_if_debugging('with opened', debugging)
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(file, 'html.parser')
        f.print_if_debugging('soup cooked', debugging)

    f.print_if_debugging('with closed', debugging)

    # Find all tables in the HTML
    tables = soup.find_all('table')

    f.print_if_debugging('tables extracted', debugging)
    f.print_if_debugging(len(tables), ' = nr of tables', debugging)

    if len(tables) == 0:
        raise ValueError("No tables found in the HTML content.")
    elif len(tables) > 1:
        raise ValueError('More than one table in the HTML content.')

    # Convert the first table to a DataFrame
    # You can use 'pd.read_html()' on the HTML string of the table
    fm_exports = pd.read_html(StringIO(str(tables[0])))[0]

    f.print_if_debugging('documents in pandas dataframe', debugging)

    # Display the DataFrame
    f.print_if_debugging(fm_exports.head(), debugging)
    # Shows the first few rows to confirm the data is imported correctly

    return fm_exports
