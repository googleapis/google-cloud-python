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

import pandas as pd

import bigframes.ml.preprocessing


def test_standard_scaler_normalizes(penguins_df_default_index, new_penguins_df):
    # TODO(bmil): add a second test that compares output to sklearn.preprocessing.StandardScaler
    scaler = bigframes.ml.preprocessing.StandardScaler()
    scaler.fit(
        penguins_df_default_index[
            "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"
        ]
    )

    result = scaler.transform(
        penguins_df_default_index[
            "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"
        ]
    ).to_pandas()

    # If standard-scaled correctly, mean should be 0.0 and standard deviation 1.0
    for column in result.columns:
        assert math.isclose(result[column].mean(), 0.0, abs_tol=1e-3)
        assert math.isclose(result[column].std(), 1.0, abs_tol=1e-3)

    result = scaler.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "scaled_culmen_depth_mm": [0.8349, 0.02473, 0.4805],
            "scaled_culmen_length_mm": [-0.8099, -0.9931, -1.103],
            "scaled_flipper_length_mm": [-0.3495, -1.4163, -0.9185],
        },
        dtype="Float64",
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected, rtol=1e-3)


def test_one_hot_encoder_encodes(penguins_df_default_index, new_penguins_df):
    encoder = bigframes.ml.preprocessing.OneHotEncoder()
    encoder.fit(penguins_df_default_index["species", "sex"])

    result = encoder.transform(new_penguins_df).to_pandas()

    # TODO: bug? feature columns seem to be in nondeterministic random order
    # workaround: sort columns by name. Can't repro it in pantheon, so could
    # be a bigframes issue...
    result = result.reindex(sorted(result.columns), axis=1)

    expected = pd.DataFrame(
        {
            "onehotencoded_sex": [
                [{"index": 2, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
            ],
            "onehotencoded_species": [
                [{"index": 1, "value": 1.0}],
                [{"index": 1, "value": 1.0}],
                [{"index": 2, "value": 1.0}],
            ],
        },
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )

    pd.testing.assert_frame_equal(result, expected)
