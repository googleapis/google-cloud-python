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
Scikit-Learn's metrics module: https://scikit-learn.org/stable/modules/metrics.html."""

import inspect
import typing
from typing import Tuple, Union

import numpy as np
import pandas as pd
import sklearn.metrics as sklearn_metrics  # type: ignore

import bigframes.constants as constants
from bigframes.ml import utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.metrics._classification as vendored_mertics_classification
import third_party.bigframes_vendored.sklearn.metrics._ranking as vendored_mertics_ranking
import third_party.bigframes_vendored.sklearn.metrics._regression as vendored_metrics_regression


def r2_score(
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
    force_finite=True,
) -> float:
    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

    # total sum of squares
    # (dataframe, scalar) binops
    # TODO(tbergeron): These stats are eagerly evaluated. Move to lazy representation once scalar subqueries supported.
    delta_from_mean = y_true_series - y_true_series.mean()
    ss_total = (delta_from_mean * delta_from_mean).sum()

    # residual sum of squares
    # (scalar, scalar) binops
    delta_from_pred = y_true_series - y_pred_series
    ss_res = (delta_from_pred * delta_from_pred).sum()

    if force_finite and ss_total == 0:
        return 0.0 if ss_res > 0 else 1.0

    return 1 - (ss_res / ss_total)


r2_score.__doc__ = inspect.getdoc(vendored_metrics_regression.r2_score)


def accuracy_score(
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
    normalize=True,
) -> float:
    # TODO(ashleyxu): support sample_weight as the parameter
    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

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
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_score: Union[bpd.DataFrame, bpd.Series],
    drop_intermediate: bool = True,
) -> Tuple[bpd.Series, bpd.Series, bpd.Series]:
    # TODO(bmil): Add multi-class support
    # TODO(bmil): Add multi-label support

    # TODO(bmil): Implement drop_intermediate
    if drop_intermediate:
        raise NotImplementedError(
            f"drop_intermediate is not yet implemented. {constants.FEEDBACK_LINK}"
        )

    y_true_series, y_score_series = utils.convert_to_series(y_true, y_score)

    session = y_true_series._block.expr.session

    # We operate on rows, so, remove the index if there is one
    # TODO(bmil): check that the indexes are equivalent before removing

    y_true_series = typing.cast(bpd.Series, y_true_series.reset_index(drop=True))
    y_score_series = typing.cast(bpd.Series, y_score_series.reset_index(drop=True))

    df = bpd.DataFrame(
        {
            "y_true": y_true_series,
            "y_score": y_score_series,
        }
    )

    total_positives = y_true_series.sum()
    total_negatives = y_true_series.count() - total_positives

    df = df.sort_values(by="y_score", ascending=False)
    df["cum_tp"] = df["y_true"].cumsum()
    # have to astype("Int64") as not supported boolean cumsum yet.
    df["cum_fp"] = (
        (~typing.cast(bpd.Series, df["y_true"].astype("boolean")))
        .astype("Int64")
        .cumsum()
    )

    # produce just one data point per y_score
    df = df.drop_duplicates(subset="y_score", keep="last")
    df = df.sort_values(by="y_score", ascending=False)

    df["tpr"] = typing.cast(bpd.Series, df["cum_tp"]) / total_positives
    df["fpr"] = typing.cast(bpd.Series, df["cum_fp"]) / total_negatives
    df["thresholds"] = typing.cast(bpd.Series, df["y_score"].astype("Float64"))

    # sklearn includes an extra datapoint for the origin with threshold np.inf
    # having problems with concating inline
    df_origin = session.read_pandas(
        pd.DataFrame({"tpr": [0.0], "fpr": [0.0], "thresholds": np.inf})
    )
    df = typing.cast(bpd.DataFrame, bpd.concat([df_origin, df], ignore_index=True))
    df = df.reset_index(drop=True)

    return (
        typing.cast(bpd.Series, df["fpr"]),
        typing.cast(bpd.Series, df["tpr"]),
        typing.cast(bpd.Series, df["thresholds"]),
    )


roc_curve.__doc__ = inspect.getdoc(vendored_mertics_ranking.roc_curve)


def roc_auc_score(
    y_true: Union[bpd.DataFrame, bpd.Series], y_score: Union[bpd.DataFrame, bpd.Series]
) -> float:
    # TODO(bmil): Add multi-class support
    # TODO(bmil): Add multi-label support
    y_true_series, y_score_series = utils.convert_to_series(y_true, y_score)

    fpr, tpr, _ = roc_curve(y_true_series, y_score_series, drop_intermediate=False)

    # TODO(bmil): remove this once bigframes supports the necessary operations
    pd_fpr = fpr.to_pandas()
    pd_tpr = tpr.to_pandas()

    # Use the trapezoid rule to compute the area under the ROC curve
    width_diff = pd_fpr.diff().iloc[1:].reset_index(drop=True)
    height_avg = (pd_tpr.iloc[:-1] + pd_tpr.iloc[1:].reset_index(drop=True)) / 2
    return (width_diff * height_avg).sum()


roc_auc_score.__doc__ = inspect.getdoc(vendored_mertics_ranking.roc_auc_score)


def auc(
    x: Union[bpd.DataFrame, bpd.Series],
    y: Union[bpd.DataFrame, bpd.Series],
) -> float:
    x_series, y_series = utils.convert_to_series(x, y)

    # TODO(b/286410053) Support ML exceptions and error handling.
    auc = sklearn_metrics.auc(x_series.to_pandas(), y_series.to_pandas())
    return auc


auc.__doc__ = inspect.getdoc(vendored_mertics_ranking.auc)


def confusion_matrix(
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
) -> pd.DataFrame:
    # TODO(ashleyxu): support labels and sample_weight parameters
    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

    y_true_series = y_true_series.rename("y_true")
    confusion_df = y_true_series.to_frame().assign(y_pred=y_pred_series)
    confusion_df = confusion_df.assign(dummy=0)
    groupby_count = (
        confusion_df.groupby(by=["y_true", "y_pred"], as_index=False)
        .count()
        .to_pandas()
    )

    unique_values = sorted(
        set(groupby_count["y_true"]).union(set(groupby_count["y_pred"]))
    )

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
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    if average is not None:
        raise NotImplementedError(
            f"Only average=None is supported. {constants.FEEDBACK_LINK}"
        )

    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

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
    ).to_pandas()

    recall_score = pd.Series(0, index=index)
    for i in recall_score.index:
        recall_score.loc[i] = recall.loc[i]

    return recall_score


recall_score.__doc__ = inspect.getdoc(vendored_mertics_classification.recall_score)


def precision_score(
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    if average is not None:
        raise NotImplementedError(
            f"Only average=None is supported. {constants.FEEDBACK_LINK}"
        )

    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

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
    ).to_pandas()

    precision_score = pd.Series(0, index=index)
    for i in precision.index:
        precision_score.loc[i] = precision.loc[i]

    return precision_score


precision_score.__doc__ = inspect.getdoc(
    vendored_mertics_classification.precision_score
)


def f1_score(
    y_true: Union[bpd.DataFrame, bpd.Series],
    y_pred: Union[bpd.DataFrame, bpd.Series],
    average: str = "binary",
) -> pd.Series:
    # TODO(ashleyxu): support more average type, default to "binary"
    y_true_series, y_pred_series = utils.convert_to_series(y_true, y_pred)

    if average is not None:
        raise NotImplementedError(
            f"Only average=None is supported. {constants.FEEDBACK_LINK}"
        )

    recall = recall_score(y_true_series, y_pred_series, average=None)
    precision = precision_score(y_true_series, y_pred_series, average=None)

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
