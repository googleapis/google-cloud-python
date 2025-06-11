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

from bigframes.ml import llm
from bigframes.testing import utils


@pytest.fixture(scope="session")
def llm_remote_text_pandas_df():
    """Additional data matching the penguins dataset, with a new index"""
    return pd.DataFrame(
        {
            "prompt": [
                "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: i feel beautifully emotional knowing that these women of whom i knew just a handful were holding me and my baba on our journey",
                "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: i was feeling a little vain when i did this one",
                "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: a father of children killed in an accident",
            ],
        }
    )


@pytest.fixture(scope="session")
def llm_remote_text_df(session, llm_remote_text_pandas_df):
    return session.read_pandas(llm_remote_text_pandas_df)


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ),
)
def test_llm_gemini_configure_fit(
    session, model_name, llm_fine_tune_df_default_index, llm_remote_text_df
):
    model = llm.GeminiTextGenerator(
        session=session, model_name=model_name, max_iterations=1
    )

    X_train = llm_fine_tune_df_default_index[["prompt"]]
    y_train = llm_fine_tune_df_default_index[["label"]]
    model.fit(X_train, y_train)

    assert model is not None

    df = model.predict(
        llm_remote_text_df["prompt"],
        temperature=0.5,
        max_output_tokens=100,
        top_k=20,
        top_p=0.5,
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df,
        columns=[
            "ml_generate_text_llm_result",
            "ml_generate_text_rai_result",
            "ml_generate_text_status",
            "prompt",
        ],
        index=3,
    )


@pytest.mark.flaky(retries=2)
def test_llm_gemini_w_ground_with_google_search(llm_remote_text_df):
    model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001", max_iterations=1)
    df = model.predict(
        llm_remote_text_df["prompt"],
        ground_with_google_search=True,
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df,
        columns=[
            "ml_generate_text_llm_result",
            "ml_generate_text_rai_result",
            "ml_generate_text_grounding_result",
            "ml_generate_text_status",
            "prompt",
        ],
        index=3,
    )


# (b/366290533): Claude models are of extremely low capacity. The tests should reside in small tests. Moving these here just to protect BQML's shared capacity(as load test only runs once per day.) and make sure we still have minimum coverage.
@pytest.mark.parametrize(
    "model_name",
    ("claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"),
)
@pytest.mark.flaky(retries=3, delay=120)
def test_claude3_text_generator_create_load(
    dataset_id, model_name, session, session_us_east5, bq_connection
):
    if model_name in ("claude-3-5-sonnet", "claude-3-opus"):
        session = session_us_east5
    claude3_text_generator_model = llm.Claude3TextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    assert claude3_text_generator_model is not None
    assert claude3_text_generator_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = claude3_text_generator_model.to_gbq(
        f"{dataset_id}.temp_text_model", replace=True
    )
    assert f"{dataset_id}.temp_text_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.connection_name == bq_connection
    assert reloaded_model.model_name == model_name


@pytest.mark.parametrize(
    "model_name",
    ("claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"),
)
@pytest.mark.flaky(retries=3, delay=120)
def test_claude3_text_generator_predict_default_params_success(
    llm_text_df, model_name, session, session_us_east5, bq_connection
):
    if model_name in ("claude-3-5-sonnet", "claude-3-opus"):
        session = session_us_east5
    claude3_text_generator_model = llm.Claude3TextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = claude3_text_generator_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.parametrize(
    "model_name",
    ("claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"),
)
@pytest.mark.flaky(retries=3, delay=120)
def test_claude3_text_generator_predict_with_params_success(
    llm_text_df, model_name, session, session_us_east5, bq_connection
):
    if model_name in ("claude-3-5-sonnet", "claude-3-opus"):
        session = session_us_east5
    claude3_text_generator_model = llm.Claude3TextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = claude3_text_generator_model.predict(
        llm_text_df, max_output_tokens=100, top_k=20, top_p=0.5
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.parametrize(
    "model_name",
    ("claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"),
)
@pytest.mark.flaky(retries=3, delay=120)
def test_claude3_text_generator_predict_multi_col_success(
    llm_text_df, model_name, session, session_us_east5, bq_connection
):
    if model_name in ("claude-3-5-sonnet", "claude-3-opus"):
        session = session_us_east5

    llm_text_df["additional_col"] = 1
    claude3_text_generator_model = llm.Claude3TextGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = claude3_text_generator_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df,
        columns=utils.ML_GENERATE_TEXT_OUTPUT + ["additional_col"],
        index=3,
        col_exact=False,
    )
