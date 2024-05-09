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


def test_llm_text_generation() -> None:
    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")
    LOCATION = "US"

    # [START bigquery_dataframes_generate_text_tutorial_create_remote_model]
    import bigframes
    from bigframes.ml.llm import PaLM2TextGenerator

    bigframes.options.bigquery.project = PROJECT_ID
    bigframes.options.bigquery.location = LOCATION

    model = PaLM2TextGenerator()
    # [END bigquery_dataframes_generate_text_tutorial_create_remote_model]
    assert model is not None

    # [START bigquery_dataframes_generate_text_tutorial_perform_keyword_extraction]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.imdb.reviews", max_results=5)
    df_prompt_prefix = "Extract the key words from the text below: "
    df_prompt = df_prompt_prefix + df["review"]

    # Predict using the model
    df_pred = model.predict(df_prompt, temperature=0.2, max_output_tokens=100)
    df_pred.peek(5)
    # [END bigquery_dataframes_generate_text_tutorial_perform_keyword_extraction]
    # peek() is used to show a preview of the results. If the output
    # of this sample changes, also update the screenshot for the associated
    # tutorial on cloud.google.com.
    assert df_pred["ml_generate_text_llm_result"] is not None
    assert df_pred["ml_generate_text_llm_result"].iloc[0] is not None

    # [START bigquery_dataframes_generate_text_tutorial_perform_sentiment_analysis]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.imdb.reviews", max_results=5)
    df_prompt_prefix = "perform sentiment analysis on the following text, return one the following categories: positive, negative: "
    df_prompt = df_prompt_prefix + df["review"]

    # Predict using the model
    df_pred = model.predict(df_prompt, temperature=0.2, max_output_tokens=100)
    df_pred.peek(5)
    # [END bigquery_dataframes_generate_text_tutorial_perform_sentiment_analysis]
    # peek() is used to show a preview of the results. If the output
    # of this sample changes, also update the screenshot for the associated
    # tutorial on cloud.google.com.

    assert df_pred["ml_generate_text_llm_result"] is not None
    assert df_pred["ml_generate_text_llm_result"].iloc[0] is not None
