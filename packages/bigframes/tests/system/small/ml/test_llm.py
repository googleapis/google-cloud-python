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

import pytest

from bigframes import exceptions
from bigframes.ml import llm
import bigframes.pandas as bpd
from tests.system import utils


def test_create_load_text_generator_model(
    palm2_text_generator_model, dataset_id, bq_connection
):
    # Model creation doesn't return error
    assert palm2_text_generator_model is not None
    assert palm2_text_generator_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = palm2_text_generator_model.to_gbq(
        f"{dataset_id}.temp_text_model", replace=True
    )
    assert f"{dataset_id}.temp_text_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.model_name == "text-bison"
    assert reloaded_model.connection_name == bq_connection


def test_create_load_text_generator_32k_model(
    palm2_text_generator_32k_model, dataset_id, bq_connection
):
    # Model creation doesn't return error
    assert palm2_text_generator_32k_model is not None
    assert palm2_text_generator_32k_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = palm2_text_generator_32k_model.to_gbq(
        f"{dataset_id}.temp_text_model", replace=True
    )
    assert f"{dataset_id}.temp_text_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.model_name == "text-bison-32k"
    assert reloaded_model.connection_name == bq_connection


@pytest.mark.flaky(retries=2)
def test_create_text_generator_model_default_session(
    bq_connection, llm_text_pandas_df, bigquery_client
):
    import bigframes.pandas as bpd

    # Note: This starts a thread-local session.
    with bpd.option_context(
        "bigquery.bq_connection",
        bq_connection,
        "bigquery.location",
        "US",
    ):
        model = llm.PaLM2TextGenerator()
        assert model is not None
        assert model._bqml_model is not None
        assert (
            model.connection_name.casefold()
            == f"{bigquery_client.project}.us.bigframes-rf-conn"
        )

        llm_text_df = bpd.read_pandas(llm_text_pandas_df)

        df = model.predict(llm_text_df).to_pandas()
        utils.check_pandas_df_schema_and_index(
            df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
        )


@pytest.mark.flaky(retries=2)
def test_create_text_generator_32k_model_default_session(
    bq_connection, llm_text_pandas_df, bigquery_client
):
    import bigframes.pandas as bpd

    # Note: This starts a thread-local session.
    with bpd.option_context(
        "bigquery.bq_connection",
        bq_connection,
        "bigquery.location",
        "US",
    ):
        model = llm.PaLM2TextGenerator(model_name="text-bison-32k")
        assert model is not None
        assert model._bqml_model is not None
        assert (
            model.connection_name.casefold()
            == f"{bigquery_client.project}.us.bigframes-rf-conn"
        )

        llm_text_df = bpd.read_pandas(llm_text_pandas_df)

        df = model.predict(llm_text_df).to_pandas()
        utils.check_pandas_df_schema_and_index(
            df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
        )


@pytest.mark.flaky(retries=2)
def test_create_text_generator_model_default_connection(
    llm_text_pandas_df, bigquery_client
):
    from bigframes import _config
    import bigframes.pandas as bpd

    bpd.close_session()
    _config.options = _config.Options()  # reset configs

    llm_text_df = bpd.read_pandas(llm_text_pandas_df)

    model = llm.PaLM2TextGenerator()
    assert model is not None
    assert model._bqml_model is not None
    assert (
        model.connection_name.casefold()
        == f"{bigquery_client.project}.us.bigframes-default-connection"
    )

    df = model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


# Marked as flaky only because BQML LLM is in preview, the service only has limited capacity, not stable enough.
@pytest.mark.flaky(retries=2)
def test_text_generator_predict_default_params_success(
    palm2_text_generator_model, llm_text_df
):
    df = palm2_text_generator_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.flaky(retries=2)
def test_text_generator_predict_series_default_params_success(
    palm2_text_generator_model, llm_text_df
):
    df = palm2_text_generator_model.predict(llm_text_df["prompt"]).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.flaky(retries=2)
def test_text_generator_predict_arbitrary_col_label_success(
    palm2_text_generator_model, llm_text_df
):
    llm_text_df = llm_text_df.rename(columns={"prompt": "arbitrary"})
    df = palm2_text_generator_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.flaky(retries=2)
def test_text_generator_predict_multiple_cols_success(
    palm2_text_generator_model, llm_text_df: bpd.DataFrame
):
    df = llm_text_df.assign(additional_col=1)
    pd_df = palm2_text_generator_model.predict(df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        pd_df,
        columns=utils.ML_GENERATE_TEXT_OUTPUT + ["additional_col"],
        index=3,
        col_exact=False,
    )


@pytest.mark.flaky(retries=2)
def test_text_generator_predict_with_params_success(
    palm2_text_generator_model, llm_text_df
):
    df = palm2_text_generator_model.predict(
        llm_text_df, temperature=0.5, max_output_tokens=100, top_k=20, top_p=0.5
    ).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_TEXT_OUTPUT, index=3, col_exact=False
    )


@pytest.mark.parametrize(
    "model_name",
    ("text-embedding-004", "text-multilingual-embedding-002"),
)
def test_create_load_text_embedding_generator_model(
    dataset_id, model_name, session, bq_connection
):
    text_embedding_model = llm.TextEmbeddingGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    assert text_embedding_model is not None
    assert text_embedding_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = text_embedding_model.to_gbq(
        f"{dataset_id}.temp_text_model", replace=True
    )
    assert f"{dataset_id}.temp_text_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.connection_name == bq_connection
    assert reloaded_model.model_name == model_name


@pytest.mark.parametrize(
    "model_name",
    ("text-embedding-004", "text-multilingual-embedding-002"),
)
@pytest.mark.flaky(retries=2)
def test_text_embedding_generator_predict_default_params_success(
    llm_text_df, model_name, session, bq_connection
):
    text_embedding_model = llm.TextEmbeddingGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    df = text_embedding_model.predict(llm_text_df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        df, columns=utils.ML_GENERATE_EMBEDDING_OUTPUT, index=3, col_exact=False
    )
    assert len(df["ml_generate_embedding_result"][0]) == 768


@pytest.mark.parametrize(
    "model_name",
    ("text-embedding-004", "text-multilingual-embedding-002"),
)
@pytest.mark.flaky(retries=2)
def test_text_embedding_generator_multi_cols_predict_success(
    llm_text_df: bpd.DataFrame, model_name, session, bq_connection
):
    df = llm_text_df.assign(additional_col=1)
    df = df.rename(columns={"prompt": "content"})
    text_embedding_model = llm.TextEmbeddingGenerator(
        model_name=model_name, connection_name=bq_connection, session=session
    )
    pd_df = text_embedding_model.predict(df).to_pandas()
    utils.check_pandas_df_schema_and_index(
        pd_df,
        columns=utils.ML_GENERATE_EMBEDDING_OUTPUT + ["additional_col"],
        index=3,
        col_exact=False,
    )
    assert len(pd_df["ml_generate_embedding_result"][0]) == 768


@pytest.mark.parametrize(
    "model_name",
    (
        "gemini-pro",
        "gemini-1.5-pro-preview-0514",
        "gemini-1.5-flash-preview-0514",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
    ),
)
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
        "gemini-pro",
        "gemini-1.5-pro-preview-0514",
        "gemini-1.5-flash-preview-0514",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
    ),
)
@pytest.mark.flaky(retries=2)
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
        "gemini-pro",
        "gemini-1.5-pro-preview-0514",
        "gemini-1.5-flash-preview-0514",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
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
        "gemini-pro",
        "gemini-1.5-pro-preview-0514",
        "gemini-1.5-flash-preview-0514",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
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


@pytest.mark.flaky(retries=2)
def test_llm_palm_score(llm_fine_tune_df_default_index):
    model = llm.PaLM2TextGenerator(model_name="text-bison")

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


@pytest.mark.flaky(retries=2)
def test_llm_palm_score_params(llm_fine_tune_df_default_index):
    model = llm.PaLM2TextGenerator(model_name="text-bison", max_iterations=1)

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
        index=6,
    )


@pytest.mark.flaky(retries=2)
def test_llm_gemini_pro_score(llm_fine_tune_df_default_index):
    model = llm.GeminiTextGenerator(model_name="gemini-pro")

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


@pytest.mark.flaky(retries=2)
def test_llm_gemini_pro_score_params(llm_fine_tune_df_default_index):
    model = llm.GeminiTextGenerator(model_name="gemini-pro")

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
        index=6,
    )


def test_palm2_text_generator_deprecated():
    with pytest.warns(exceptions.ApiDeprecationWarning):
        llm.PaLM2TextGenerator()


def test_palm2_text_embedding_deprecated():
    with pytest.warns(exceptions.ApiDeprecationWarning):
        try:
            llm.PaLM2TextEmbeddingGenerator()
        except (Exception):
            pass
