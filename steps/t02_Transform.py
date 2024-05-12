import pandas as pd

from t01_Import import data_input_version_id

exports: pd.DataFrame = pd.read_csv(f'intermed_results/O_exports_{data_input_version_id}.csv', sep=',', header=0)
print(exports[0:0])

# TODO split into two tables - cases and documents with a new internal document ID...

# List of columns for each new DataFrame
# TODO rename
cases_columns = ['ID_FM', 'fName_Vorname_Kind', 'ID_Fall', 'fAnmeldedatum', ]
documents_columns = ['filename', 'TextMBSVisionLength', 'TextMBSVision']

# Create new DataFrames
cases = exports[cases_columns]
documents = exports[documents_columns]

# Reset index to create a new unique ID for each row
# TODO why is this bijective?
cases.reset_index(drop=True, inplace=True)
documents.reset_index(drop=True, inplace=True)

# Add a new ID column to both DataFrames
# TODO use loc instead
# cases['DocID'] = range(1, len(cases) + 1)
# documents['DocID'] = range(1, len(documents) + 1)

# TODO change order of columns

# # Print the new DataFrames
# print("cases:")
# print(cases.head)
# print("\ndocuments:")
# print(documents)
