# TODO LATER for kispi usage - anonymize data (names, adresses, etc.) and use model ONLINE

import warnings

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from functions import functions as f


def predict_log_regr(x_train: pd.DataFrame, x_test: pd.DataFrame, train_labels: pd.Series, test_labels: pd.Series) \
        -> pd.DataFrame | float:
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
        # TODO LATER read other metrics directly or via report
        # class_report_tf_log_reg = classification_report(test_labels, predicted_labels_tf_log_reg, zero_division=np.nan)
        # if printing_steps: print(class_report_tf_log_reg)
        f1_tf_log_reg = f1_score(test_labels, predicted_labels_tf_log_reg, average='macro', zero_division=np.nan)

    return pd.DataFrame({'predicted_labels': predicted_labels_tf_log_reg}), f1_tf_log_reg


def diagnosis_prediction_dict(diag_defs: list[str], x_train: pd.DataFrame, x_test: pd.DataFrame,
                              y_train_true: pd.DataFrame, y_test_true: pd.DataFrame, printing_steps: bool) \
        -> tuple[dict, dict]:
    modell_f1_scores: dict = {}
    modell_predictions: dict = {}
    f.print_steps('start prediction with logistic regression', printing_steps)
    for diagnosis in diag_defs:
        train_labels = pd.Series(y_train_true[diagnosis])
        test_labels = pd.Series(y_test_true[diagnosis])
        diagnosis_prediction, diagnosis_f1 = predict_log_regr(x_train, x_test, train_labels, test_labels)
        modell_predictions[diagnosis] = diagnosis_prediction
        # TODO LATER ta_id is gone...
        modell_f1_scores[diagnosis] = diagnosis_f1

    return modell_f1_scores, modell_predictions
