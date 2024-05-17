import os
from io import StringIO
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from functions import functions as f

data_input_version_id = 'div_1.0'
data_version_id = 1
random_seed: int = 1404
debug = True

f.print_if_debug(debug, 'started with t01')

# Load the HTML file
# file_path_data = Path(f'data/I_exports_{data_input_version_id}.htm')
file_path_data = Path(f'data/kleines_Test_File.htm')
f.print_if_debug(debug, 'filepath is', file_path_data)

# Read the HTML content
with open(file_path_data, 'r', encoding='iso-8859-1') as file:  # did not work: 'utf-8' and 'latin-1'
    f.print_if_debug(debug, 'with opened')
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(file, 'html.parser')
    f.print_if_debug(debug, 'soup cooked')

f.print_if_debug(debug, 'with closed')

# Find all tables in the HTML
tables = soup.find_all('table')

f.print_if_debug(debug, 'tables extracted')
f.print_if_debug(debug, len(tables), ' = nr of tables')

if len(tables) == 0:
    raise ValueError("No tables found in the HTML content.")
elif len(tables) > 1:
    raise ValueError('More than one table in the HTML content.')

# Convert the first table to a DataFrame
# You can use 'pd.read_html()' on the HTML string of the table
documents = pd.read_html(StringIO(str(tables[0])))[0]

f.print_if_debug(debug, 'documents in pandas dataframe')

# Display the DataFrame
f.print_if_debug(debug, documents.head())  # Shows the first few rows to confirm the data is imported correctly

file_path_csv = os.path.join('intermed_results', f'''O_exports_{data_input_version_id}.csv''')
documents.to_csv(file_path_csv)

f.print_if_debug(debug, 'documents saved to CSV')
