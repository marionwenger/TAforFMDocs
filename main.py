# %% meta data tables
# data_versions: mf.DataVersionTable = mf.DataVersionTable()
# data_processes: mf.DataProcessTable = mf.DataProcessTable()
# tests: tf.TestTable = tf.TestTable(66)  # miss factor
# modells: mf.ModellTable = mf.ModellTable()
# evals: mf.EvalTable = mf.EvalTable(4)  # precision in digits
# bad_modells: list[int] = []  # are not trained and printed

# %%
import steps.t01_Import as t01

print(t01.exports[0:1])

import steps.t02_Transform as t02

print(t02.exports[0:1])

# %%
# TODO LATER add tests
# import steps.m03_Preprocess as m03
#
# data_processes.add_data_process(m03.data_process_id, 'No', 'mean'
#                                 , 'z-transformed (SimpleImputer)', 'one-hot'
#                                 , 'No', m03.test_size, 'no test of normal distribution, no check of outliers')
#
# tests.add_test_result(f' <= {tests.miss_factor}% of missing values per column'
#                       , tf.test_for_few_nans(m03.kids_x, tests.miss_factor, data_name))
# tests.add_test_result('all rows are put into the modell'
#                       , math.floor(len(m02.kids) * (1 - m03.test_size)) == len(m03.x_train))

# TODO LATER backup of intermediate results
# filepath_independ_train = Path(f'intermed_results/O_independ_train_{data_processes.get_print_version()}.csv')
# m03.x_train.to_csv(filepath_independ_train)

# %%
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

# %%
# TODO LATER print meta tables
# mf.print_meta_tables(data_versions, data_processes, tests, modells, evals, bad_modells,
#                      print_modells=True)

# %%
# TODO LATER save meta tables
# filepath_data_versions = Path(f'meta_data/MI_data_versions_{data_versions.get_print_version()}.csv')
# data_versions.df.to_csv(filepath_data_versions)
