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
from tests.system import utils


@pytest.fixture(scope="session")
def llm_remote_text_pandas_df():
    """Additional data matching the penguins dataset, with a new index"""
    return pd.DataFrame(
        {
            "prompt": [
                "Please do sentiment analysis on the following text and only output a number from 0 to 5where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: i feel beautifully emotional knowing that these women of whom i knew just a handful were holding me and my baba on our journey",
                "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: i was feeling a little vain when i did this one",
                "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: a father of children killed in an accident",
            ],
        }
    )


@pytest.fixture(scope="session")
def llm_remote_text_df(session, llm_remote_text_pandas_df):
    return session.read_pandas(llm_remote_text_pandas_df)


@pytest.mark.flaky(retries=2)
def test_llm_palm_configure_fit(llm_fine_tune_df_default_index, llm_remote_text_df):
    model = llm.PaLM2TextGenerator(model_name="text-bison", max_iterations=1)

    X_train = llm_fine_tune_df_default_index[["prompt"]]
    y_train = llm_fine_tune_df_default_index[["label"]]
    model.fit(X_train, y_train)

    assert model is not None

    df = model.predict(llm_remote_text_df["prompt"]).to_pandas()
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
    # TODO(ashleyxu b/335492787): After bqml rolled out version control: save, load, check parameters to ensure configuration was kept


@pytest.mark.flaky(retries=2)
def test_llm_gemini_configure_fit(llm_fine_tune_df_default_index, llm_remote_text_df):
    model = llm.GeminiTextGenerator(model_name="gemini-pro", max_iterations=1)

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
    # TODO(ashleyxu b/335492787): After bqml rolled out version control: save, load, check parameters to ensure configuration was kept
