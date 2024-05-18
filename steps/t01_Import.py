from io import StringIO
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f


def import_fm_exports(printing_steps: bool = False) -> pd.DataFrame:
    f.print_steps('started with t01', printing_steps)

    # Load the HTML file
    # file_path_data = Path(f'data/I_exports_{data_input_version_id}.htm')
    file_path_data = Path(f'data/kleines_Test_File.htm')  # TODO NOW replace with original file
    f.print_steps('filepath is ' + str(file_path_data), printing_steps)

    # Read the HTML content
    with open(file_path_data, 'r', encoding='iso-8859-1') as file:  # did not work: 'utf-8' and 'latin-1'
        f.print_steps('with opened', printing_steps)
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(file, 'html.parser')
        f.print_steps('soup cooked', printing_steps)

    f.print_steps('with closed', printing_steps)

    # Find all tables in the HTML
    tables = soup.find_all('table')

    f.print_steps('tables extracted', printing_steps)
    f.print_steps(str(len(tables)) + ' = nr of tables', printing_steps)

    if len(tables) == 0:
        raise ValueError("No tables found in the HTML content.")
    elif len(tables) > 1:
        raise ValueError('More than one table in the HTML content.')

    # Convert the first table to a DataFrame
    # You can use 'pd.read_html()' on the HTML string of the table
    fm_exports = pd.read_html(StringIO(str(tables[0])))[0]

    f.print_steps('documents in pandas dataframe', printing_steps)

    # Display the DataFrame
    f.print_steps(fm_exports.head(), printing_steps)
    # Shows the first few rows to confirm the data is imported correctly

    return fm_exports
