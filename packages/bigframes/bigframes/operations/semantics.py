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


import re
import typing
from typing import List, Optional

import bigframes


class Semantics:
    def __init__(self, df) -> None:
        if not bigframes.options.experiments.semantic_operators:
            raise NotImplementedError()

        self._df = df

    def filter(self, instruction: str, model):
        """
        Filters the DataFrame with the semantics of the user instruction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.semantic_operators = True

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-1.5-flash-001")

            >>> df = bpd.DataFrame({"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]})
            >>> df.semantics.filter("{city} is the capital of {country}", model)
               country    city
            1  Germany  Berlin
            <BLANKLINE>
            [1 rows x 2 columns]

        Args:
            instruction:
                An instruction on how to filter the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "The {food} is healthy."

            model:
                A GeminiTextGenerator provided by Bigframes ML package.

        Returns:
            DataFrame filtered by the instruction.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
        _validate_model(model)

        output_instruction = "Based on the provided context, reply to the following claim by only True or False:"

        from bigframes.dataframe import DataFrame

        results = typing.cast(
            DataFrame, model.predict(self._make_prompt(instruction, output_instruction))
        )

        return self._df[
            results["ml_generate_text_llm_result"].str.lower().str.contains("true")
        ]

    def map(self, instruction: str, output_column: str, model):
        """
        Maps the DataFrame with the semantics of the user instruction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.semantic_operators = True

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-1.5-flash-001")

            >>> df = bpd.DataFrame({"ingredient_1": ["Burger Bun", "Soy Bean"], "ingredient_2": ["Beef Patty", "Bittern"]})
            >>> df.semantics.map("What is the food made from {ingredient_1} and {ingredient_2}? One word only.", output_column="food", model=model)
              ingredient_1 ingredient_2      food
            0   Burger Bun   Beef Patty  Burger
            <BLANKLINE>
            1     Soy Bean      Bittern    Tofu
            <BLANKLINE>
            <BLANKLINE>
            [2 rows x 3 columns]

        Args:
            instruction:
                An instruction on how to map the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "Get the ingredients of {food}."

            result_column_name:
                The column name of the mapping result.

            model:
                A GeminiTextGenerator provided by Bigframes ML package.

        Returns:
            DataFrame with attached mapping results.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
        _validate_model(model)

        output_instruction = (
            "Based on the provided contenxt, answer the following instruction:"
        )

        from bigframes.series import Series

        results = typing.cast(
            Series,
            model.predict(self._make_prompt(instruction, output_instruction))[
                "ml_generate_text_llm_result"
            ],
        )

        from bigframes.core.reshape import concat

        return concat([self._df, results.rename(output_column)], axis=1)

    def _make_prompt(self, user_instruction: str, output_instruction: str):
        columns = _parse_columns(user_instruction)

        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column {column} not found.")

        # Replace column references with names.
        user_instruction = user_instruction.format(**{col: col for col in columns})

        prompt_df = self._df[columns].copy()
        prompt_df["prompt"] = f"{output_instruction}\n{user_instruction}\nContext: "

        # Combine context from multiple columns.
        for col in columns:
            prompt_df["prompt"] += f"{col} is `" + prompt_df[col] + "`\n"

        return prompt_df["prompt"]

    def join(self, other, instruction: str, model, max_rows: int = 1000):
        """
        Joines two dataframes by applying the instruction over each pair of rows from
        the left and right table.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.semantic_operators = True

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-1.5-flash-001")

            >>> cities = bpd.DataFrame({'city': ['Seattle', 'Ottawa', 'Berlin', 'Shanghai', 'New Delhi']})
            >>> continents = bpd.DataFrame({'continent': ['North America', 'Africa', 'Asia']})

            >>> cities.semantics.join(continents, "{city} is in {continent}", model)
                    city      continent
            0    Seattle  North America
            1     Ottawa  North America
            2   Shanghai           Asia
            3  New Delhi           Asia
            <BLANKLINE>
            [4 rows x 2 columns]

        Args:
            other:
                The other dataframe.

            instruction:
                An instruction on how left and right rows can be joined. This value must contain
                column references by name. which should be wrapped in a pair of braces.
                For example: "The {city} belongs to the {country}".
                For column names that are shared between two dataframes, you need to add "_left"
                and "_right" suffix for differentiation. This is especially important when you do
                self joins. For example: "The {employee_name_left} reports to {employee_name_right}"
                You must not add "_left" or "_right" suffix to non-overlapping columns.

            model:
                A GeminiTextGenerator provided by Bigframes ML package.

            max_rows:
                The maximum number of rows allowed to be sent to the model per call. If the result is too large, the method
                call will end early with an error.

        Returns:
            The joined dataframe.

        Raises:
            ValueError if the amount of data that will be sent for LLM processing is larger than max_rows.
        """
        _validate_model(model)

        joined_table_rows = len(self._df) * len(other)

        if joined_table_rows > max_rows:
            raise ValueError(
                f"Number of rows that need processing is {joined_table_rows}, which exceeds row limit {max_rows}."
            )

        columns = _parse_columns(instruction)

        left_columns = []
        right_columns = []

        for col in columns:
            if col in self._df.columns and col in other.columns:
                raise ValueError(f"Ambiguous column reference: {col}")

            elif col in self._df.columns:
                left_columns.append(col)

            elif col in other.columns:
                right_columns.append(col)

            elif col.endswith("_left"):
                original_col_name = col[: -len("_left")]
                if (
                    original_col_name in self._df.columns
                    and original_col_name in other.columns
                ):
                    left_columns.append(col)
                elif original_col_name in self._df.columns:
                    raise ValueError(f"Unnecessary suffix for {col}")
                else:
                    raise ValueError(f"Column {col} not found")

            elif col.endswith("_right"):
                original_col_name = col[: -len("_right")]
                if (
                    original_col_name in self._df.columns
                    and original_col_name in other.columns
                ):
                    right_columns.append(col)
                elif original_col_name in other.columns:
                    raise ValueError(f"Unnecessary suffix for {col}")
                else:
                    raise ValueError(f"Column {col} not found")

            else:
                raise ValueError(f"Column {col} not found")

        if not left_columns or not right_columns:
            raise ValueError()

        joined_df = self._df.merge(other, how="cross", suffixes=("_left", "_right"))

        return joined_df.semantics.filter(instruction, model).reset_index(drop=True)

    def search(
        self,
        search_column: str,
        query: str,
        top_k: int,
        model,
        score_column: Optional[str] = None,
    ):
        """
        Performs semantic search on the DataFrame.

        ** Examples: **

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.semantic_operators = True

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-004")

            >>> df = bpd.DataFrame({"creatures": ["salmon", "sea urchin", "frog", "chimpanzee"]})
            >>> df.semantics.search("creatures", "monkey", top_k=1, model=model, score_column='distance')
                creatures  distance
            3  chimpanzee  0.781101
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

        if search_column not in self._df.columns:
            raise ValueError(f"Column {search_column} not found")

        import bigframes.ml.llm as llm

        if not isinstance(model, llm.TextEmbeddingGenerator):
            raise TypeError(f"Expect a text embedding model, but got: {type(model)}")

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


def _validate_model(model):
    from bigframes.ml.llm import GeminiTextGenerator

    if not isinstance(model, GeminiTextGenerator):
        raise ValueError("Model is not GeminiText Generator")


def _parse_columns(instruction: str) -> List[str]:
    columns = re.findall(r"(?<!{)\{(?!{)(.*?)\}(?!\})", instruction)

    if not columns:
        raise ValueError("No column references")

    return columns
