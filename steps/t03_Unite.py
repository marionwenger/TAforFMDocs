import pandas as pd

from functions import functions as f


def unite_texts_per_case(documents: pd.DataFrame, printing_steps: bool) -> pd.DataFrame:
    f.print_steps('uniting texts per case', printing_steps)

    # TODO NOW ensure that the ta id stays the same for the texts of a case (test with one row...)

    # Ensure no NaN values interfere with concatenation (I think there are none...)
    documents.loc[:, 'contents'] = documents['contents'].fillna('')
    documents.loc[:, 'name'] = documents['name'].fillna('')

    # TODO NOW SettingWithCopyWarning:
    #  A value is trying to be set on a copy of a slice from a DataFrame.
    #  Try using .loc[row_indexer,col_indexer] = value instead
    documents.loc[:, 'contents_with_name'] = ""
    documents.loc[:, 'contents_with_name'] = documents.apply(f.prepare_contents_for_concatenation, args=(), axis=1)

    texts_per_case = pd.DataFrame(documents.groupby('id')['contents_with_name'].agg(''.join))
    texts_per_case.rename(columns={'contents_with_name': 'contents'}, inplace=True)

    return texts_per_case
