# Copyright 2025 Google LLC
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

import bigframes.bigquery as bbq


def test_rand(scalars_df_index):
    df = scalars_df_index

    # Apply rand
    df = df.assign(random=bbq.rand())
    result = df["random"]

    # Eagerly evaluate
    result_pd = result.to_pandas()

    # Check length
    assert len(result_pd) == len(df)

    # Check values in [0, 1)
    assert (result_pd >= 0).all()
    assert (result_pd < 1).all()

    # Check not all values are equal (unlikely collision for random)
    if len(result_pd) > 1:
        assert result_pd.nunique() > 1
