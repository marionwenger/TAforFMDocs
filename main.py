import time

import pandas as pd

import t01_Import as t01
import t02_Exclude as t02
from functions import functions as f


def main(saving_to_csv: bool, printing_steps: bool, data_input_version_id: str, input_seed: int,
         data_years: list[int], start_time, import_docs_anew):
    f.print_steps('--- main ---', printing_steps)

    # DOCUMENTS
    folder_name = 'intermed_results'
    file_name = f'O_all_doc_exports_{data_input_version_id}'

    f.print_steps('--- t01 IMPORT ---', printing_steps)
    if import_docs_anew:
        # %% t01 IMPORT
        fm_doc_exports = t01.import_documents(data_years, data_input_version_id, start_time, printing_steps)
        f.print_steps('imported fm exports', printing_steps)
        f.save_to_csv(fm_doc_exports, folder_name, file_name, saving_to_csv,
                      printing_steps)
    else:
        # parsing already done
        fm_doc_exports = f.read_from_csv(folder_name, file_name, printing_steps)
        f.print_steps('used former import', printing_steps)

    fm_doc_exports = t01.process_documents(fm_doc_exports, input_seed, printing_steps)
    f.print_steps('processed documents', printing_steps)

    # t02 %% EXCLUDE
    f.print_steps('--- t02 EXCLUDE ---', printing_steps)
    documents = t02.exclude(fm_doc_exports, random_seed, printing_steps)
    f.print_steps('excluded internally generated documents', printing_steps)

    # TODO NEXT (IV) import & process diaglist (after exclusion of recommendations, that is more interesting for ZHAW...)
    # DIAGNOSES LISTS
    fm_diaglist_exports = pd.DataFrame()
    fm_diaglist_exports = t01.import_diaglists(data_years, data_input_version_id, start_time, printing_steps)
    fm_diaglist_exports = t01.process_diagllists(fm_diaglist_exports, printing_steps)
    # TODO save csv
    # f.save_to_csv(documents, 'intermed_results', f'O_nogen_documents_{data_input_version_id}',
    # saving_to_csv, printing_steps)

    # %% TODO LATER t03 UNITE
    # TODO LATER clean & preprocess diagnoses (docs are fine), see Melanie
    # TODO LATER split into training and test data, see Melanie

    # %% TODO LATER add tests for steps
    # data_processes.add_data_process(m03.data_process_id, 'No', 'mean'
    #                                 , 'z-transformed (SimpleImputer)', 'one-hot'
    #                                 , 'No', m03.test_size, 'no test of normal distribution, no check of outliers')
    #
    # tests.add_test_result(f' <= {tests.miss_factor}% of missing values per column'
    #                       , tf.test_for_few_nans(m03.kids_x, tests.miss_factor, data_name))
    # tests.add_test_result('all rows are put into the modell'
    #                       , math.floor(len(m02.kids) * (1 - m03.test_size)) == len(m03.x_train))

    # %% TODO LATER import modell steps
    # import steps.m04_Mod_Poly_Reg as m04
    #
    # if not m04.m04_train_all:
    #     bad_modells.extend(m04.m04_bad_modells)
    #
    # # modell 001
    # if m04.modell_id_001 not in bad_modells:
    #     modells.add_modell(m04.modell_id_001, m04.modell_name_001, 'poly regr', f'degree {m04.poly_degree_001}'
    #                        , m04.nr_params_001, f'No, shift {m04.y_shift_001}, sigmoid & round'
    #                        , 'Alisa recommended starting with degree 2, no more')
    #
    #     evals.add_eval(m04.eval_id_001, m02.data_version_id, m03.data_process_id, m03.random_seed, m04.modell_id_001,
    #                    m04.acc_001
    #                    , 'very frustrating for my first modell ever...')

    # %% TODO LATER meta data tables
    # data_versions: mf.DataVersionTable = mf.DataVersionTable()
    # data_processes: mf.DataProcessTable = mf.DataProcessTable()
    # tests: tf.TestTable = tf.TestTable(66)  # miss factor
    # modells: mf.ModellTable = mf.ModellTable()
    # evals: mf.EvalTable = mf.EvalTable(4)  # precision in digits
    # bad_modells: list[int] = []  # are not trained and printed

    # TODO LATER print meta tables
    # mf.print_meta_tables(data_versions, data_processes, tests, modells, evals, bad_modells,
    #                      print_modells=True)

    # TODO LATER save meta tables
    # filepath_data_versions = Path(f'meta_data/MI_data_versions_{data_versions.get_print_version()}.csv')
    # data_versions.df.to_csv(filepath_data_versions)

if __name__ == "__main__":
    start_time = time.time()

    # global variables
    saving_to_csv = True
    printing_steps = True

    # TODO CLEANUP do I need this?
    data_input_version_id = 'div_1.0'
    data_version_id = 1
    random_seed: int = 1404
    current_year = int(time.strftime("%Y"))
    data_years = [2013, current_year]

    import_docs_anew = False  # False = parsing already done (it's time-consuming...)

    # TODO LATER replace with meta parameter table, see Melanie
    f.print_steps(f'--- DATA ---\ndata years {data_years[0]} - {data_years[1]} \ndata input version '
                  f'{data_input_version_id} \ndata version {data_version_id} \nPROCESSING with \nrandom seed {random_seed} '
                  f'\nimport_docs_anew = {import_docs_anew} \nsaving_to_csv = {saving_to_csv}',
                  printing_steps)

    main(saving_to_csv, printing_steps, data_input_version_id, random_seed, data_years, start_time, import_docs_anew)

    print(f'--- {f.get_running_time(start_time, 3)} ---')
    end_time = time.time()
