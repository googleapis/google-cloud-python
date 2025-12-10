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

import pytest

from bigframes.ml import llm
import bigframes.pandas as bpd
from bigframes.testing import utils


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_multimodal_input(
    images_mm_df: bpd.DataFrame, model_name, session, bq_connection
):
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    pd_df = gemini_text_generator_model.predict(
        images_mm_df, prompt=["Describe", images_mm_df["blob_col"]]
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        pd_df,
        columns=utils.ML_GENERATE_TEXT_OUTPUT + ["blob_col"],
        index=2,
        col_exact=False,
    )
