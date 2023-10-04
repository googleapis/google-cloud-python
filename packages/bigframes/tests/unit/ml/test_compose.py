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

import sklearn.compose as sklearn_compose  # type: ignore
import sklearn.preprocessing as sklearn_preprocessing  # type: ignore

from bigframes.ml import compose, preprocessing


def test_columntransformer_init_expectedtransforms():
    onehot_transformer = preprocessing.OneHotEncoder()
    standard_scaler_transformer = preprocessing.StandardScaler()
    max_abs_scaler_transformer = preprocessing.MaxAbsScaler()
    min_max_scaler_transformer = preprocessing.MinMaxScaler()
    k_bins_discretizer_transformer = preprocessing.KBinsDiscretizer(strategy="uniform")
    label_transformer = preprocessing.LabelEncoder()
    column_transformer = compose.ColumnTransformer(
        [
            ("onehot", onehot_transformer, "species"),
            (
                "standard_scale",
                standard_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                max_abs_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                min_max_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                k_bins_discretizer_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("label", label_transformer, "species"),
        ]
    )

    assert column_transformer.transformers_ == [
        ("onehot", onehot_transformer, "species"),
        ("standard_scale", standard_scaler_transformer, "culmen_length_mm"),
        ("standard_scale", standard_scaler_transformer, "flipper_length_mm"),
        ("max_abs_scale", max_abs_scaler_transformer, "culmen_length_mm"),
        ("max_abs_scale", max_abs_scaler_transformer, "flipper_length_mm"),
        ("min_max_scale", min_max_scaler_transformer, "culmen_length_mm"),
        ("min_max_scale", min_max_scaler_transformer, "flipper_length_mm"),
        ("k_bins_discretizer", k_bins_discretizer_transformer, "culmen_length_mm"),
        ("k_bins_discretizer", k_bins_discretizer_transformer, "flipper_length_mm"),
        ("label", label_transformer, "species"),
    ]


def test_columntransformer_repr():
    column_transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    assert (
        column_transformer.__repr__()
        == """ColumnTransformer(transformers=[('onehot', OneHotEncoder(), 'species'),
                                ('standard_scale', StandardScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('max_abs_scale', MaxAbsScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('min_max_scale', MinMaxScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('k_bins_discretizer',
                                 KBinsDiscretizer(strategy='uniform'),
                                 ['culmen_length_mm', 'flipper_length_mm'])])"""
    )


def test_columntransformer_repr_matches_sklearn():
    bf_column_transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )
    sk_column_transformer = sklearn_compose.ColumnTransformer(
        [
            (
                "onehot",
                sklearn_preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                sklearn_preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                sklearn_preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                sklearn_preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                sklearn_preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    assert bf_column_transformer.__repr__() == sk_column_transformer.__repr__()
