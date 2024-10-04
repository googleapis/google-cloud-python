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
            >>> df.semantics.map("What is the food made from {ingredient_1} and {ingredient_2}? One word only.", result_column_name="food", model=model)
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
        # Validate column references
        columns = re.findall(r"(?<!{)\{(?!{)(.*?)\}(?!\})", user_instruction)

        if not columns:
            raise ValueError("No column references.")

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


def _validate_model(model):
    from bigframes.ml.llm import GeminiTextGenerator

    if not isinstance(model, GeminiTextGenerator):
        raise ValueError("Model is not GeminiText Generator")
