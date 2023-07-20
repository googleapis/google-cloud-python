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

"""Metrics functions for evaluating models. This module is styled after
Scikit-Learn's metrics module: https://scikit-learn.org/stable/modules/metrics.html"""

import inspect
import typing
from typing import Tuple

import numpy as np
import pandas as pd
import sklearn.metrics as sklearn_metrics  # type: ignore

import bigframes.core.blocks as blocks
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.metrics._classification as vendored_mertics_classification
import third_party.bigframes_vendored.sklearn.metrics._ranking as vendored_mertics_ranking
import third_party.bigframes_vendored.sklearn.metrics._regression as vendored_metrics_regression


def r2_score(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
    force_finite=True,
) -> float:
    # TODO(bmil): support multioutput
    if len(y_true.columns) > 1 or len(y_pred.columns) > 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    y_true_series = typing.cast(
        bpd.Series, y_true[typing.cast(str, y_true.columns.tolist()[0])]
    )
    y_pred_series = typing.cast(
        bpd.Series, y_pred[typing.cast(str, y_pred.columns.tolist()[0])]
    )

    # total sum of squares
    # (dataframe, scalar) binops
    # TODO(bmil): remove multiply by self when bigframes supports pow()
    # TODO(tbergeron): These stats are eagerly evaluated. Move to lazy representation once scalar subqueries supported.
    delta_from_mean = y_true_series - y_true_series.mean()
    ss_total = (delta_from_mean * delta_from_mean).sum()

    # residual sum of squares
    # (scalar, scalar) binops
    # TODO(bmil): remove multiply by self when bigframes supports pow()
    delta_from_pred = y_true_series - y_pred_series
    ss_res = (delta_from_pred * delta_from_pred).sum()

    if force_finite and ss_total == 0:
        return 0.0 if ss_res > 0 else 1.0

    return 1 - (ss_res / ss_total)


r2_score.__doc__ = inspect.getdoc(vendored_metrics_regression.r2_score)


def accuracy_score(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
    normalize=True,
) -> float:
    # TODO(ashleyxu): support sample_weight as the parameter
    if len(y_true.columns) != 1 or len(y_pred.columns) != 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    y_true_series = typing.cast(
        bpd.Series, y_true[typing.cast(str, y_true.columns.tolist()[0])]
    )
    y_pred_series = typing.cast(
        bpd.Series, y_pred[typing.cast(str, y_pred.columns.tolist()[0])]
    )

    # Compute accuracy for each possible representation
    # TODO(ashleyxu): add multilabel classification support where y_type
    # starts with "multilabel"
    score = (y_true_series == y_pred_series).astype(pd.Int64Dtype())

    if normalize:
        return score.mean()
    else:
        return score.sum()


accuracy_score.__doc__ = inspect.getdoc(vendored_mertics_classification.accuracy_score)


def roc_curve(
    y_true: bpd.DataFrame,
    y_score: bpd.DataFrame,
    drop_intermediate: bool = True,
) -> Tuple[bpd.Series, bpd.Series, bpd.Series]:
    # TODO(bmil): Add multi-class support
    # TODO(bmil): Add multi-label support
    if len(y_true.columns) > 1 or len(y_score.columns) > 1:
        raise NotImplementedError("Only binary classification is supported")

    # TODO(bmil): Implement drop_intermediate
    if drop_intermediate:
        raise NotImplementedError("drop_intermediate is not yet implemented")

    # TODO(bmil): remove this once bigframes supports the necessary operations
    session = y_true._block.expr._session
    pd_y_true = y_true.to_pandas()
    pd_y_score = y_score.to_pandas()

    # We operate on rows, so, remove the index if there is one
    # TODO(bmil): check that the indexes are equivalent before removing
    pd_y_true = pd_y_true.reset_index(drop=True)
    pd_y_score = pd_y_score.reset_index(drop=True)

    pd_df = pd.DataFrame(
        {
            "y_true": pd_y_true[pd_y_true.columns[0]],
            "y_score": pd_y_score[pd_y_score.columns[0]],
        }
    )

    total_positives = pd_df.y_true.sum()
    total_negatives = len(pd_df) - total_positives

    pd_df = pd_df.sort_values(by="y_score", ascending=False)
    pd_df["cum_tp"] = pd_df.y_true.cumsum()
    pd_df["cum_fp"] = (~pd_df.y_true.astype(bool)).cumsum()

    # produce just one data point per y_score
    pd_df = pd_df.groupby("y_score", as_index=False).last()
    pd_df = pd_df.sort_values(by="y_score", ascending=False)

    pd_df["tpr"] = pd_df.cum_tp / total_positives
    pd_df["fpr"] = pd_df.cum_fp / total_negatives
    pd_df["thresholds"] = pd_df.y_score

    # sklearn includes an extra datapoint for the origin with threshold np.inf
    pd_origin = pd.DataFrame({"tpr": [0.0], "fpr": [0.0], "thresholds": np.inf})
    pd_df = pd.concat([pd_origin, pd_df])

    df = session.read_pandas(pd_df)
    return df.fpr, df.tpr, df.thresholds


roc_curve.__doc__ = inspect.getdoc(vendored_mertics_ranking.roc_curve)


def roc_auc_score(y_true: bpd.DataFrame, y_score: bpd.DataFrame) -> float:
    # TODO(bmil): Add multi-class support
    # TODO(bmil): Add multi-label support
    if len(y_true.columns) > 1 or len(y_score.columns) > 1:
        raise NotImplementedError("Only binary classification is supported")

    fpr, tpr, _ = roc_curve(y_true, y_score, drop_intermediate=False)

    # TODO(bmil): remove this once bigframes supports the necessary operations
    pd_fpr = fpr.compute()
    pd_tpr = tpr.compute()

    # Use the trapezoid rule to compute the area under the ROC curve
    width_diff = pd_fpr.diff().iloc[1:].reset_index(drop=True)
    height_avg = (pd_tpr.iloc[:-1] + pd_tpr.iloc[1:].reset_index(drop=True)) / 2
    return (width_diff * height_avg).sum()


roc_auc_score.__doc__ = inspect.getdoc(vendored_mertics_ranking.roc_auc_score)


def auc(
    x: bpd.DataFrame,
    y: bpd.DataFrame,
) -> float:
    if len(x.columns) != 1 or len(y.columns) != 1:
        raise ValueError("Only 1-D data structure is supported")

    # TODO(b/286410053) Support ML exceptions and error handling.
    auc = sklearn_metrics.auc(x.to_pandas(), y.to_pandas())
    return auc


auc.__doc__ = inspect.getdoc(vendored_mertics_ranking.auc)


def confusion_matrix(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
) -> pd.DataFrame:
    # TODO(ashleyxu): support labels and sample_weight parameters
    # TODO(ashleyxu): support bpd.Series as input type
    if len(y_true.columns) != 1 or len(y_pred.columns) != 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    y_true_column = typing.cast(blocks.Label, y_true.columns[0])
    y_pred_series = typing.cast(
        bpd.Series,
        y_pred[typing.cast(blocks.Label, y_pred.columns.tolist()[0])],
    )
    confusion_df = y_true.assign(y_pred=y_pred_series)
    confusion_df = confusion_df.assign(dummy=0)
    groupby_count = (
        confusion_df.groupby(by=[y_true_column, "y_pred"], as_index=False)
        .count()
        .to_pandas()
    )

    unique_values = sorted(set(groupby_count.y_true).union(set(groupby_count.y_pred)))

    confusion_matrix = pd.DataFrame(
        0, index=pd.Index(unique_values), columns=pd.Index(unique_values), dtype=int
    )

    # Loop through the result by rows and columns
    for _, row in groupby_count.iterrows():
        y_true = row["y_true"]
        y_pred = row["y_pred"]
        count = row["dummy"]
        confusion_matrix[y_pred][y_true] = count

    return confusion_matrix


confusion_matrix.__doc__ = inspect.getdoc(
    vendored_mertics_classification.confusion_matrix
)


def recall_score(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    # TODO(ashleyxu): support bpd.Series as input type
    if len(y_true.columns) != 1 or len(y_pred.columns) != 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    if average is not None:
        raise NotImplementedError("Only average=None is supported")

    y_true_series = typing.cast(
        bpd.Series,
        y_true[typing.cast(blocks.Label, y_true.columns.tolist()[0])],
    )
    y_pred_series = typing.cast(
        bpd.Series,
        y_pred[typing.cast(blocks.Label, y_pred.columns.tolist()[0])],
    )

    is_accurate = y_true_series == y_pred_series
    unique_labels = (
        bpd.concat([y_true_series, y_pred_series], join="outer")
        .drop_duplicates()
        .sort_values()
    )
    index = unique_labels.to_list()

    recall = (
        is_accurate.groupby(y_true_series).sum()
        / is_accurate.groupby(y_true_series).count()
    ).compute()

    recall_score = pd.Series(0, index=index)
    for i in recall_score.index:
        recall_score.loc[i] = recall.loc[i]

    return recall_score


recall_score.__doc__ = inspect.getdoc(vendored_mertics_classification.recall_score)


def precision_score(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    # TODO(ashleyxu): support bpd.Series as input type
    if len(y_true.columns) != 1 or len(y_pred.columns) != 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    if average is not None:
        raise NotImplementedError("Only average=None is supported")

    y_true_series = typing.cast(
        bpd.Series,
        y_true[typing.cast(blocks.Label, y_true.columns.tolist()[0])],
    )
    y_pred_series = typing.cast(
        bpd.Series,
        y_pred[typing.cast(blocks.Label, y_pred.columns.tolist()[0])],
    )

    is_accurate = y_true_series == y_pred_series
    unique_labels = (
        bpd.concat([y_true_series, y_pred_series], join="outer")
        .drop_duplicates()
        .sort_values()
    )
    index = unique_labels.to_list()

    precision = (
        is_accurate.groupby(y_pred_series).sum()
        / is_accurate.groupby(y_pred_series).count()
    ).compute()

    precision_score = pd.Series(0, index=index)
    for i in precision.index:
        precision_score.loc[i] = precision.loc[i]

    return precision_score


precision_score.__doc__ = inspect.getdoc(
    vendored_mertics_classification.precision_score
)


def f1_score(
    y_true: bpd.DataFrame,
    y_pred: bpd.DataFrame,
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    # TODO(ashleyxu): support bpd.Series as input type
    if len(y_true.columns) != 1 or len(y_pred.columns) != 1:
        raise NotImplementedError(
            "Only one labels column, one predictions column is supported"
        )

    if average is not None:
        raise NotImplementedError("Only average=None is supported")

    recall = recall_score(y_true, y_pred, average=None)
    precision = precision_score(y_true, y_pred, average=None)

    f1_score = pd.Series(0, index=recall.index)
    for index in recall.index:
        if precision[index] + recall[index] != 0:
            f1_score[index] = (
                2
                * (precision[index] * recall[index])
                / (precision[index] + recall[index])
            )
        else:
            f1_score[index] = 0

    return f1_score


f1_score.__doc__ = inspect.getdoc(vendored_mertics_classification.f1_score)
