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

from bigframes.ml import remote


def test_remote_linear_vertex_model_predict(
    linear_remote_vertex_model: remote.VertexAIModel, new_penguins_df
):
    predictions = linear_remote_vertex_model.predict(new_penguins_df).to_pandas()
    expected = pd.DataFrame(
        {"predicted_body_mass_g": [[3739.54], [3675.79], [3619.54]]},
        index=pd.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        predictions[["predicted_body_mass_g"]].sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )
