import time

import t01_Import as t01
import t02_Exclude as t02
from functions import functions as f


def main(saving_to_csv: bool, printing_steps: bool, data_input_version_id: str, random_seed: int,
         data_years: list[int], start_time):
    f.print_steps('started with main', printing_steps)

    # %% t01 IMPORT
    fm_doc_exports, fm_diaglist_exports = t01.import_fm_exports(data_years, data_input_version_id,
                                                                start_time, printing_steps)
    f.print_steps('t01: imported fm exports', printing_steps)
    f.save_to_csv(fm_doc_exports, 'intermed_results', f'O_all_doc_exports_{data_input_version_id}', saving_to_csv,
                  printing_steps)

    # t02 %% EXCLUDE
    documents = t02.exclude(fm_doc_exports, random_seed, printing_steps)
    f.print_steps('t02: excluded internally generated documents', printing_steps)
    # TODO LATER save csv
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

    # TODO replace with meta parameter table, see Melanie
    f.print_steps(f'---\nDATA from the years {data_years[0]} - {data_years[1]} with \ndata input version '
                  f'{data_input_version_id} and \ndata version {data_version_id} \nPREPROCESSING with \nrandom seed {random_seed} \n---',
                  printing_steps)

    main(saving_to_csv, printing_steps, data_input_version_id, random_seed, data_years, start_time)

    print("--- %s seconds ---" % round((time.time() - start_time), 3))
