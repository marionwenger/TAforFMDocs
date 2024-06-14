import time

import pandas as pd
from sklearn.model_selection import train_test_split

import t01_Import as t01
import t02_Exclude as t02
import t03_Unite_Encode as t03
import t04_Modell as t04
from functions import functions as f


def main(diag_defs: list[str]):
    f.print_if('--- MAIN ---', printing_if)

    # DOCUMENTS
    folder_intermed_name = 'intermed_results'
    file_doc_name = f'O_all_doc_exports_{data_input_version_id}'
    file_diaglist_name = f'O_all_diaglist_exports_{data_input_version_id}'

    f.print_if('--- t01 IMPORT & PROCESS DOCUMENTS ---', printing_if)
    if import_docs_anew:
        # %% t01 IMPORT
        fm_doc_exports = t01.import_documents(data_input_version_id, start_time, digits, printing_if)
        f.print_if('imported fm exports', printing_if)
        f.save_to_csv(fm_doc_exports, folder_intermed_name, file_doc_name, False, saving_to_csv,
                      printing_if)
    else:
        # parsing already done
        fm_doc_exports = f.read_from_csv(folder_intermed_name, file_doc_name, printing_if)
        f.print_if('used former documents import', printing_if)

    fm_doc_exports = t01.process_documents(fm_doc_exports, random_seed, printing_if,
                                           test_on, test_case_ids)
    f.print_if('processed documents', printing_if)

    # t02 %% EXCLUDE recommendations
    f.print_if('--- t02 EXCLUDE DOCUMENTS---', printing_if)
    documents = t02.exclude(fm_doc_exports, printing_if)
    f.print_if('excluded internally generated documents', printing_if)

    # DIAGNOSES LISTS
    f.print_if('--- t01 IMPORT & PROCESS DIAGLISTS ---', printing_if)
    if import_diaglists_anew:
        # %% t01 IMPORT
        fm_diaglist_exports: pd.DataFrame = t01.import_diaglists(data_input_version_id, start_time, digits,
                                                                 printing_if)
        fm_diaglist_exports = t01.process_diaglists(fm_diaglist_exports, random_seed, printing_if,
                                                    test_on, test_case_ids)
        f.print_if('processed diag lists', printing_if)
        f.save_to_csv(fm_diaglist_exports, folder_intermed_name, file_diaglist_name, True, saving_to_csv,
                      printing_if)
    else:  # TODO LATER rearrange code with methods so there are less duplicated statements
        # parsing already done
        fm_diaglist_exports = f.read_from_csv(folder_intermed_name, file_diaglist_name, printing_if)
        fm_diaglist_exports['id'] = fm_diaglist_exports['id'].astype(str)
        for i in range(1, fm_diaglist_exports.shape[1] - 1):
            fm_diaglist_exports[f'diag_{i}'] = fm_diaglist_exports[f'diag_{i}'].astype(str)
        f.print_if('used former diaglist import', printing_if)

    # %% t03 UNITE
    f.print_if('--- t03 UNITE TEXTS PER CASE ---', printing_if)
    texts_per_case = t03.unite_texts_per_case(documents, printing_if, random_seed, test_on, test_case_ids)
    file_texts_name = f'O_all_texts_exports_{data_input_version_id}'
    f.save_to_csv(texts_per_case, folder_intermed_name, file_texts_name, True, saving_to_csv, printing_if)
    f.print_if('united texts per case', printing_if)

    # %% t03 ENCODE
    f.print_if('--- t03 ENCODE DIAGNOSES ---', printing_if)
    diagvec_per_case = t03.encode_diagnoses(fm_diaglist_exports, diag_defs, printing_if)
    file_diagvec_name = f'O_diag_vectors_{data_input_version_id}'
    f.save_to_csv(diagvec_per_case, folder_intermed_name, file_diagvec_name, False, saving_to_csv, printing_if)
    f.print_if('encoded diagnoses', printing_if)

    texts_per_case.index = texts_per_case.index.astype(str)
    diagvec_per_case.index = diagvec_per_case.index.astype(str)
    texts_per_case = f.anonymize_and_index(texts_per_case, random_seed, test_on, test_case_ids, printing_if)
    diagvec_per_case = f.anonymize_and_index(diagvec_per_case, random_seed, test_on, test_case_ids, printing_if)
    # TODO LATER for kispi usage - check why so few rows remain... (see README for the numbers)
    merged_ids = sorted(set(texts_per_case.index) & set(diagvec_per_case.index))
    f.print_if(f'nr of common ta ids in texts and diaglists is {len(merged_ids)}', printing_if)

    # prepare for merge

    # inner join on index, but keep index
    combined_data: pd.DataFrame = pd.merge(texts_per_case, diagvec_per_case, left_index=True, right_index=True)
    file_modell_input_name = f'O_modell_input_{data_input_version_id}'
    f.save_to_csv(combined_data, folder_intermed_name, file_modell_input_name, False, saving_to_csv, printing_if)

    # prepare for modell
    target_col_first = 1
    df_x, df_y = f.split_in_dependents(target_col_first, combined_data)
    x_train, x_test, y_train_true, y_test_true = train_test_split(df_x, df_y, test_size=test_size,
                                                                  random_state=random_seed)

    # remove diagnoses which do not occur in test data
    y_train_true = pd.DataFrame(y_train_true.loc[:, (y_train_true != 0).any(axis=0)])
    if only_one_diag_run:
        y_train_true = pd.DataFrame(y_train_true[y_train_true.columns[0]])
    existing_diagnoses = y_train_true.columns
    y_test_true = y_test_true[existing_diagnoses]
    f.print_if(f'nr of diagnoses with a positive sample is {len(existing_diagnoses)}', printing_if)
    diag_defs = sorted(set(diag_defs) & set(existing_diagnoses), key=diag_defs.index)

    folder_final_name = 'meta_data'
    file_log_regr_pred_name = f'O_log_regr_pred_{data_input_version_id}'
    file_log_regr_f1_name = f'O_log_regr_f1_{data_input_version_id}'
    # TODO NOW (dict -> df) does not work (to save the results of log regr)
    # if predict_log_regr_anew:
    log_regr_f1_scores, log_regr_predictions = t04.predict_log_regr(diag_defs, x_train, x_test,
                                                                    y_train_true, y_test_true, printing_if,
                                                                    start_time, digits)

    f.print_if('--- sklearn.LogisticRegression Results ---', printing_if)
    f.print_if('f1 scores per diagnosis', printing_if)
    f.print_if('f1 = 1.0 means that there was no positive sample and no training', printing_if)
    f.print_if(log_regr_f1_scores, printing_if, True)

    #     log_regr_pred = pd.DataFrame.from_dict(log_regr_predictions)
    #     log_regr_f1 = pd.DataFrame.from_dict(log_regr_f1_scores)
    #     f.save_to_csv(log_regr_pred, folder_intermed_name, file_log_regr_pred_name, True, saving_to_csv, printing_if)
    #     f.save_to_csv(log_regr_f1, folder_final_name, file_log_regr_f1_name, True, saving_to_csv, printing_if)
    #
    # else:
    #     log_regr_pred = f.read_from_csv(folder_intermed_name, file_log_regr_pred_name, printing_if)
    #     log_regr_f1 =  f.read_from_csv(folder_final_name, file_log_regr_f1_name, printing_if)
    #     log_regr_pred['id'] = log_regr_pred['id'].astype(str)
    #     log_regr_f1['id'] = log_regr_f1['id'].astype(str)
    #     f.print_if('used former log regr predictions', printing_if)
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
    digits = 3
    print(f'--- START TIME = {f.print_time(start_time, digits)} ---')

    saving_to_csv = True
    printing_if = True

    # TODO LATER different version ids for diaglists and docs
    data_input_version_id = 'div_1.1'  # only different for diaglists: 1.0 Marions Export 1.1 Emis Export (200610)
    data_version_id = 1

    random_seed: int = 1404
    current_year = int(time.strftime("%Y"))
    data_years = [2013, current_year]
    # TODO NOW or LATER improve predictions by separating Vor-/Nachschule

    # False = parsing already done (it's time-consuming...)
    import_docs_anew = False  # import takes about 3 minutes
    import_diaglists_anew = False  # import takes 8 seconds (used to take half a minute with data input version 1.0)

    # test_case_ids[i] <--> test_ta_ids[i]
    test_on = False
    test_case_ids = [22225, 23619, 51285]
    # um id in diaglist zu testen, muss import_diaglists_anew auf True gesetzt werden
    # bei docs hingegen nicht, da dort die ID-Generierung erst später stattfindet
    # test_ta_ids = ['TA-MZZ3EI', 'TA-4X4219', 'TA-HNT0K0'] # TODO LATER set up test

    diag_defs: list[str] = ['empty',  # 0  # TODO LATER remove here and change indices in method accordingly...
                            "LKG",  # 1
                            "myofunkt. Dysfunk.",  # 2
                            "Fehlbildung: Div.",  # 3
                            "Gehirn: Div.",  # 4
                            "Blutung",  # 5
                            "CP",  # 6
                            "Epilepsie",  # 7
                            "kard. Erkrank.",  # 8
                            "Audit. Verarbeit./Wahrnehm.stör",  # 9
                            "Fütter/Essstör",  # 10
                            "Hörstör (o. CI)",  # 11
                            "Hörstör mit CI",  # 12
                            "Schluckstör",  # 13
                            "Sehstör",  # 14
                            "Trinkschwäche",  # 15
                            "Organisch: Div.",  # 16
                            "Syndrom: Div.",  # 17
                            "Tris21",  # 18
                            "Feinmotorik",  # 19
                            "Grobmotorik",  # 20
                            "Oralmotorik",  # 21
                            "Globaler ER",  # 22
                            "Kognitiver ER",  # 23
                            "SES expr mehrspr",  # 24
                            "SES expr mono",  # 25
                            "SES Komorb mehrspr",  # 26
                            "SES Komorb mono",  # 27
                            "SES rezep mehrspr",  # 28
                            "SES rezep mono",  # 29
                            "SES rezep expr mehrspr",  # 30
                            "SES rezep expr mono",  # 31
                            "SEV expr mehrspr",  # 32
                            "SEV expr mono",  # 33
                            "SEV expr rezep mehrspr",  # 34
                            "SEV expr rezep mono",  # 35
                            "Sprachentwicklung: Div.",  # 36
                            "Erworbene Sprachstör",  # 37
                            "Rhinolalie",  # 38
                            "Stimmstör",  # 39
                            "Stottern",  # 40
                            "Sprachstör: Div.",  # 41
                            "AD(H)S",  # 42
                            "ASS",  # 43
                            "Emotionale/soziale Stör",  # 44
                            "Mutismus",  # 45
                            "Regulationsstör",  # 46
                            "Verhalten: Div.",  # 47
                            "Geburt",  # 48
                            "Langzeithospital.",  # 49
                            "Umfeldproblematik",  # 50
                            "Risikofaktoren: Div.",  # 51
                            "Div. Diagnosen",  # 52
                            "Dyskalkulie",  # 53
                            "Isolierte Lesestör",  # 54
                            "Isolierte Rechtschreibstör",  # 55
                            "Dyslexie",  # 56
                            "Schule: Div."  # 57]
                            ]

    test_size: float = 0.33

    only_one_diag_run: bool = True  # predict only one diagnoses
    predict_log_regr_anew = True  # prediction takes almost 10 minutes

    # TODO LATER replace with meta parameter table, see Melanie
    f.print_if(f'--- data variables ---'
                  f'\ndata_years = {data_years[0]} - {data_years[1]} '
                  f'\ndata_input_version_id = {data_input_version_id} '
                  f'\ndata_version_id = {data_version_id} '
                  f'\n--- process variables --- '
                  f'\nrandom_seed = {random_seed} '
                  f'\nimport_docs_anew = {import_docs_anew} '
                  f'\nimport_diaglists_anew = {import_diaglists_anew}'
               f'\nsaving_to_csv = {saving_to_csv}'
               f'\ntest_on = {test_on}'
               f'\ntest_case_ids = {test_case_ids}'
               f'\ntest_size = {test_size}'
               f'\nonly_one_diag_run = {only_one_diag_run}'
               f'\npredict_log_regr_anew = {predict_log_regr_anew}',
               printing_if)

    main(diag_defs)

    print(f'--- END TIME = {f.print_time(time.time(), digits)} ---')
    print(f'--- RUNNING TIME = {f.get_running_time(start_time, digits)} ---')
