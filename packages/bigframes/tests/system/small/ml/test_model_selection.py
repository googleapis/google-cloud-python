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

import pandas as pd
import pytest

from bigframes.ml import model_selection
import bigframes.pandas as bpd


def test_train_test_split_default_correct_shape(penguins_df_default_index):
    X = penguins_df_default_index[
        [
            "species",
            "island",
            "culmen_length_mm",
        ]
    ]
    y = penguins_df_default_index[["body_mass_g"]]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)

    # even though the default seed is random, it should always result in this shape
    assert X_train.shape == (258, 3)
    assert X_test.shape == (86, 3)
    assert y_train.shape == (258, 1)
    assert y_test.shape == (86, 1)


def test_train_test_split_series_default_correct_shape(penguins_df_default_index):
    X = penguins_df_default_index[["species"]]
    y = penguins_df_default_index["body_mass_g"]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y)
    assert isinstance(X_train, bpd.DataFrame)
    assert isinstance(X_test, bpd.DataFrame)
    assert isinstance(y_train, bpd.Series)
    assert isinstance(y_test, bpd.Series)

    # even though the default seed is random, it should always result in this shape
    assert X_train.shape == (258, 1)
    assert X_test.shape == (86, 1)
    assert y_train.shape == (258,)
    assert y_test.shape == (86,)


def test_train_test_double_split_correct_shape(penguins_df_default_index):
    X = penguins_df_default_index[
        [
            "species",
            "island",
            "culmen_length_mm",
        ]
    ]
    y = penguins_df_default_index[["body_mass_g"]]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.2, train_size=0.4
    )

    # should have 20% in test, 40% in train, 40% dropped
    assert X_train.shape == (138, 3)
    assert X_test.shape == (69, 3)
    assert y_train.shape == (138, 1)
    assert y_test.shape == (69, 1)


def test_train_test_three_dataframes_correct_shape(penguins_df_default_index):
    A = penguins_df_default_index[
        [
            "species",
            "culmen_length_mm",
        ]
    ]
    B = penguins_df_default_index[
        [
            "island",
        ]
    ]
    C = penguins_df_default_index[["culmen_depth_mm", "body_mass_g"]]
    (
        A_train,
        A_test,
        B_train,
        B_test,
        C_train,
        C_test,
    ) = model_selection.train_test_split(A, B, C)

    assert A_train.shape == (258, 2)
    assert A_test.shape == (86, 2)
    assert B_train.shape == (258, 1)
    assert B_test.shape == (86, 1)
    assert C_train.shape == (258, 2)
    assert C_test.shape == (86, 2)


def test_train_test_split_seeded_correct_rows(
    session, penguins_pandas_df_default_index
):
    # Note that we're using `penguins_pandas_df_default_index` as this test depends
    # on a stable row order being present end to end
    # filter down to the chunkiest penguins, to keep our test code a reasonable size
    all_data = penguins_pandas_df_default_index[
        penguins_pandas_df_default_index.body_mass_g > 5500
    ]

    # Note that bigframes loses the index if it doesn't have a name
    all_data.index.name = "rowindex"

    df = session.read_pandas(all_data)

    X = df[
        [
            "species",
            "island",
            "culmen_length_mm",
        ]
    ]
    y = df[["body_mass_g"]]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, random_state=42
    )

    X_train = X_train.to_pandas().sort_index()
    X_test = X_test.to_pandas().sort_index()
    y_train = y_train.to_pandas().sort_index()
    y_test = y_test.to_pandas().sort_index()

    train_index = pd.Index(
        [
            144,
            146,
            168,
            183,
            186,
            217,
            221,
            225,
            237,
            240,
            244,
            245,
            257,
            260,
            262,
            263,
            264,
            266,
            267,
            268,
            290,
        ],
        dtype="Int64",
        name="rowindex",
    )
    test_index = pd.Index(
        [148, 161, 226, 269, 278, 289, 291], dtype="Int64", name="rowindex"
    )

    all_data.index.name = "_"
    pd.testing.assert_frame_equal(
        X_train,
        all_data[
            [
                "species",
                "island",
                "culmen_length_mm",
            ]
        ].loc[train_index],
    )
    pd.testing.assert_frame_equal(
        X_test,
        all_data[
            [
                "species",
                "island",
                "culmen_length_mm",
            ]
        ].loc[test_index],
    )
    pd.testing.assert_frame_equal(
        y_train,
        all_data[
            [
                "body_mass_g",
            ]
        ].loc[train_index],
    )
    pd.testing.assert_frame_equal(
        y_test,
        all_data[
            [
                "body_mass_g",
            ]
        ].loc[test_index],
    )


@pytest.mark.parametrize(
    ("train_size", "test_size"),
    [
        (0.0, 0.5),
        (-0.5, 0.7),
        (0.5, 1.2),
        (0.6, 0.6),
    ],
)
def test_train_test_split_value_error(penguins_df_default_index, train_size, test_size):
    X = penguins_df_default_index[
        [
            "species",
            "island",
            "culmen_length_mm",
        ]
    ]
    y = penguins_df_default_index[["body_mass_g"]]
    with pytest.raises(ValueError):
        model_selection.train_test_split(
            X, y, train_size=train_size, test_size=test_size
        )
