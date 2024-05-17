import pandas as pd

import t01_Import as t01
import t02_Split as t02
from functions import functions as f


# TODO NOW why does it not print out??? is it a stream I have to catch???

def main(saving, debugging):
    f.print_if_debugging('started with main', debugging)

    # t01 IMPORT
    fm_exports: pd.DataFrame = t01.import_fm_exports(debugging)
    f.print_if_debugging('t01: imported fm exports', debugging)
    f.save_to_csv(fm_exports, 'intermed_results', f'O_exports_{data_input_version_id}', saving, debugging)

    # t02 SPLIT
    cases, documents = t02.split(fm_exports, debugging)
    f.print_if_debugging('t02: splitted cases and documents', debugging)
    f.save_to_csv(cases, 'intermed_results', f'O_cases_{data_input_version_id}', False, debugging)
    f.save_to_csv(documents, 'intermed_results', f'O_documents_{data_input_version_id}', False, debugging)

    # TODO LATER add tests for steps
    # data_processes.add_data_process(m03.data_process_id, 'No', 'mean'
    #                                 , 'z-transformed (SimpleImputer)', 'one-hot'
    #                                 , 'No', m03.test_size, 'no test of normal distribution, no check of outliers')
    #
    # tests.add_test_result(f' <= {tests.miss_factor}% of missing values per column'
    #                       , tf.test_for_few_nans(m03.kids_x, tests.miss_factor, data_name))
    # tests.add_test_result('all rows are put into the modell'
    #                       , math.floor(len(m02.kids) * (1 - m03.test_size)) == len(m03.x_train))

    # TODO LATER import modell steps
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
    # global variables
    saving = True
    debugging = True

    # TODO CLEANUP do I need this?
    data_input_version_id = 'div_1.0'
    data_version_id = 1
    random_seed: int = 1404

    main(saving, debugging)
