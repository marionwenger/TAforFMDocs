# TODO LATER for kispi usage - anonymize data (names, adresses, etc.) and use model ONLINE

import time
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, recall_score

from functions import functions as f


def predict_log_regr_per_diagn(x_train: pd.DataFrame, x_test: pd.DataFrame, train_labels: pd.Series,
                               test_labels: pd.Series) \
        -> pd.DataFrame | float | float | float:
    # L03P05 Text Classification with Word Embeddings
    # Run a TF-IDF + LogReg baseline on the data

    # TFIDF Vectorization and data handling
    vectorizer = TfidfVectorizer()
    train_features = vectorizer.fit_transform(x_train['contents'].tolist())
    test_features = vectorizer.transform(x_test['contents'].tolist())

    # Classifier training: Try changing the C and class_weight parameters
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
    # C
    # Inverse of regularization strength; must be a positive float.
    # Like in support vector machines, smaller values specify stronger regularization.
    # max_iter
    # Maximum number of iterations taken for the solvers to converge.
    # class_weight
    # Weights associated with classes in the form {class_label: weight}.
    # If not given, all classes are supposed to have weight one.
    classifier = LogisticRegression(C=1, max_iter=10000, class_weight=None)
    classifier.fit(train_features, train_labels)

    predicted_labels_tf_log_reg = classifier.predict(test_features)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        #  UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples.
        #  Use `zero_division` parameter to control this behavior.
        f1_tf_log_reg = f1_score(test_labels, predicted_labels_tf_log_reg, average='macro', zero_division=np.nan)
        acc_log_reg = accuracy_score(test_labels, predicted_labels_tf_log_reg)
        recall_log_reg = recall_score(test_labels, predicted_labels_tf_log_reg, zero_division=np.nan)
        # TODO LATER calc other metrics
        #  confusion_matrix(y_true, y_pred, *, labels=None, sample_weight=None, normalize=None):
        #  multilabel_confusion_matrix( y_true, y_pred, *, sample_weight=None, labels=None, samplewise=False)
        #  class_report_tf_log_reg = classification_report(test_labels, predicted_labels_tf_log_reg, zero_division=np.nan)
        # if printing_if: print(class_report_tf_log_reg)

    return pd.DataFrame({'predicted_labels': predicted_labels_tf_log_reg}), f1_tf_log_reg, acc_log_reg, recall_log_reg


def predict_log_regr(diag_defs: list[str], x_train: pd.DataFrame, x_test: pd.DataFrame,
                     y_train_true: pd.DataFrame, y_test_true: pd.DataFrame, printing_if: bool,
                     start_time, digits) \
        -> tuple[dict, dict, dict, dict]:
    start_time_prediction = time.time()
    log_regr_f1_scores: dict = {}
    log_regr_acc_scores: dict = {}
    log_regr_recall_scores: dict = {}
    log_regr_predictions: dict = {}
    f.print_if('start prediction with logistic regression', printing_if)

    for diagnosis in diag_defs:
        train_labels = pd.Series(y_train_true[diagnosis])
        test_labels = pd.Series(y_test_true[diagnosis])
        diagnosis_prediction, diagnosis_f1, diagnosis_acc, diagnosis_recall = predict_log_regr_per_diagn(x_train,
                                                                                                         x_test,
                                                                                                         train_labels,
                                                                                                         test_labels)
        log_regr_predictions[diagnosis] = diagnosis_prediction
        log_regr_f1_scores[diagnosis] = diagnosis_f1
        log_regr_acc_scores[diagnosis] = diagnosis_acc
        log_regr_recall_scores[diagnosis] = diagnosis_recall
        f.print_if(f'diagnosis "{diagnosis}" predicted after {f.get_running_time(start_time, digits)}'
                   , printing_if)

    f.print_if(f'predicted all diagnoses after {f.get_running_time(start_time, digits)}', printing_if)
    f.print_if(f'prediction took {f.get_running_time(start_time_prediction, digits)}', printing_if)

    return log_regr_f1_scores, log_regr_acc_scores, log_regr_recall_scores, log_regr_predictions


def predict_rand_forest(x_train, x_test, y_train_true) -> dict:
    corpus = x_train['contents'].to_list()
    Y = np.array(y_train_true).ravel()  # TODO LATER generalize for more than one dimension/diagnosis
    existing_diagnoses = y_train_true.columns
    # Creating bag-of-words using CountVectorizer
    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    clf = RandomForestClassifier()
    clf.fit(X, Y)  # TODO LATER this takes hours - is it stuck??? no error messages...
    rand_forest_results: dict = {}
    for row in x_test:
        rand_forest_predictions: dict = {}
        for diagnosis in existing_diagnoses:
            rand_forest_predictions[diagnosis] = clf.predict(vectorizer.transform(row['contents']).toarray())
        rand_forest_results[row.index] = rand_forest_predictions
    return rand_forest_results
