from pathlib import Path

import pandas as pd

data_input_version_id = 'div_1.0'
data_version_id = 1
random_seed: int = 1404

# Load the HTML file
file_path_data = Path(f'data/I_exports_{data_input_version_id}.htm')

# TODO NOW UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 in position 429: invalid continuation byte
# File "<frozen codecs>", line 322, in decode
# Read the HTML content
# with open(file_path_data, 'r', encoding='utf-8') as file:
#     html_content = file.read()

# # Use BeautifulSoup to parse the HTML
# soup = BeautifulSoup(html_content, 'html.parser')
#
# # Find all tables in the HTML
# tables = soup.find_all('table')
#
# if len(tables) == 0:
#     raise ValueError("No tables found in the HTML content.")
# elif len(tables) >1:
#     raise ValueError('More than one table in the HTML content.')
#
# # Convert the first table to a DataFrame
# # You can use 'pd.read_html()' on the HTML string of the table
# exports: pd.DataFrame = pd.read_html(str(tables[0]))[0]
# print(exports.head())
exports = pd.DataFrame((14, 4, 1980))

# TODO NOW save csv
# file_path_csv = os.path.join('intermed_results', f'''O_exports_{data_input_version_id}.csv''')
# exports.to_csv(file_path_csv)
