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

from __future__ import annotations

import re
import typing
from typing import Dict, Iterable, List, Optional, Sequence, Union
import warnings

from bigframes import dtypes, exceptions, options
from bigframes.core import guid, log_adapter


@log_adapter.class_logger
class AIAccessor:
    def __init__(self, df, base_bqml=None) -> None:
        import bigframes  # Import in the function body to avoid circular imports.
        import bigframes.dataframe
        from bigframes.ml import core as ml_core

        self._df: bigframes.dataframe.DataFrame = df
        self._base_bqml: ml_core.BaseBqml = base_bqml or ml_core.BaseBqml(df._session)

    def filter(
        self,
        instruction: str,
        model,
        ground_with_google_search: bool = False,
    ):
        """
        Filters the DataFrame with the semantics of the user instruction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

            >>> df = bpd.DataFrame({"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]})
            >>> df.ai.filter("{city} is the capital of {country}", model)
               country    city
            1  Germany  Berlin
            <BLANKLINE>
            [1 rows x 2 columns]

        Args:
            instruction (str):
                An instruction on how to filter the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "The {food} is healthy."

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by Bigframes ML package.

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.pandas.DataFrame: DataFrame filtered by the instruction.

        Raises:
            NotImplementedError: when the AI operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        answer_col = "answer"

        output_schema = {answer_col: "bool"}
        result = self.map(
            instruction,
            model,
            output_schema,
            ground_with_google_search,
        )

        return result[result[answer_col]].drop(answer_col, axis=1)

    def map(
        self,
        instruction: str,
        model,
        output_schema: Dict[str, str] | None = None,
        ground_with_google_search: bool = False,
    ):
        """
        Maps the DataFrame with the semantics of the user instruction. The name of the keys in the output_schema parameter carry
        semantic meaning, and can be used for information extraction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

            >>> df = bpd.DataFrame({"ingredient_1": ["Burger Bun", "Soy Bean"], "ingredient_2": ["Beef Patty", "Bittern"]})
            >>> df.ai.map("What is the food made from {ingredient_1} and {ingredient_2}? One word only.", model=model, output_schema={"food": "string"})
              ingredient_1 ingredient_2      food
            0   Burger Bun   Beef Patty  Burger
            <BLANKLINE>
            1     Soy Bean      Bittern    Tofu
            <BLANKLINE>
            <BLANKLINE>
            [2 rows x 3 columns]


            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

            >>> df = bpd.DataFrame({"text": ["Elmo lives at 123 Sesame Street."]})
            >>> df.ai.map("{text}", model=model, output_schema={"person": "string", "address": "string"})
                                           text person            address
            0  Elmo lives at 123 Sesame Street.   Elmo  123 Sesame Street
            <BLANKLINE>
            [1 rows x 3 columns]

        Args:
            instruction (str):
                An instruction on how to map the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "Get the ingredients of {food}."

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by Bigframes ML package.

            output_schema (Dict[str, str] or None, default None):
                The schema used to generate structured output as a bigframes DataFrame. The schema is a string key-value pair of <column_name>:<type>.
                Supported types are int64, float64, bool, string, array<type> and struct<column type>. If None, generate string result under the column
                "ml_generate_text_llm_result".

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.pandas.DataFrame: DataFrame with attached mapping results.

        Raises:
            NotImplementedError: when the AI operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        import bigframes.dataframe
        import bigframes.series

        self._validate_model(model)
        columns = self._parse_columns(instruction)
        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column {column} not found.")

        if ground_with_google_search:
            msg = exceptions.format_message(
                "Enables Grounding with Google Search may impact billing cost. See pricing "
                "details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models"
            )
            warnings.warn(msg, category=UserWarning)

        self._confirm_operation(len(self._df))

        df: bigframes.dataframe.DataFrame = self._df[columns].copy()
        has_blob_column = False
        for column in columns:
            if df[column].dtype == dtypes.OBJ_REF_DTYPE:
                # Don't cast blob columns to string
                has_blob_column = True
                continue

            if df[column].dtype != dtypes.STRING_DTYPE:
                df[column] = df[column].astype(dtypes.STRING_DTYPE)

        user_instruction = self._format_instruction(instruction, columns)
        output_instruction = (
            "Based on the provided contenxt, answer the following instruction:"
        )

        if output_schema is None:
            output_schema = {"ml_generate_text_llm_result": "string"}

        if has_blob_column:
            results = typing.cast(
                bigframes.series.Series,
                model.predict(
                    df,
                    prompt=self._make_multimodel_prompt(
                        df, columns, user_instruction, output_instruction
                    ),
                    temperature=0.0,
                    ground_with_google_search=ground_with_google_search,
                    output_schema=output_schema,
                ),
            )
        else:
            results = typing.cast(
                bigframes.series.Series,
                model.predict(
                    self._make_text_prompt(
                        df, columns, user_instruction, output_instruction
                    ),
                    temperature=0.0,
                    ground_with_google_search=ground_with_google_search,
                    output_schema=output_schema,
                ),
            )

        attach_columns = [results[col] for col, _ in output_schema.items()]

        from bigframes.core.reshape.api import concat

        return concat([self._df, *attach_columns], axis=1)

    def classify(
        self,
        instruction: str,
        model,
        labels: Sequence[str],
        output_column: str = "result",
        ground_with_google_search: bool = False,
    ):
        """
        Classifies the rows of dataframes based on user instruction into the provided labels.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

            >>> df = bpd.DataFrame({
            ...     "feedback_text": [
            ...         "The product is amazing, but the shipping was slow.",
            ...         "I had an issue with my recent bill.",
            ...         "The user interface is very intuitive."
            ...     ],
            ... })
            >>> df.ai.classify("{feedback_text}", model=model, labels=["Shipping", "Billing", "UI"])
                                                   feedback_text     result
            0  The product is amazing, but the shipping was s...   Shipping
            1                I had an issue with my recent bill.    Billing
            2              The user interface is very intuitive.         UI
            <BLANKLINE>
            [3 rows x 2 columns]

        Args:
            instruction (str):
                An instruction on how to classify the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "feedback", you can refer to this column
                with"{food}".

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by Bigframes ML package.

            labels (Sequence[str]):
                A collection of labels (categories). It must contain at least two and at most 20 elements.
                Labels are case sensitive. Duplicated labels are not allowed.

            output_column (str, default "result"):
                The name of column for the output.

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.pandas.DataFrame: DataFrame with classification result.

        Raises:
            NotImplementedError: when the AI operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, when no
                columns are referred to, or when the count of labels does not meet the
                requirement.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        if len(labels) < 2 or len(labels) > 20:
            raise ValueError(
                f"The number of labels should be between 2 and 20 (inclusive), but {len(labels)} labels are provided."
            )

        if len(set(labels)) != len(labels):
            raise ValueError("There are duplicate labels.")

        updated_instruction = f"Based on the user instruction {instruction}, you must provide an answer that must exist in the following list of labels: {labels}"

        return self.map(
            updated_instruction,
            model,
            output_schema={output_column: "string"},
            ground_with_google_search=ground_with_google_search,
        )

    def join(
        self,
        other,
        instruction: str,
        model,
        ground_with_google_search: bool = False,
    ):
        """
        Joines two dataframes by applying the instruction over each pair of rows from
        the left and right table.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

            >>> cities = bpd.DataFrame({'city': ['Seattle', 'Ottawa', 'Berlin', 'Shanghai', 'New Delhi']})
            >>> continents = bpd.DataFrame({'continent': ['North America', 'Africa', 'Asia']})

            >>> cities.ai.join(continents, "{city} is in {continent}", model)
                    city      continent
            0    Seattle  North America
            1     Ottawa  North America
            2   Shanghai           Asia
            3  New Delhi           Asia
            <BLANKLINE>
            [4 rows x 2 columns]

        Args:
            other (bigframes.pandas.DataFrame):
                The other dataframe.

            instruction (str):
                An instruction on how left and right rows can be joined. This value must contain
                column references by name. which should be wrapped in a pair of braces.
                For example: "The {city} belongs to the {country}".
                For column names that are shared between two dataframes, you need to add "left."
                and "right." prefix for differentiation. This is especially important when you do
                self joins. For example: "The {left.employee_name} reports to {right.employee_name}"
                For unique column names, this prefix is optional.

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by Bigframes ML package.

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.pandas.DataFrame: The joined dataframe.

        Raises:
            ValueError if the amount of data that will be sent for LLM processing is larger than max_rows.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        self._validate_model(model)
        columns = self._parse_columns(instruction)

        if ground_with_google_search:
            msg = exceptions.format_message(
                "Enables Grounding with Google Search may impact billing cost. See pricing "
                "details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models"
            )
            warnings.warn(msg, category=UserWarning)

        work_estimate = len(self._df) * len(other)
        self._confirm_operation(work_estimate)

        left_columns = []
        right_columns = []

        for col in columns:
            if col in self._df.columns and col in other.columns:
                raise ValueError(f"Ambiguous column reference: {col}")

            elif col in self._df.columns:
                left_columns.append(col)

            elif col in other.columns:
                right_columns.append(col)

            elif col.startswith("left."):
                original_col_name = col[len("left.") :]
                if (
                    original_col_name in self._df.columns
                    and original_col_name in other.columns
                ):
                    left_columns.append(col)
                elif original_col_name in self._df.columns:
                    left_columns.append(col)
                    instruction = instruction.replace(col, original_col_name)
                else:
                    raise ValueError(f"Column {col} not found")

            elif col.startswith("right."):
                original_col_name = col[len("right.") :]
                if (
                    original_col_name in self._df.columns
                    and original_col_name in other.columns
                ):
                    right_columns.append(col)
                elif original_col_name in other.columns:
                    right_columns.append(col)
                    instruction = instruction.replace(col, original_col_name)
                else:
                    raise ValueError(f"Column {col} not found")

            else:
                raise ValueError(f"Column {col} not found")

        if not left_columns:
            raise ValueError("No left column references.")

        if not right_columns:
            raise ValueError("No right column references.")

        # Update column references to be compatible with internal naming scheme.
        # That is, "left.col" -> "col_left" and "right.col" -> "col_right"
        instruction = re.sub(r"(?<!{){left\.(\w+)}(?!})", r"{\1_left}", instruction)
        instruction = re.sub(r"(?<!{){right\.(\w+)}(?!})", r"{\1_right}", instruction)

        joined_df = self._df.merge(other, how="cross", suffixes=("_left", "_right"))

        return joined_df.ai.filter(
            instruction,
            model,
            ground_with_google_search=ground_with_google_search,
        ).reset_index(drop=True)

    def search(
        self,
        search_column: str,
        query: str,
        top_k: int,
        model,
        score_column: Optional[str] = None,
    ):
        """
        Performs AI semantic search on the DataFrame.

        ** Examples: **

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-005")

            >>> df = bpd.DataFrame({"creatures": ["salmon", "sea urchin", "frog", "chimpanzee"]})
            >>> df.ai.search("creatures", "monkey", top_k=1, model=model, score_column='distance')
                creatures  distance
            3  chimpanzee  0.635844
            <BLANKLINE>
            [1 rows x 2 columns]

        Args:
            search_column:
                The name of the column to search from.
            query (str):
                The search query.
            top_k (int):
                The number of nearest neighbors to return.
            model (TextEmbeddingGenerator):
                A TextEmbeddingGenerator provided by Bigframes ML package.
            score_column (Optional[str], default None):
                The name of the the additional column containning the similarity scores. If None,
                this column won't be attached to the result.

        Returns:
            DataFrame: the DataFrame with the search result.

        Raises:
            ValueError: when the search_column is not found from the the data frame.
            TypeError: when the provided model is not TextEmbeddingGenerator.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        if search_column not in self._df.columns:
            raise ValueError(f"Column `{search_column}` not found")

        self._confirm_operation(len(self._df))

        import bigframes.ml.llm as llm

        if not isinstance(model, llm.TextEmbeddingGenerator):
            raise TypeError(f"Expect a text embedding model, but got: {type(model)}")

        if top_k < 1:
            raise ValueError("top_k must be an integer greater than or equal to 1.")

        embedded_df = model.predict(self._df[search_column])
        embedded_table = embedded_df.reset_index().to_gbq()

        import bigframes.pandas as bpd

        embedding_result_column = "ml_generate_embedding_result"
        query_df = model.predict(bpd.DataFrame({"query_id": [query]})).rename(
            columns={"content": "query_id", embedding_result_column: "embedding"}
        )

        import bigframes.bigquery as bbq

        search_result = (
            bbq.vector_search(
                base_table=embedded_table,
                column_to_search=embedding_result_column,
                query=query_df,
                top_k=top_k,
            )
            .rename(columns={"content": search_column})
            .set_index("index")
        )

        search_result.index.name = self._df.index.name

        if score_column is not None:
            search_result = search_result.rename(columns={"distance": score_column})[
                [search_column, score_column]
            ]
        else:
            search_result = search_result[[search_column]]

        import bigframes.dataframe

        return typing.cast(bigframes.dataframe.DataFrame, search_result)

    def sim_join(
        self,
        other,
        left_on: str,
        right_on: str,
        model,
        top_k: int = 3,
        score_column: Optional[str] = None,
        max_rows: int = 1000,
    ):
        """
        Joins two dataframes based on the similarity of the specified columns.

        This method uses BigQuery's VECTOR_SEARCH function to match rows on the left side with the rows that have
        nearest embedding vectors on the right. In the worst case scenario, the complexity is around O(M * N * log K).
        Therefore, this is a potentially expensive operation.

        ** Examples: **

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.ai_operators = True
            >>> bpd.options.compute.ai_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-005")

            >>> df1 = bpd.DataFrame({'animal': ['monkey', 'spider']})
            >>> df2 = bpd.DataFrame({'animal': ['scorpion', 'baboon']})

            >>> df1.ai.sim_join(df2, left_on='animal', right_on='animal', model=model, top_k=1)
            animal  animal_1
            0  monkey    baboon
            1  spider  scorpion
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            other (DataFrame):
                The other data frame to join with.
            left_on (str):
                The name of the column on left side for the join.
            right_on (str):
                The name of the column on the right side for the join.
            top_k (int, default 3):
                The number of nearest neighbors to return.
            model (TextEmbeddingGenerator):
                A TextEmbeddingGenerator provided by Bigframes ML package.
            score_column (Optional[str], default None):
                The name of the the additional column containning the similarity scores. If None,
                this column won't be attached to the result.
            max_rows:
                The maximum number of rows allowed to be processed per call. If the result is too large, the method
                call will end early with an error.

        Returns:
            DataFrame: the data frame with the join result.

        Raises:
            ValueError: when the amount of data to be processed exceeds the specified max_rows.
        """
        if not options.experiments.ai_operators:
            raise NotImplementedError()

        if left_on not in self._df.columns:
            raise ValueError(f"Left column {left_on} not found")
        if right_on not in self._df.columns:
            raise ValueError(f"Right column {right_on} not found")

        import bigframes.ml.llm as llm

        if not isinstance(model, llm.TextEmbeddingGenerator):
            raise TypeError(f"Expect a text embedding model, but got: {type(model)}")

        joined_table_rows = len(self._df) * len(other)
        if joined_table_rows > max_rows:
            raise ValueError(
                f"Number of rows that need processing is {joined_table_rows}, which exceeds row limit {max_rows}."
            )

        if top_k < 1:
            raise ValueError("top_k must be an integer greater than or equal to 1.")

        work_estimate = len(self._df) * len(other)
        self._confirm_operation(work_estimate)

        base_table_embedding_column = guid.generate_guid()
        base_table = self._attach_embedding(
            other, right_on, base_table_embedding_column, model
        ).to_gbq()
        query_table = self._attach_embedding(self._df, left_on, "embedding", model)

        import bigframes.bigquery as bbq

        join_result = bbq.vector_search(
            base_table=base_table,
            column_to_search=base_table_embedding_column,
            query=query_table,
            top_k=top_k,
        )

        join_result = join_result.drop(
            ["embedding", base_table_embedding_column], axis=1
        )

        if score_column is not None:
            join_result = join_result.rename(columns={"distance": score_column})
        else:
            del join_result["distance"]

        return join_result

    def forecast(
        self,
        timestamp_column: str,
        data_column: str,
        *,
        model: str = "TimesFM 2.0",
        id_columns: Optional[Iterable[str]] = None,
        horizon: int = 10,
        confidence_level: float = 0.95,
    ):
        """
        Forecast time series at future horizon. Using Google Research's open source TimesFM(https://github.com/google-research/timesfm) model.

        .. note::

            This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        Args:
            timestamp_column (str):
                A str value that specified the name of the time points column.
                The time points column provides the time points used to generate the forecast.
                The time points column must use one of the following data types: TIMESTAMP, DATE and DATETIME
            data_column (str):
                A str value that specifies the name of the data column. The data column contains the data to forecast.
                The data column must use one of the following data types: INT64, NUMERIC and FLOAT64
            model (str, default "TimesFM 2.0"):
                A str value that specifies the name of the model. TimesFM 2.0 is the only supported value, and is the default value.
            id_columns (Iterable[str] or None, default None):
                An iterable of str value that specifies the names of one or more ID columns. Each ID identifies a unique time series to forecast.
                Specify one or more values for this argument in order to forecast multiple time series using a single query.
                The columns that you specify must use one of the following data types: STRING, INT64, ARRAY<STRING> and ARRAY<INT64>
            horizon (int, default 10):
                An int value that specifies the number of time points to forecast. The default value is 10. The valid input range is [1, 10,000].
            confidence_level (float, default 0.95):
                A FLOAT64 value that specifies the percentage of the future values that fall in the prediction interval.
                The default value is 0.95. The valid input range is [0, 1).

        Returns:
            DataFrame:
                The forecast dataframe matches that of the BigQuery AI.FORECAST function.
                See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast

        Raises:
            ValueError: when referring to a non-existing column.
        """
        columns = [timestamp_column, data_column]
        if id_columns:
            columns += id_columns
        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column `{column}` not found")

        options: dict[str, Union[int, float, str, Iterable[str]]] = {
            "data_col": data_column,
            "timestamp_col": timestamp_column,
            "model": model,
            "horizon": horizon,
            "confidence_level": confidence_level,
        }
        if id_columns:
            options["id_cols"] = id_columns

        return self._base_bqml.ai_forecast(input_data=self._df, options=options)

    @staticmethod
    def _attach_embedding(dataframe, source_column: str, embedding_column: str, model):
        result_df = dataframe.copy()
        embeddings = model.predict(dataframe[source_column])[
            "ml_generate_embedding_result"
        ]
        result_df[embedding_column] = embeddings
        return result_df

    @staticmethod
    def _make_multimodel_prompt(
        prompt_df, columns, user_instruction: str, output_instruction: str
    ):
        prompt = [f"{output_instruction}\n{user_instruction}\nContext: "]
        for col in columns:
            prompt.extend([f"{col} is ", prompt_df[col]])

        return prompt

    @staticmethod
    def _make_text_prompt(
        prompt_df, columns, user_instruction: str, output_instruction: str
    ):
        prompt_df["prompt"] = f"{output_instruction}\n{user_instruction}\nContext: "

        # Combine context from multiple columns.
        for col in columns:
            prompt_df["prompt"] += f"{col} is `" + prompt_df[col] + "`\n"

        return prompt_df["prompt"]

    @staticmethod
    def _parse_columns(instruction: str) -> List[str]:
        """Extracts column names enclosed in curly braces from the user instruction.
        For example, _parse_columns("{city} is in {continent}") == ["city", "continent"]
        """
        columns = re.findall(r"(?<!{)\{(?!{)(.*?)\}(?!\})", instruction)

        if not columns:
            raise ValueError("No column references.")

        return columns

    @staticmethod
    def _format_instruction(instruction: str, columns: List[str]) -> str:
        """Extracts column names enclosed in curly braces from the user instruction.
        For example, `_format_instruction(["city", "continent"], "{city} is in {continent}")
         == "city is in continent"`
        """
        return instruction.format(**{col: col for col in columns})

    @staticmethod
    def _validate_model(model):
        from bigframes.ml.llm import GeminiTextGenerator

        if not isinstance(model, GeminiTextGenerator):
            raise TypeError("Model is not GeminiText Generator")

    @staticmethod
    def _confirm_operation(row_count: int):
        """Raises OperationAbortedError when the confirmation fails"""
        import bigframes  # Import in the function body to avoid circular imports.

        threshold = bigframes.options.compute.ai_ops_confirmation_threshold

        if threshold is None or row_count <= threshold:
            return

        if bigframes.options.compute.ai_ops_threshold_autofail:
            raise exceptions.OperationAbortedError(
                f"Operation was cancelled because your work estimate is {row_count} rows, which exceeds the threshold {threshold} rows."
            )

        # Separate the prompt out. In IDE such VS Code, leaving prompt in the
        # input function makes it less visible to the end user.
        print(f"This operation will process about {row_count} rows.")
        print(
            "You can raise the confirmation threshold by setting `bigframes.options.compute.ai_ops_confirmation_threshold` to a higher value. To completely turn off the confirmation check, set the threshold to `None`."
        )
        print("Proceed? [Y/n]")
        reply = input().casefold()
        if reply not in {"y", "yes", ""}:
            raise exceptions.OperationAbortedError("Operation was cancelled.")
