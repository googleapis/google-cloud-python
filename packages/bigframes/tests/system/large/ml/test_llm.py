# Copyright 2024 Google LLC
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


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ),
)
@pytest.mark.flaky(
    retries=2
)  # usually create model shouldn't be flaky, but this one due to the limited quota of gemini-2.0-flash-exp.
def test_create_load_gemini_text_generator_model(
    dataset_id, model_name, session, bq_connection
):
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    assert gemini_text_generator_model is not None
    assert gemini_text_generator_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = gemini_text_generator_model.to_gbq(
        f"{dataset_id}.temp_text_model", replace=True
    )
    assert f"{dataset_id}.temp_text_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.connection_name == bq_connection
    assert reloaded_model.model_name == model_name


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ),
)
# @pytest.mark.flaky(retries=2)
def test_gemini_text_generator_predict_default_params_success(
    llm_text_df, model_name, session, bq_connection
):
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = gemini_text_generator_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_predict_with_params_success(
    llm_text_df, model_name, session, bq_connection
):
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = gemini_text_generator_model.predict(
        llm_text_df, temperature=0.5, max_output_tokens=100, top_k=20, top_p=0.5
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_multi_cols_predict_success(
    llm_text_df: bpd.DataFrame, model_name, session, bq_connection
):
    df = llm_text_df.assign(additional_col=1)
    gemini_text_generator_model = llm.GeminiTextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    pd_df = gemini_text_generator_model.predict(df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        pd_df,
        columns=utils.ML_GENERATE_TEXT_OUTPUT + ["additional_col"],
        index=3,
        col_exact=False,
    )


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ),
)
@pytest.mark.flaky(retries=2)
def test_gemini_text_generator_predict_output_schema_success(
    llm_text_df: bpd.DataFrame, model_name, session, bq_connection
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
    df = gemini_text_generator_model.predict(llm_text_df, output_schema=output_schema)
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
        columns=list(output_schema.keys()) + ["prompt", "full_response", "status"],
        index=3,
        col_exact=False,
    )


@pytest.mark.flaky(retries=2)
@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ),
)
def test_llm_gemini_score(llm_fine_tune_df_default_index, model_name):
    model = llm.GeminiTextGenerator(model_name=model_name)

    # Check score to ensure the model was fitted
    score_result = model.score(
        X=llm_fine_tune_df_default_index[["prompt"]],
        y=llm_fine_tune_df_default_index[["label"]],
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result,
        columns=[
            "bleu4_score",
            "rouge-l_precision",
            "rouge-l_recall",
            "rouge-l_f1_score",
            "evaluation_status",
        ],
        index=1,
    )


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ),
)
def test_llm_gemini_pro_score_params(llm_fine_tune_df_default_index, model_name):
    model = llm.GeminiTextGenerator(model_name=model_name)

    # Check score to ensure the model was fitted
    score_result = model.score(
        X=llm_fine_tune_df_default_index["prompt"],
        y=llm_fine_tune_df_default_index["label"],
        task_type="classification",
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        score_result,
        columns=[
            "precision",
            "recall",
            "f1_score",
            "label",
            "evaluation_status",
        ],
    )
