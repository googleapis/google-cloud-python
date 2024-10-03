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

        Args:
            instruction:
                An instruction on how to filter the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "The {food} is healthy."

            model:
                A LLM model provided by Bigframes ML package.

        Returns:
            DataFrame filtered by the instruction.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """

        # Validate column references
        columns = re.findall(r"(?<!{)\{(?!{)(.*?)\}(?!\})", instruction)

        if not columns:
            raise ValueError("No column references.")

        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column {column} not found.")

        # Replace column references with names.
        instruction = instruction.format(**{col: col for col in columns})

        prompt_df = self._df.copy()

        # Combine context from multiple columns.
        for idx, col in enumerate(columns):
            if idx == 0:
                prompt_df["context"] = f"{col} is `" + prompt_df[col] + "`\n"
            else:
                prompt_df["context"] += f"{col} is `" + prompt_df[col] + "`\n"

        prompt_df["prompt"] = (
            "Decide the folowing claim by only True and False: "
            + instruction
            + "\nContext:"
            + prompt_df["context"]
        )

        import bigframes.dataframe

        results = typing.cast(
            bigframes.dataframe.DataFrame, model.predict(prompt_df["prompt"])
        )

        return self._df[
            results["ml_generate_text_llm_result"].str.lower().str.contains("true")
        ]
