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


def test_gemini_text_generator_model() -> None:
    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")
    REGION = "us"
    CONN_NAME = "bigframes-default-connection"

    # [START bigquery_dataframes_gemini_model]
    from bigframes.ml.llm import GeminiTextGenerator
    import bigframes.pandas as bpd

    # Create the Gemini LLM model
    session = bpd.get_global_session()
    connection = f"{PROJECT_ID}.{REGION}.{CONN_NAME}"
    model = GeminiTextGenerator(
        session=session, connection_name=connection, model_name="gemini-2.0-flash-001"
    )

    df_api = bpd.read_csv("gs://cloud-samples-data/vertex-ai/bigframe/df.csv")

    # Prepare the prompts and send them to the LLM model for prediction
    df_prompt_prefix = "Generate Pandas sample code for DataFrame."
    df_prompt = df_prompt_prefix + df_api["API"]

    # Predict using the model
    df_pred = model.predict(df_prompt.to_frame(), max_output_tokens=1024)
    # [END bigquery_dataframes_gemini_model]
    assert df_pred["ml_generate_text_llm_result"] is not None
    assert df_pred["ml_generate_text_llm_result"].iloc[0] is not None
