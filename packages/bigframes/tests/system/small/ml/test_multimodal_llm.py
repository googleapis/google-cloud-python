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

import bigframes
from bigframes.ml import llm
import bigframes.pandas as bpd
from tests.system import utils


@pytest.mark.flaky(retries=2)
def test_multimodal_embedding_generator_predict_default_params_success(
    images_mm_df, test_session, bq_connection
):
    bigframes.options.experiments.blob = True

    text_embedding_model = llm.MultimodalEmbeddingGenerator(
        connection_name=bq_connection, session=test_session
    )
    df = text_embedding_model.predict(images_mm_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df,
        columns=utils.ML_MULTIMODAL_GENERATE_EMBEDDING_OUTPUT,
        index=2,
        col_exact=False,
    )
    assert len(df["ml_generate_embedding_result"][0]) == 1408


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_multimodal_input(
    images_mm_df: bpd.DataFrame, model_name, test_session, bq_connection
):
    bigframes.options.experiments.blob = True

    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=test_session
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
