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

from typing import Callable
from unittest import mock

import pandas as pd
import pytest

from bigframes import exceptions
from bigframes.ml import core, llm
import bigframes.pandas as bpd
from bigframes.testing import utils


@pytest.mark.parametrize(
    "model_name",
    ("text-embedding-005", "text-embedding-004", "text-multilingual-embedding-002"),
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
    ("text-embedding-005", "text-embedding-004", "text-multilingual-embedding-002"),
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
    ("text-embedding-005", "text-embedding-004", "text-multilingual-embedding-002"),
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


def test_create_load_multimodal_embedding_generator_model(
    dataset_id, session, bq_connection
):
    mm_embedding_model = llm.MultimodalEmbeddingGenerator(
        connection_name=bq_connection, session=session
    )
    assert mm_embedding_model is not None
    assert mm_embedding_model._bqml_model is not None

    # save, load to ensure configuration was kept
    reloaded_model = mm_embedding_model.to_gbq(
        f"{dataset_id}.temp_mm_model", replace=True
    )
    assert f"{dataset_id}.temp_mm_model" == reloaded_model._bqml_model.model_name
    assert reloaded_model.connection_name == bq_connection


# Overrides __eq__ function for comparing as mock.call parameter
class EqCmpAllDataFrame(bpd.DataFrame):
    def __eq__(self, other):
        return self.equals(other)


@pytest.mark.skip("b/436340035 test failed")
@pytest.mark.parametrize(
    (
        "model_class",
        "options",
    ),
    [
        (
            llm.GeminiTextGenerator,
            {
                "temperature": 0.9,
                "max_output_tokens": 8192,
                "top_p": 1.0,
                "ground_with_google_search": False,
            },
        ),
        (
            llm.Claude3TextGenerator,
            {
                "max_output_tokens": 128,
                "top_k": 40,
                "top_p": 0.95,
            },
        ),
    ],
)
def test_text_generator_retry_success(
    session,
    model_class,
    options,
    bq_connection,
):
    # Requests.
    df0 = EqCmpAllDataFrame(
        {
            "prompt": [
                "What is BigQuery?",
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ]
        },
        index=[0, 1, 2],
        session=session,
    )
    df1 = EqCmpAllDataFrame(
        {
            "ml_generate_text_status": ["error", "error"],
            "prompt": [
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ],
        },
        index=[1, 2],
        session=session,
    )
    df2 = EqCmpAllDataFrame(
        {
            "ml_generate_text_status": ["error"],
            "prompt": [
                "What is BQML?",
            ],
        },
        index=[1],
        session=session,
    )

    mock_generate_text = mock.create_autospec(
        Callable[[core.BqmlModel, bpd.DataFrame, dict], bpd.DataFrame]
    )
    mock_bqml_model = mock.create_autospec(spec=core.BqmlModel)
    type(mock_bqml_model).session = mock.PropertyMock(return_value=session)
    generate_text_tvf = core.BqmlModel.TvfDef(
        mock_generate_text, "ml_generate_text_status"
    )
    # Responses. Retry twice then all succeeded.
    mock_generate_text.side_effect = [
        EqCmpAllDataFrame(
            {
                "ml_generate_text_status": ["", "error", "error"],
                "prompt": [
                    "What is BigQuery?",
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[0, 1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_text_status": ["error", ""],
                "prompt": [
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_text_status": [""],
                "prompt": [
                    "What is BQML?",
                ],
            },
            index=[1],
            session=session,
        ),
    ]

    text_generator_model = model_class(connection_name=bq_connection, session=session)
    text_generator_model._bqml_model = mock_bqml_model

    with mock.patch.object(core.BqmlModel, "generate_text_tvf", generate_text_tvf):
        # 3rd retry isn't triggered
        result = text_generator_model.predict(df0, max_retries=3)

        mock_generate_text.assert_has_calls(
            [
                mock.call(mock_bqml_model, df0, options),
                mock.call(mock_bqml_model, df1, options),
                mock.call(mock_bqml_model, df2, options),
            ]
        )
        pd.testing.assert_frame_equal(
            result.to_pandas(),
            pd.DataFrame(
                {
                    "ml_generate_text_status": ["", "", ""],
                    "prompt": [
                        "What is BigQuery?",
                        "What is BigQuery DataFrame?",
                        "What is BQML?",
                    ],
                },
                index=[0, 2, 1],
            ),
            check_dtype=False,
            check_index_type=False,
        )


@pytest.mark.skip("b/436340035 test failed")
@pytest.mark.parametrize(
    (
        "model_class",
        "options",
    ),
    [
        (
            llm.GeminiTextGenerator,
            {
                "temperature": 0.9,
                "max_output_tokens": 8192,
                "top_p": 1.0,
                "ground_with_google_search": False,
            },
        ),
        (
            llm.Claude3TextGenerator,
            {
                "max_output_tokens": 128,
                "top_k": 40,
                "top_p": 0.95,
            },
        ),
    ],
)
def test_text_generator_retry_no_progress(session, model_class, options, bq_connection):
    # Requests.
    df0 = EqCmpAllDataFrame(
        {
            "prompt": [
                "What is BigQuery?",
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ]
        },
        index=[0, 1, 2],
        session=session,
    )
    df1 = EqCmpAllDataFrame(
        {
            "ml_generate_text_status": ["error", "error"],
            "prompt": [
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ],
        },
        index=[1, 2],
        session=session,
    )

    mock_generate_text = mock.create_autospec(
        Callable[[core.BqmlModel, bpd.DataFrame, dict], bpd.DataFrame]
    )
    mock_bqml_model = mock.create_autospec(spec=core.BqmlModel)
    type(mock_bqml_model).session = mock.PropertyMock(return_value=session)
    generate_text_tvf = core.BqmlModel.TvfDef(
        mock_generate_text, "ml_generate_text_status"
    )
    # Responses. Retry once, no progress, just stop.
    mock_generate_text.side_effect = [
        EqCmpAllDataFrame(
            {
                "ml_generate_text_status": ["", "error", "error"],
                "prompt": [
                    "What is BigQuery?",
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[0, 1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_text_status": ["error", "error"],
                "prompt": [
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[1, 2],
            session=session,
        ),
    ]

    text_generator_model = model_class(connection_name=bq_connection, session=session)
    text_generator_model._bqml_model = mock_bqml_model

    with mock.patch.object(core.BqmlModel, "generate_text_tvf", generate_text_tvf):
        # No progress, only conduct retry once
        result = text_generator_model.predict(df0, max_retries=3)

        mock_generate_text.assert_has_calls(
            [
                mock.call(mock_bqml_model, df0, options),
                mock.call(mock_bqml_model, df1, options),
            ]
        )
        pd.testing.assert_frame_equal(
            result.to_pandas(),
            pd.DataFrame(
                {
                    "ml_generate_text_status": ["", "error", "error"],
                    "prompt": [
                        "What is BigQuery?",
                        "What is BQML?",
                        "What is BigQuery DataFrame?",
                    ],
                },
                index=[0, 1, 2],
            ),
            check_dtype=False,
            check_index_type=False,
        )


@pytest.mark.skip("b/436340035 test failed")
def test_text_embedding_generator_retry_success(session, bq_connection):
    # Requests.
    df0 = EqCmpAllDataFrame(
        {
            "content": [
                "What is BigQuery?",
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ]
        },
        index=[0, 1, 2],
        session=session,
    )
    df1 = EqCmpAllDataFrame(
        {
            "ml_generate_embedding_status": ["error", "error"],
            "content": [
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ],
        },
        index=[1, 2],
        session=session,
    )
    df2 = EqCmpAllDataFrame(
        {
            "ml_generate_embedding_status": ["error"],
            "content": [
                "What is BQML?",
            ],
        },
        index=[1],
        session=session,
    )

    mock_generate_embedding = mock.create_autospec(
        Callable[[core.BqmlModel, bpd.DataFrame, dict], bpd.DataFrame]
    )
    mock_bqml_model = mock.create_autospec(spec=core.BqmlModel)
    type(mock_bqml_model).session = mock.PropertyMock(return_value=session)
    generate_embedding_tvf = core.BqmlModel.TvfDef(
        mock_generate_embedding, "ml_generate_embedding_status"
    )

    # Responses. Retry twice then all succeeded.
    mock_generate_embedding.side_effect = [
        EqCmpAllDataFrame(
            {
                "ml_generate_embedding_status": ["", "error", "error"],
                "content": [
                    "What is BigQuery?",
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[0, 1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_embedding_status": ["error", ""],
                "content": [
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_embedding_status": [""],
                "content": [
                    "What is BQML?",
                ],
            },
            index=[1],
            session=session,
        ),
    ]
    options: dict = {}

    text_embedding_model = llm.TextEmbeddingGenerator(
        connection_name=bq_connection, session=session
    )
    text_embedding_model._bqml_model = mock_bqml_model

    with mock.patch.object(
        core.BqmlModel, "generate_embedding_tvf", generate_embedding_tvf
    ):
        # 3rd retry isn't triggered
        result = text_embedding_model.predict(df0, max_retries=3)

        mock_generate_embedding.assert_has_calls(
            [
                mock.call(mock_bqml_model, df0, options),
                mock.call(mock_bqml_model, df1, options),
                mock.call(mock_bqml_model, df2, options),
            ]
        )
        pd.testing.assert_frame_equal(
            result.to_pandas(),
            pd.DataFrame(
                {
                    "ml_generate_embedding_status": ["", "", ""],
                    "content": [
                        "What is BigQuery?",
                        "What is BigQuery DataFrame?",
                        "What is BQML?",
                    ],
                },
                index=[0, 2, 1],
            ),
            check_dtype=False,
            check_index_type=False,
        )


def test_text_embedding_generator_retry_no_progress(session, bq_connection):
    # Requests.
    df0 = EqCmpAllDataFrame(
        {
            "content": [
                "What is BigQuery?",
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ]
        },
        index=[0, 1, 2],
        session=session,
    )
    df1 = EqCmpAllDataFrame(
        {
            "ml_generate_embedding_status": ["error", "error"],
            "content": [
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ],
        },
        index=[1, 2],
        session=session,
    )

    mock_generate_embedding = mock.create_autospec(
        Callable[[core.BqmlModel, bpd.DataFrame, dict], bpd.DataFrame]
    )
    mock_bqml_model = mock.create_autospec(spec=core.BqmlModel)
    type(mock_bqml_model).session = mock.PropertyMock(return_value=session)
    generate_embedding_tvf = core.BqmlModel.TvfDef(
        mock_generate_embedding, "ml_generate_embedding_status"
    )

    # Responses. Retry once, no progress, just stop.
    mock_generate_embedding.side_effect = [
        EqCmpAllDataFrame(
            {
                "ml_generate_embedding_status": ["", "error", "error"],
                "content": [
                    "What is BigQuery?",
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[0, 1, 2],
            session=session,
        ),
        EqCmpAllDataFrame(
            {
                "ml_generate_embedding_status": ["error", "error"],
                "content": [
                    "What is BQML?",
                    "What is BigQuery DataFrame?",
                ],
            },
            index=[1, 2],
            session=session,
        ),
    ]
    options: dict = {}

    text_embedding_model = llm.TextEmbeddingGenerator(
        connection_name=bq_connection, session=session
    )
    text_embedding_model._bqml_model = mock_bqml_model

    with mock.patch.object(
        core.BqmlModel, "generate_embedding_tvf", generate_embedding_tvf
    ):
        # No progress, only conduct retry once
        result = text_embedding_model.predict(df0, max_retries=3)

        mock_generate_embedding.assert_has_calls(
            [
                mock.call(mock_bqml_model, df0, options),
                mock.call(mock_bqml_model, df1, options),
            ]
        )
        pd.testing.assert_frame_equal(
            result.to_pandas(),
            pd.DataFrame(
                {
                    "ml_generate_embedding_status": ["", "error", "error"],
                    "content": [
                        "What is BigQuery?",
                        "What is BQML?",
                        "What is BigQuery DataFrame?",
                    ],
                },
                index=[0, 1, 2],
            ),
            check_dtype=False,
            check_index_type=False,
        )


@pytest.mark.parametrize(
    "model_name",
    ("gemini-2.0-flash-exp",),
)
def test_gemini_preview_model_warnings(model_name):
    with pytest.warns(exceptions.PreviewWarning):
        llm.GeminiTextGenerator(model_name=model_name)


# b/436340035 temp disable the test to unblock presumbit
@pytest.mark.parametrize(
    "model_class",
    [
        llm.TextEmbeddingGenerator,
        llm.MultimodalEmbeddingGenerator,
        llm.GeminiTextGenerator,
        # llm.Claude3TextGenerator,
    ],
)
def test_text_embedding_generator_no_default_model_warning(model_class):
    message = "Since upgrading the default model can cause unintended breakages, the\ndefault model will be removed in BigFrames 3.0. Please supply an\nexplicit model to avoid this message."
    with pytest.warns(FutureWarning, match=message):
        model_class(model_name=None)
