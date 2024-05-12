import pandas as pd

from t01_Import import data_input_version_id

documents: pd.DataFrame = pd.read_csv(f'intermed_results/O_documents_{data_input_version_id}.csv', sep=',', header=0)
