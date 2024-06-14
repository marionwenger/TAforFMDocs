import warnings

import pandas as pd

from functions import functions as f


def unite_texts_per_case(documents: pd.DataFrame, printing_if: bool, random_seed: int,
                         test_on: bool, test_case_ids: list[int]) -> pd.DataFrame:
    f.print_if('uniting texts per case', printing_if)

    # Ensure no NaN values interfere with concatenation (I think there are none...)
    documents.loc[:, 'contents'] = documents['contents'].fillna('')
    documents.loc[:, 'name'] = documents['name'].fillna('')

    # ignore SettingWithCopyWarning (for now)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        # SettingWithCopyWarning:
        # A value is trying to be set on a copy of a slice from a DataFrame.
        # Try using .loc[row_indexer,col_indexer] = value instead"
        documents.loc[:, 'contents_with_name'] = ""

    documents.loc[:, 'contents_with_name'] = documents.apply(f.prepare_contents_for_concatenation, args=(), axis=1)

    texts_per_case = pd.DataFrame(documents.groupby('id')['contents_with_name'].agg(''.join))
    texts_per_case.rename(columns={'contents_with_name': 'contents'}, inplace=True)

    return texts_per_case


def encode_diagnoses(diag_lists: pd.DataFrame, diag_defs: list[str], printing_if: bool) -> pd.DataFrame:
    f.print_if('hot-encoding diagnoses', printing_if)
    diagvec_per_case = diag_lists.apply(f.get_hot_diagnoses, axis=1)
    diagvec_per_case['id'] = diag_lists['id']
    diagvec_per_case.columns = diag_defs + ['id']
    diagvec_per_case.set_index('id', inplace=True)
    diagvec_per_case.drop('empty', axis=1, inplace=True)

    return diagvec_per_case
