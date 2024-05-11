import os

# TODO reconstruct main
# TODO create config file for main

data_input_version_id = 'div_1.0'
data_version_id = 1
random_seed: int = 1404
file_path = os.path.join('data', f'''I_documents_{data_input_version_id}.htm''')

# TODO read htm - maybe version from before does not work anymore because of python version
# tables: list[pd.DataFrame] = pd.read_html(file_path)
# if not len(tables) == 1:
#     print('There are more than one table in the htm file!')
# documents: pd.DataFrame = tables[0]
# print(documents.head())
# filepath_documents = Path(f'''intermed_results/O_documents_{data_input_version_id}.csv''')
# documents.to_csv(filepath_documents)
