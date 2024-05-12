import pandas as pd

from t01_Import import data_input_version_id

exports: pd.DataFrame = pd.read_csv(f'intermed_results/O_exports_{data_input_version_id}.csv', sep=',', header=0)
print(exports[0:0])

# TODO split into two tables - cases and documents with a new internal document ID...
