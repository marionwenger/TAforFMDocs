import re

import pandas as pd

from functions import functions as f

# geordnet nach vermuteter Seltenheit in anderen Dokumenten ⇨ lazy OR ist ok!
forbidden_texts = ['Höchstzahl Stunden:', 'Gültigkeit und Dauer:', 'Form der Durchführung:', 'Ort der Durchführung:',
                   'Art der Leistung:']


def exclude(fm_doc_exports: pd.DataFrame, input_seed: int, printing_steps: bool = False) -> pd.DataFrame:
    f.print_steps('exclusion of documents', printing_steps)

    # Create a single regular expression pattern from the forbidden text snippets
    pattern = '|'.join(map(re.escape, forbidden_texts))
    # map(re.escape, forbidden_texts): Escapes each forbidden text snippet to handle any special characters.
    # |.join(...): Joins the escaped snippets with the regex OR operator (|),
    # creating a pattern that matches any of the snippets.

    # Filter the DataFrame
    fm_doc_exports = fm_doc_exports[~fm_doc_exports['contents'].str.contains(pattern, case=True, na=True)]
    # case=False: Makes the matching case-insensitive.
    # na=False: Treats NaN values as not matching the pattern.
    # ~: Negates the boolean mask to filter out rows that match the forbidden text snippets.

    # Alternativer Ausschluss über Dokumentname: exclude 'Empfehlung' und falls das nicht reicht auch 'AJB'
    return fm_doc_exports
