# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import numpy as np
import pandas as pd
import pytest
import sklearn.metrics as sklearn_metrics  # type: ignore

import bigframes.ml.metrics


def test_r2_score_perfect_fit(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [1, 7, 3, 2, 5],
            "y_pred_arbitrary_name": [1, 7, 3, 2, 5],
        }
    )

    df = session.read_pandas(pd_df)
    assert (
        bigframes.ml.metrics.r2_score(
            df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]]
        )
        == 1.0
    )


def test_r2_score_bad_fit(session):
    pd_df = pd.DataFrame({"y_true": [1, 2, 3, 4, 5], "y_pred": [5, 4, 3, 2, 1]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.r2_score(df[["y_true"]], df[["y_pred"]]) == -3.0


def test_r2_score_force_finite(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [1, 1, 1, 1, 1],
            "y_pred_1": [5, 4, 3, 2, 1],
            "y_pred_2": [1, 1, 1, 1, 1],
        }
    )

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.r2_score(
        df[["y_true"]], df[["y_pred_1"]], force_finite=False
    ) == float("-inf")
    assert bigframes.ml.metrics.r2_score(df[["y_true"]], df[["y_pred_1"]]) == 0.0
    assert math.isnan(
        bigframes.ml.metrics.r2_score(
            df[["y_true"]], df[["y_pred_2"]], force_finite=False
        )
    )
    assert bigframes.ml.metrics.r2_score(df[["y_true"]], df[["y_pred_2"]]) == 1.0


def test_r2_score_ok_fit_matches_sklearn(session):
    pd_df = pd.DataFrame({"y_true": [1, 2, 3, 4, 5], "y_pred": [2, 3, 4, 3, 6]})

    df = session.read_pandas(pd_df)
    bf_result = bigframes.ml.metrics.r2_score(df[["y_true"]], df[["y_pred"]])
    sklearn_result = sklearn_metrics.r2_score(pd_df[["y_true"]], pd_df[["y_pred"]])
    assert math.isclose(bf_result, sklearn_result)


def test_r2_score_series(session):
    pd_df = pd.DataFrame({"y_true": [1, 7, 3, 2, 5], "y_pred": [1, 7, 3, 2, 5]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.r2_score(df["y_true"], df["y_pred"]) == 1.0


def test_accuracy_score_perfect_fit(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [1, 7, 3, 2, 5],
            "y_pred_arbitrary_name": [1, 7, 3, 2, 5],
        }
    )

    df = session.read_pandas(pd_df)
    assert (
        bigframes.ml.metrics.accuracy_score(
            df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]]
        )
        == 1.0
    )


def test_accuracy_score_bad_fit(session):
    pd_df = pd.DataFrame({"y_true": [0, 2, 1, 3, 4], "y_pred": [0, 1, 2, 3, 4]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.accuracy_score(df[["y_true"]], df[["y_pred"]]) == 0.6


def test_accuracy_score_not_normailze(session):
    pd_df = pd.DataFrame({"y_true": [0, 2, 1, 3, 4], "y_pred": [0, 1, 2, 3, 4]})

    df = session.read_pandas(pd_df)
    assert (
        bigframes.ml.metrics.accuracy_score(
            df[["y_true"]], df[["y_pred"]], normalize=False
        )
        == 3
    )


def test_accuracy_score_fit_matches_sklearn(session):
    pd_df = pd.DataFrame({"y_true": [1, 2, 3, 4, 5], "y_pred": [2, 3, 4, 3, 6]})

    df = session.read_pandas(pd_df)
    bf_result = bigframes.ml.metrics.accuracy_score(df[["y_true"]], df[["y_pred"]])
    sklearn_result = sklearn_metrics.accuracy_score(
        pd_df[["y_true"]], pd_df[["y_pred"]]
    )
    assert math.isclose(bf_result, sklearn_result)


def test_accuracy_score_series(session):
    pd_df = pd.DataFrame({"y_true": [1, 7, 3, 2, 5], "y_pred": [1, 7, 3, 2, 5]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.accuracy_score(df["y_true"], df["y_pred"]) == 1.0


def test_roc_curve_binary_classification_prediction_returns_expected(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score_arbitrary_name": [
                0.1,
                0.4,
                0.35,
                0.8,
                0.65,
                0.9,
                0.5,
                0.3,
                0.6,
                0.45,
            ],
        }
    )

    df = session.read_pandas(pd_df)
    fpr, tpr, thresholds = bigframes.ml.metrics.roc_curve(
        df[["y_true_arbitrary_name"]],
        df[["y_score_arbitrary_name"]],
        drop_intermediate=False,
    )

    pd_fpr = fpr.to_pandas()
    pd_tpr = tpr.to_pandas()
    pd_thresholds = thresholds.to_pandas()

    pd.testing.assert_series_equal(
        # skip testing the first value, as it is redundant and inconsistent across sklearn versions
        pd_thresholds[1:],
        pd.Series(
            [0.9, 0.8, 0.65, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.1],
            dtype="Float64",
            name="thresholds",
        ),
        check_index=False,
    )
    pd.testing.assert_series_equal(
        pd_fpr,
        pd.Series(
            [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 0.75, 1.0],
            dtype="Float64",
            name="fpr",
        ),
        check_index_type=False,
    )
    pd.testing.assert_series_equal(
        pd_tpr,
        pd.Series(
            [
                0.0,
                0.16666667,
                0.33333333,
                0.33333333,
                0.5,
                0.5,
                0.66666667,
                0.66666667,
                0.83333333,
                1.0,
                1.0,
            ],
            dtype="Float64",
            name="tpr",
        ),
        check_index_type=False,
    )


def test_roc_curve_binary_classification_prediction_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45],
        }
    )

    df = session.read_pandas(pd_df)
    fpr, tpr, thresholds = bigframes.ml.metrics.roc_curve(
        df[["y_true"]], df[["y_score"]], drop_intermediate=False
    )
    expected_fpr, expected_tpr, expected_thresholds = sklearn_metrics.roc_curve(
        pd_df[["y_true"]], pd_df[["y_score"]], drop_intermediate=False
    )

    # sklearn returns float64 np arrays
    np_fpr = fpr.to_pandas().astype("float64").array
    np_tpr = tpr.to_pandas().astype("float64").array
    np_thresholds = thresholds.to_pandas().astype("float64").array

    np.testing.assert_array_equal(
        # skip testing the first value, as it is redundant and inconsistent across sklearn versions
        np_thresholds[1:],
        expected_thresholds[1:],
    )
    np.testing.assert_array_equal(
        np_fpr,
        expected_fpr,
    )
    np.testing.assert_array_equal(
        np_tpr,
        expected_tpr,
    )


def test_roc_curve_binary_classification_decision_returns_expected(session):
    # Instead of operating on probabilities, assume a 70% decision threshold
    # has been applied, and operate on the final output
    y_score = [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45]
    decisions_70pct = [1 if s > 0.7 else 0 for s in y_score]
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": decisions_70pct,
        }
    )

    df = session.read_pandas(pd_df)
    fpr, tpr, thresholds = bigframes.ml.metrics.roc_curve(
        df[["y_true"]], df[["y_score"]], drop_intermediate=False
    )

    pd_fpr = fpr.to_pandas()
    pd_tpr = tpr.to_pandas()
    pd_thresholds = thresholds.to_pandas()

    pd.testing.assert_series_equal(
        # skip testing the first value, as it is redundant and inconsistent across sklearn versions
        pd_thresholds[1:],
        pd.Series(
            [1.0, 0.0],
            dtype="Float64",
            name="thresholds",
        ),
        check_index=False,
    )
    pd.testing.assert_series_equal(
        pd_fpr,
        pd.Series(
            [0.0, 0.0, 1.0],
            dtype="Float64",
            name="fpr",
        ),
        check_index_type=False,
    )
    pd.testing.assert_series_equal(
        pd_tpr,
        pd.Series(
            [
                0.0,
                0.33333333,
                1.0,
            ],
            dtype="Float64",
            name="tpr",
        ),
        check_index_type=False,
    )


def test_roc_curve_binary_classification_decision_matches_sklearn(session):
    # Instead of operating on probabilities, assume a 70% decision threshold
    # has been applied, and operate on the final output
    y_score = [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45]
    decisions_70pct = [1 if s > 0.7 else 0 for s in y_score]
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": decisions_70pct,
        }
    )

    df = session.read_pandas(pd_df)
    fpr, tpr, thresholds = bigframes.ml.metrics.roc_curve(
        df[["y_true"]], df[["y_score"]], drop_intermediate=False
    )
    expected_fpr, expected_tpr, expected_thresholds = sklearn_metrics.roc_curve(
        pd_df[["y_true"]], pd_df[["y_score"]], drop_intermediate=False
    )

    # sklearn returns float64 np arrays
    np_fpr = fpr.to_pandas().astype("float64").array
    np_tpr = tpr.to_pandas().astype("float64").array
    np_thresholds = thresholds.to_pandas().astype("float64").array

    np.testing.assert_array_equal(
        # skip testing the first value, as it is redundant and inconsistent across sklearn versions
        np_thresholds[1:],
        expected_thresholds[1:],
    )
    np.testing.assert_array_equal(
        np_fpr,
        expected_fpr,
    )
    np.testing.assert_array_equal(
        np_tpr,
        expected_tpr,
    )


def test_roc_curve_binary_classification_prediction_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45],
        }
    )

    df = session.read_pandas(pd_df)
    fpr, tpr, thresholds = bigframes.ml.metrics.roc_curve(
        df["y_true"], df["y_score"], drop_intermediate=False
    )

    pd_fpr = fpr.to_pandas()
    pd_tpr = tpr.to_pandas()
    pd_thresholds = thresholds.to_pandas()

    pd.testing.assert_series_equal(
        # skip testing the first value, as it is redundant and inconsistent across sklearn versions
        pd_thresholds[1:],
        pd.Series(
            [0.9, 0.8, 0.65, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.1],
            dtype="Float64",
            name="thresholds",
        ),
        check_index=False,
    )
    pd.testing.assert_series_equal(
        pd_fpr,
        pd.Series(
            [0.0, 0.0, 0.0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 0.75, 1.0],
            dtype="Float64",
            name="fpr",
        ),
        check_index_type=False,
    )
    pd.testing.assert_series_equal(
        pd_tpr,
        pd.Series(
            [
                0.0,
                0.16666667,
                0.33333333,
                0.33333333,
                0.5,
                0.5,
                0.66666667,
                0.66666667,
                0.83333333,
                1.0,
                1.0,
            ],
            dtype="Float64",
            name="tpr",
        ),
        check_index_type=False,
    )


def test_roc_auc_score_returns_expected(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score_arbitrary_name": [
                0.1,
                0.4,
                0.35,
                0.8,
                0.65,
                0.9,
                0.5,
                0.3,
                0.6,
                0.45,
            ],
        }
    )

    df = session.read_pandas(pd_df)
    score = bigframes.ml.metrics.roc_auc_score(
        df[["y_true_arbitrary_name"]], df[["y_score_arbitrary_name"]]
    )

    assert score == 0.625


def test_roc_auc_score_returns_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45],
        }
    )

    df = session.read_pandas(pd_df)
    score = bigframes.ml.metrics.roc_auc_score(df[["y_true"]], df[["y_score"]])
    expected_score = sklearn_metrics.roc_auc_score(
        pd_df[["y_true"]], pd_df[["y_score"]]
    )

    assert score == expected_score


def test_roc_auc_score_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            "y_score": [0.1, 0.4, 0.35, 0.8, 0.65, 0.9, 0.5, 0.3, 0.6, 0.45],
        }
    )

    df = session.read_pandas(pd_df)
    score = bigframes.ml.metrics.roc_auc_score(df["y_true"], df["y_score"])

    assert score == 0.625


def test_auc_invalid_x_size(session):
    pd_df = pd.DataFrame({"x_arbitrary_name": [0], "y_arbitrary_name": [0]})
    df = session.read_pandas(pd_df)
    with pytest.raises(ValueError):
        bigframes.ml.metrics.auc(df[["x_arbitrary_name"]], df[["y_arbitrary_name"]])


def test_auc_nondecreasing_x(session):
    pd_df = pd.DataFrame({"x": [0, 0, 0.5, 0.5, 1], "y": [0, 0.5, 0.5, 1, 1]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.auc(df[["x"]], df[["y"]]) == 0.75


def test_auc_nonincreasing_x(session):
    pd_df = pd.DataFrame({"x": [0, 0, -0.5, -0.5, -1], "y": [0, 0.5, 0.5, 1, 1]})
    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.auc(df[["x"]], df[["y"]]) == 0.75


def test_auc_nonincreasing_x_negative(session):
    pd_df = pd.DataFrame({"x": [0, 0, -0.5, -0.5, -1], "y": [0, -0.5, -0.5, -1, -1]})
    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.auc(df[["x"]], df[["y"]]) == -0.75


def test_auc_series(session):
    pd_df = pd.DataFrame({"x": [0, 0, 0.5, 0.5, 1], "y": [0, 0.5, 0.5, 1, 1]})

    df = session.read_pandas(pd_df)
    assert bigframes.ml.metrics.auc(df["x"], df["y"]) == 0.75


def test_confusion_matrix(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [2, 0, 2, 2, 0, 1],
            "y_pred_arbitrary_name": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    confusion_matrix = bigframes.ml.metrics.confusion_matrix(
        df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]]
    )
    expected_pd_df = pd.DataFrame(
        {
            0: [2, 0, 1],
            1: [0, 0, 0],
            2: [0, 1, 2],
        }
    ).astype("int64")
    pd.testing.assert_frame_equal(
        confusion_matrix, expected_pd_df, check_index_type=False
    )


def test_confusion_matrix_column_index(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 3, 3, 3, 4, 1],
            "y_pred": [4, 1, 2, 2, 4, 1],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    confusion_matrix = bigframes.ml.metrics.confusion_matrix(
        df[["y_true"]], df[["y_pred"]]
    )
    expected_pd_df = (
        pd.DataFrame(
            {1: [1, 0, 1, 0], 2: [0, 0, 2, 0], 3: [0, 0, 0, 0], 4: [0, 1, 0, 1]}
        )
        .astype("int64")
        .set_index([pd.Index([1, 2, 3, 4])])
    )
    pd.testing.assert_frame_equal(
        confusion_matrix, expected_pd_df, check_index_type=False
    )


def test_confusion_matrix_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 3, 3, 3, 4, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    confusion_matrix = bigframes.ml.metrics.confusion_matrix(
        df[["y_true"]], df[["y_pred"]]
    )
    expected_confusion_matrix = sklearn_metrics.confusion_matrix(
        pd_df[["y_true"]], pd_df[["y_pred"]]
    )
    expected_pd_df = pd.DataFrame(expected_confusion_matrix)
    pd.testing.assert_frame_equal(
        confusion_matrix, expected_pd_df, check_index_type=False
    )


def test_confusion_matrix_str_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": ["cat", "ant", "cat", "cat", "ant", "bird"],
            "y_pred": ["ant", "ant", "cat", "cat", "ant", "cat"],
        }
    ).astype("str")
    df = session.read_pandas(pd_df)
    confusion_matrix = bigframes.ml.metrics.confusion_matrix(
        df[["y_true"]], df[["y_pred"]]
    )
    expected_confusion_matrix = sklearn_metrics.confusion_matrix(
        pd_df[["y_true"]], pd_df[["y_pred"]]
    )
    expected_pd_df = pd.DataFrame(expected_confusion_matrix).set_index(
        [pd.Index(["ant", "bird", "cat"])]
    )
    expected_pd_df.columns = pd.Index(["ant", "bird", "cat"])
    pd.testing.assert_frame_equal(
        confusion_matrix, expected_pd_df, check_index_type=False
    )


def test_confusion_matrix_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    confusion_matrix = bigframes.ml.metrics.confusion_matrix(df["y_true"], df["y_pred"])
    expected_pd_df = pd.DataFrame(
        {
            0: [2, 0, 1],
            1: [0, 0, 0],
            2: [0, 1, 2],
        }
    ).astype("int64")
    pd.testing.assert_frame_equal(
        confusion_matrix, expected_pd_df, check_index_type=False
    )


def test_recall_score(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [2, 0, 2, 2, 0, 1],
            "y_pred_arbitrary_name": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    recall = bigframes.ml.metrics.recall_score(
        df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]], average=None
    )
    expected_values = [1.000000, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_recall = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(recall, expected_recall, check_index_type=False)


def test_recall_score_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    recall = bigframes.ml.metrics.recall_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.recall_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = [0, 1, 2]
    expected_recall = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(recall, expected_recall, check_index_type=False)


def test_recall_score_str_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": ["cat", "ant", "cat", "cat", "ant", "bird"],
            "y_pred": ["ant", "ant", "cat", "cat", "ant", "cat"],
        }
    ).astype("str")
    df = session.read_pandas(pd_df)
    recall = bigframes.ml.metrics.recall_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.recall_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = ["ant", "bird", "cat"]
    expected_recall = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(recall, expected_recall, check_index_type=False)


def test_recall_score_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    recall = bigframes.ml.metrics.recall_score(df["y_true"], df["y_pred"], average=None)
    expected_values = [1.000000, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_recall = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(recall, expected_recall, check_index_type=False)


def test_precision_score(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [2, 0, 2, 2, 0, 1],
            "y_pred_arbitrary_name": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    precision_score = bigframes.ml.metrics.precision_score(
        df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]], average=None
    )
    expected_values = [0.666667, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_precision = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(
        precision_score, expected_precision, check_index_type=False
    )


def test_precision_score_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    precision_score = bigframes.ml.metrics.precision_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.precision_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = [0, 1, 2]
    expected_precision = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(
        precision_score, expected_precision, check_index_type=False
    )


def test_precision_score_str_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": ["cat", "ant", "cat", "cat", "ant", "bird"],
            "y_pred": ["ant", "ant", "cat", "cat", "ant", "cat"],
        }
    ).astype("str")
    df = session.read_pandas(pd_df)
    precision_score = bigframes.ml.metrics.precision_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.precision_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = ["ant", "bird", "cat"]
    expected_precision = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(
        precision_score, expected_precision, check_index_type=False
    )


def test_precision_score_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    precision_score = bigframes.ml.metrics.precision_score(
        df["y_true"], df["y_pred"], average=None
    )
    expected_values = [0.666667, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_precision = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(
        precision_score, expected_precision, check_index_type=False
    )


def test_f1_score(session):
    pd_df = pd.DataFrame(
        {
            "y_true_arbitrary_name": [2, 0, 2, 2, 0, 1],
            "y_pred_arbitrary_name": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    f1_score = bigframes.ml.metrics.f1_score(
        df[["y_true_arbitrary_name"]], df[["y_pred_arbitrary_name"]], average=None
    )
    expected_values = [0.8, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_f1 = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(f1_score, expected_f1, check_index_type=False)


def test_f1_score_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    f1_score = bigframes.ml.metrics.f1_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.f1_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = [0, 1, 2]
    expected_f1 = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(f1_score, expected_f1, check_index_type=False)


def test_f1_score_str_matches_sklearn(session):
    pd_df = pd.DataFrame(
        {
            "y_true": ["cat", "ant", "cat", "cat", "ant", "bird"],
            "y_pred": ["ant", "ant", "cat", "cat", "ant", "cat"],
        }
    ).astype("str")
    df = session.read_pandas(pd_df)
    f1_score = bigframes.ml.metrics.f1_score(
        df[["y_true"]], df[["y_pred"]], average=None
    )
    expected_values = sklearn_metrics.f1_score(
        pd_df[["y_true"]], pd_df[["y_pred"]], average=None
    )
    expected_index = ["ant", "bird", "cat"]
    expected_f1 = pd.Series(expected_values, index=expected_index)
    pd.testing.assert_series_equal(f1_score, expected_f1, check_index_type=False)


def test_f1_score_series(session):
    pd_df = pd.DataFrame(
        {
            "y_true": [2, 0, 2, 2, 0, 1],
            "y_pred": [0, 0, 2, 2, 0, 2],
        }
    ).astype("Int64")
    df = session.read_pandas(pd_df)
    f1_score = bigframes.ml.metrics.f1_score(df["y_true"], df["y_pred"], average=None)
    expected_values = [0.8, 0.000000, 0.666667]
    expected_index = [0, 1, 2]
    expected_f1 = pd.Series(expected_values, index=expected_index)

    pd.testing.assert_series_equal(f1_score, expected_f1, check_index_type=False)
