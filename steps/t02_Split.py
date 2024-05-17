import pandas as pd

from functions import functions as f


# TODO NOW split into two tables - cases and documents with a new internal document ID...
def split(fm_exports: pd.DataFrame, debugging: bool = False) -> (pd.DataFrame, pd.DataFrame):
    f.print_if_debugging(debugging, 'started with t02')

    # TODO LATER adapt code: fName_Vorname_Kind will be missing as a column (new export by Emi)

    # List of columns for each new DataFrame
    # TODO rename
    cases_columns = ['ID_FM', 'fName_Vorname_Kind', 'ID_Fall', 'fAnmeldedatum', ]
    documents_columns = ['filename', 'TextMBSVisionLength', 'TextMBSVision']

    # Create new DataFrames
    # cases = exports[cases_columns]
    # documents = exports[documents_columns]
    cases = pd.DataFrame([cases_columns])
    documents = pd.DataFrame([documents_columns])

    # Reset index to create a new unique ID for each row
    # TODO why is this bijective?
    # cases.reset_index(drop=True, inplace=True)
    # documents.reset_index(drop=True, inplace=True)

    # Add a new ID column to both DataFrames
    # TODO use loc instead
    # cases['DocID'] = range(1, len(cases) + 1)
    # documents['DocID'] = range(1, len(documents) + 1)

    # TODO change order of columns

    # # Print the new DataFrames
    # f.print_if_debugging(debug, "cases:")
    # f.print_if_debugging(debug, cases.head)
    # f.print_if_debugging(debug, "\ndocuments:")
    # f.print_if_debugging(debug, documents)

    return cases, documents
