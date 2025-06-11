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

import pandas as pd
import pyarrow as pa
import pytest

from bigframes.ml import llm
import bigframes.pandas as bpd
from bigframes.testing import utils


@pytest.mark.flaky(retries=2)
def test_multimodal_embedding_generator_predict_default_params_success(
    images_mm_df, session, bq_connection
):
    text_embedding_model = llm.MultimodalEmbeddingGenerator(
        connection_name=bq_connection, session=session
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


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_multimodal_structured_output(
    images_mm_df: bpd.DataFrame, model_name, session, bq_connection
):
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    output_schema = {
        "bool_output": "bool",
        "int_output": "int64",
        "float_output": "float64",
        "str_output": "string",
        "array_output": "array<int64>",
        "struct_output": "struct<number int64>",
    }
    df = gemini_text_generator_model.predict(
        images_mm_df,
        prompt=["Describe", images_mm_df["blob_col"]],
        output_schema=output_schema,
    )
    assert df["bool_output"].dtype == pd.BooleanDtype()
    assert df["int_output"].dtype == pd.Int64Dtype()
    assert df["float_output"].dtype == pd.Float64Dtype()
    assert df["str_output"].dtype == pd.StringDtype(storage="pyarrow")
    assert df["array_output"].dtype == pd.ArrowDtype(pa.list_(pa.int64()))
    assert df["struct_output"].dtype == pd.ArrowDtype(
        pa.struct([("number", pa.int64())])
    )

    pd_df = df.to_pandas()
    utils.check_pandas_df_schema_and_index(
        pd_df,
        columns=list(output_schema.keys())
        + ["blob_col", "prompt", "full_response", "status"],
        index=2,
        col_exact=False,
    )
