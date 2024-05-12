import pandas as pd

data_input_version_id = 'div_1.0'
data_version_id = 1
random_seed: int = 1404

# TODO ONLY IF sure that input will be as htm...

# TODO does not find file??? did find it before... tried both pathlib and os... - I suspect this will be solved with main.py
# # Load the HTML file
# file_path_data = Path(f'data/I_documents_{data_input_version_id}.htm')
# # file_path_data = os.path.join('data', f'''I_documents_{data_input_version_id}.htm''')
#
# # Read the HTML content
# with open(file_path_data, 'r', encoding='utf-8') as file:
#     html_content = file.read()
#
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
# documents: pd.DataFrame = pd.read_html(str(tables[0]))[0]
# print(documents.head())
documents = pd.DataFrame((14, 4, 1980))

# TODO save csv
# file_path_csv = os.path.join('intermed_results', f'''O_documents_{data_input_version_id}.csv''')
# documents.to_csv(file_path_csv)
