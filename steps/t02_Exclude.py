import pandas as pd

from functions import functions as f


def exclude(fm_doc_exports: pd.DataFrame, random_seed: int, printing_steps: bool = False) -> pd.DataFrame:
    f.print_steps('started with t02', printing_steps)

    # %% TODO erstes exclude mithilfe von filename ohne Text selber...
    # TODO zweites exclude anhand mr_translations Textstücken (OCR-Erkennung testen!)

    documents = pd.DataFrame()

    return documents
