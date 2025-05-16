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
import warnings

import numpy as np

from bigframes import dtypes, exceptions
from bigframes.core import guid, log_adapter


@log_adapter.class_logger
class Semantics:
    def __init__(self, df) -> None:
        import bigframes  # Import in the function body to avoid circular imports.
        import bigframes.dataframe

        if not bigframes.options.experiments.semantic_operators:
            raise NotImplementedError()

        self._df: bigframes.dataframe.DataFrame = df

    def agg(
        self,
        instruction: str,
        model,
        cluster_column: typing.Optional[str] = None,
        max_agg_rows: int = 10,
        ground_with_google_search: bool = False,
    ):
        """
        Performs an aggregation over all rows of the table.

        This method recursively aggregates the input data to produce partial answers
        in parallel, until a single answer remains.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001") # doctest: +SKIP

            >>> df = bpd.DataFrame(
            ... {
            ...     "Movies": [
            ...         "Titanic",
            ...         "The Wolf of Wall Street",
            ...         "Inception",
            ...     ],
            ...     "Year": [1997, 2013, 2010],
            ... })
            >>> df.semantics.agg( # doctest: +SKIP
            ...     "Find the first name shared by all actors in {Movies}. One word answer.",
            ...     model=model,
            ... )
            0    Leonardo
            <BLANKLINE>
            Name: Movies, dtype: string

        Args:
            instruction (str):
                An instruction on how to map the data. This value must contain
                column references by name enclosed in braces.
                For example, to reference a column named "movies", use "{movies}" in the
                instruction, like: "Find actor names shared by all {movies}."

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by the Bigframes ML package.

            cluster_column (Optional[str], default None):
                If set, aggregates each cluster before performing aggregations across
                clusters. Clustering based on semantic similarity can improve accuracy
                of the sementic aggregations.

            max_agg_rows (int, default 10):
                The maxinum number of rows to be aggregated at a time.

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.dataframe.DataFrame: A new DataFrame with the aggregated answers.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when
                more than one columns are referred to.
        """
        import bigframes.bigquery as bbq
        import bigframes.dataframe
        import bigframes.series

        self._validate_model(model)
        columns = self._parse_columns(instruction)

        if max_agg_rows <= 1:
            raise ValueError(
                f"Invalid value for `max_agg_rows`: {max_agg_rows}."
                "It must be greater than 1."
            )

        work_estimate = len(self._df) * int(max_agg_rows / (max_agg_rows - 1))
        self._confirm_operation(work_estimate)

        df: bigframes.dataframe.DataFrame = self._df.copy()
        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column {column} not found.")

            if df[column].dtype != dtypes.STRING_DTYPE:
                df[column] = df[column].astype(dtypes.STRING_DTYPE)

        if len(columns) > 1:
            raise NotImplementedError(
                "Semantic aggregations are limited to a single column."
            )
        column = columns[0]

        if ground_with_google_search:
            msg = exceptions.format_message(
                "Enables Grounding with Google Search may impact billing cost. See pricing "
                "details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models"
            )
            warnings.warn(msg, category=UserWarning)

        user_instruction = self._format_instruction(instruction, columns)

        num_cluster = 1
        if cluster_column is not None:
            if cluster_column not in df.columns:
                raise ValueError(f"Cluster column `{cluster_column}` not found.")

            if df[cluster_column].dtype != dtypes.INT_DTYPE:
                raise TypeError(
                    "Cluster column must be an integer type, not "
                    f"{type(df[cluster_column])}"
                )

            num_cluster = df[cluster_column].unique().shape[0]
            df = df.sort_values(cluster_column)
        else:
            cluster_column = guid.generate_guid("pid")
            df[cluster_column] = 0

        aggregation_group_id = guid.generate_guid("agg")
        group_row_index = guid.generate_guid("gid")
        llm_prompt = guid.generate_guid("prompt")
        df = (
            df.reset_index(drop=True)
            .reset_index()
            .rename(columns={"index": aggregation_group_id})
        )

        output_instruction = (
            "Answer user instructions using the provided context from various sources. "
            "Combine all relevant information into a single, concise, well-structured response. "
            f"Instruction: {user_instruction}.\n\n"
        )

        while len(df) > 1:
            df[group_row_index] = (df[aggregation_group_id] % max_agg_rows + 1).astype(
                dtypes.STRING_DTYPE
            )
            df[aggregation_group_id] = (df[aggregation_group_id] / max_agg_rows).astype(
                dtypes.INT_DTYPE
            )
            df[llm_prompt] = "\t\nSource #" + df[group_row_index] + ": " + df[column]

            if len(df) > num_cluster:
                # Aggregate within each partition
                agg_df = bbq.array_agg(
                    df.groupby(by=[cluster_column, aggregation_group_id])
                )
            else:
                # Aggregate cross partitions
                agg_df = bbq.array_agg(df.groupby(by=[aggregation_group_id]))
                agg_df[cluster_column] = agg_df[cluster_column].list[0]

            # Skip if the aggregated group only has a single item
            single_row_df: bigframes.series.Series = bbq.array_to_string(
                agg_df[agg_df[group_row_index].list.len() <= 1][column],
                delimiter="",
            )
            prompt_s: bigframes.series.Series = bbq.array_to_string(
                agg_df[agg_df[group_row_index].list.len() > 1][llm_prompt],
                delimiter="",
            )
            prompt_s = output_instruction + prompt_s  # type:ignore

            # Run model
            predict_df = typing.cast(
                bigframes.dataframe.DataFrame,
                model.predict(
                    prompt_s,
                    temperature=0.0,
                    ground_with_google_search=ground_with_google_search,
                ),
            )
            agg_df[column] = predict_df["ml_generate_text_llm_result"].combine_first(
                single_row_df
            )

            agg_df = agg_df.reset_index()
            df = agg_df[[aggregation_group_id, cluster_column, column]]

        return df[column]

    def cluster_by(
        self,
        column: str,
        output_column: str,
        model,
        n_clusters: int = 5,
    ):
        """
        Clusters data based on the semantic similarity of text within a specified column.

        This method leverages a language model to generate text embeddings for each value in
        the given column. These embeddings capture the semantic meaning of the text.
        The data is then grouped into `n` clusters using the k-means clustering algorithm,
        which groups data points based on the similarity of their embeddings.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-005")

            >>> df = bpd.DataFrame({
            ...     "Product": ["Smartphone", "Laptop", "T-shirt", "Jeans"],
            ... })
            >>> df.semantics.cluster_by("Product", "Cluster ID", model, n_clusters=2) # doctest: +SKIP
                    Product  Cluster ID
            0    Smartphone           2
            1        Laptop           2
            2       T-shirt           1
            3         Jeans           1
            <BLANKLINE>
            [4 rows x 2 columns]

        Args:
            column (str):
                An column name to perform the similarity clustering.

            output_column (str):
                An output column to store the clustering ID.

            model (bigframes.ml.llm.TextEmbeddingGenerator):
                A TextEmbeddingGenerator provided by Bigframes ML package.

            n_clusters (int, default 5):
                Default 5. Number of clusters to be detected.

        Returns:
            bigframes.dataframe.DataFrame: A new DataFrame with the clustering output column.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the column refers to a non-existing column.
        """

        import bigframes.dataframe
        import bigframes.ml.cluster as cluster
        import bigframes.ml.llm as llm

        if not isinstance(model, llm.TextEmbeddingGenerator):
            raise TypeError(f"Expect a text embedding model, but got: {type(model)}")

        if column not in self._df.columns:
            raise ValueError(f"Column {column} not found.")

        if n_clusters <= 1:
            raise ValueError(
                f"Invalid value for `n_clusters`: {n_clusters}."
                "It must be greater than 1."
            )

        self._confirm_operation(len(self._df))

        df: bigframes.dataframe.DataFrame = self._df.copy()
        embeddings_df = model.predict(df[column])

        cluster_model = cluster.KMeans(n_clusters=n_clusters)
        cluster_model.fit(embeddings_df[["ml_generate_embedding_result"]])
        clustered_result = cluster_model.predict(embeddings_df)
        df[output_column] = clustered_result["CENTROID_ID"]
        return df

    def filter(self, instruction: str, model, ground_with_google_search: bool = False):
        """
        Filters the DataFrame with the semantics of the user instruction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001") # doctest: +SKIP

            >>> df = bpd.DataFrame({"country": ["USA", "Germany"], "city": ["Seattle", "Berlin"]})
            >>> df.semantics.filter("{city} is the capital of {country}", model) # doctest: +SKIP
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
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
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
        output_instruction = "Based on the provided context, reply to the following claim by only True or False:"

        if has_blob_column:
            results = typing.cast(
                bigframes.dataframe.DataFrame,
                model.predict(
                    df,
                    prompt=self._make_multimodel_prompt(
                        df, columns, user_instruction, output_instruction
                    ),
                    temperature=0.0,
                    ground_with_google_search=ground_with_google_search,
                ),
            )
        else:
            results = typing.cast(
                bigframes.dataframe.DataFrame,
                model.predict(
                    self._make_text_prompt(
                        df, columns, user_instruction, output_instruction
                    ),
                    temperature=0.0,
                    ground_with_google_search=ground_with_google_search,
                ),
            )

        return self._df[
            results["ml_generate_text_llm_result"].str.lower().str.contains("true")
        ]

    def map(
        self,
        instruction: str,
        output_column: str,
        model,
        ground_with_google_search: bool = False,
    ):
        """
        Maps the DataFrame with the semantics of the user instruction.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001") # doctest: +SKIP

            >>> df = bpd.DataFrame({"ingredient_1": ["Burger Bun", "Soy Bean"], "ingredient_2": ["Beef Patty", "Bittern"]})
            >>> df.semantics.map("What is the food made from {ingredient_1} and {ingredient_2}? One word only.", output_column="food", model=model) # doctest: +SKIP
              ingredient_1 ingredient_2      food
            0   Burger Bun   Beef Patty  Burger
            <BLANKLINE>
            1     Soy Bean      Bittern    Tofu
            <BLANKLINE>
            <BLANKLINE>
            [2 rows x 3 columns]

        Args:
            instruction (str):
                An instruction on how to map the data. This value must contain
                column references by name, which should be wrapped in a pair of braces.
                For example, if you have a column "food", you can refer to this column
                in the instructions like:
                "Get the ingredients of {food}."

            output_column (str):
                The column name of the mapping result.

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
            bigframes.pandas.DataFrame: DataFrame with attached mapping results.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
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
                )["ml_generate_text_llm_result"],
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
                )["ml_generate_text_llm_result"],
            )

        from bigframes.core.reshape.api import concat

        return concat([self._df, results.rename(output_column)], axis=1)

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
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001") # doctest: +SKIP

            >>> cities = bpd.DataFrame({'city': ['Seattle', 'Ottawa', 'Berlin', 'Shanghai', 'New Delhi']})
            >>> continents = bpd.DataFrame({'continent': ['North America', 'Africa', 'Asia']})

            >>> cities.semantics.join(continents, "{city} is in {continent}", model) # doctest: +SKIP
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

            max_rows (int, default 1000):
                The maximum number of rows allowed to be sent to the model per call. If the result is too large, the method
                call will end early with an error.

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

        return joined_df.semantics.filter(
            instruction, model, ground_with_google_search=ground_with_google_search
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
        Performs semantic search on the DataFrame.

        ** Examples: **

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> import bigframes
            >>> bigframes.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-005") # doctest: +SKIP

            >>> df = bpd.DataFrame({"creatures": ["salmon", "sea urchin", "frog", "chimpanzee"]})
            >>> df.semantics.search("creatures", "monkey", top_k=1, model=model, score_column='distance') # doctest: +SKIP
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

    def top_k(
        self,
        instruction: str,
        model,
        k: int = 10,
        ground_with_google_search: bool = False,
    ):
        """
        Ranks each tuple and returns the k best according to the instruction.

        This method employs a quick select algorithm to efficiently compare the pivot
        with all other items. By leveraging an LLM (Large Language Model), it then
        identifies the top 'k' best answers from these comparisons.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001") # doctest: +SKIP

            >>> df = bpd.DataFrame(
            ... {
            ...     "Animals": ["Dog", "Bird", "Cat", "Horse"],
            ...     "Sounds": ["Woof", "Chirp", "Meow", "Neigh"],
            ... })
            >>> df.semantics.top_k("{Animals} are more popular as pets", model=model, k=2) # doctest: +SKIP
              Animals Sounds
            0     Dog   Woof
            2     Cat   Meow
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            instruction (str):
                An instruction on how to map the data. This value must contain
                column references by name enclosed in braces.
                For example, to reference a column named "Animals", use "{Animals}" in the
                instruction, like: "{Animals} are more popular as pets"

            model (bigframes.ml.llm.GeminiTextGenerator):
                A GeminiTextGenerator provided by the Bigframes ML package.

            k (int, default 10):
                The number of rows to return.

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the GeminiTextGenerator model.
                When set to True, the model incorporates relevant information from Google
                Search results into its responses, enhancing their accuracy and factualness.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

        Returns:
            bigframes.dataframe.DataFrame: A new DataFrame with the top k rows.

        Raises:
            NotImplementedError: when the semantic operator experiment is off.
            ValueError: when the instruction refers to a non-existing column, or when no
                columns are referred to.
        """
        import bigframes.dataframe
        import bigframes.series

        self._validate_model(model)
        columns = self._parse_columns(instruction)
        for column in columns:
            if column not in self._df.columns:
                raise ValueError(f"Column {column} not found.")
        if len(columns) > 1:
            raise NotImplementedError("Semantic top K are limited to a single column.")

        if ground_with_google_search:
            msg = exceptions.format_message(
                "Enables Grounding with Google Search may impact billing cost. See pricing "
                "details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models"
            )
            warnings.warn(msg, category=UserWarning)

        work_estimate = int(len(self._df) * (len(self._df) - 1) / 2)
        self._confirm_operation(work_estimate)

        df: bigframes.dataframe.DataFrame = self._df[columns].copy()
        column = columns[0]
        if df[column].dtype != dtypes.STRING_DTYPE:
            df[column] = df[column].astype(dtypes.STRING_DTYPE)

        # `index` is reserved for the `reset_index` below.
        if column == "index":
            raise ValueError(
                "Column name 'index' is reserved. Please choose a different name."
            )

        if k < 1:
            raise ValueError("k must be an integer greater than or equal to 1.")

        user_instruction = self._format_instruction(instruction, columns)

        n = df.shape[0]
        if k >= n:
            return df

        # Create a unique index and duplicate it as the "index" column. This workaround
        # is needed for the select search algorithm due to unimplemented bigFrame methods.
        df = df.reset_index().rename(columns={"index": "old_index"}).reset_index()

        # Initialize a status column to track the selection status of each item.
        #  - None: Unknown/not yet processed
        #  - 1.0: Selected as part of the top-k items
        #  - -1.0: Excluded from the top-k items
        status_column = guid.generate_guid("status")
        df[status_column] = bigframes.series.Series(
            None, dtype=dtypes.FLOAT_DTYPE, session=df._session
        )

        num_selected = 0
        while num_selected < k:
            df, num_new_selected = self._topk_partition(
                df,
                column,
                status_column,
                user_instruction,
                model,
                k - num_selected,
                ground_with_google_search,
            )
            num_selected += num_new_selected

        result_df: bigframes.dataframe.DataFrame = self._df.copy()
        return result_df[df.set_index("old_index")[status_column] > 0.0]

    @staticmethod
    def _topk_partition(
        df,
        column: str,
        status_column: str,
        user_instruction: str,
        model,
        k: int,
        ground_with_google_search: bool,
    ):
        output_instruction = (
            "Given a question and two documents, choose the document that best answers "
            "the question. Respond with 'Document 1' or 'Document 2'.  You must choose "
            "one, even if neither is ideal. "
        )

        # Random pivot selection for improved average quickselect performance.
        pending_df = df[df[status_column].isna()]
        pivot_iloc = np.random.randint(0, pending_df.shape[0])
        pivot_index = pending_df.iloc[pivot_iloc]["index"]
        pivot_df = pending_df[pending_df["index"] == pivot_index]

        # Build a prompt to compare the pivot item's relevance to other pending items.
        prompt_s = pending_df[pending_df["index"] != pivot_index][column]
        prompt_s = (
            f"{output_instruction}\n\nQuestion: {user_instruction}\n"
            + f"\nDocument 1: {column} "
            + pivot_df.iloc[0][column]
            + f"\nDocument 2: {column} "
            + prompt_s  # type:ignore
        )

        import bigframes.dataframe

        predict_df = typing.cast(
            bigframes.dataframe.DataFrame,
            model.predict(
                prompt_s,
                temperature=0.0,
                ground_with_google_search=ground_with_google_search,
            ),
        )

        marks = predict_df["ml_generate_text_llm_result"].str.contains("2")
        more_relavant: bigframes.dataframe.DataFrame = df[marks]
        less_relavent: bigframes.dataframe.DataFrame = df[~marks]

        num_more_relavant = more_relavant.shape[0]
        if k < num_more_relavant:
            less_relavent[status_column] = -1.0
            pivot_df[status_column] = -1.0
            df = df.combine_first(less_relavent).combine_first(pivot_df)
            return df, 0
        else:  # k >= num_more_relavant
            more_relavant[status_column] = 1.0
            df = df.combine_first(more_relavant)
            if k >= num_more_relavant + 1:
                pivot_df[status_column] = 1.0
                df = df.combine_first(pivot_df)
                return df, num_more_relavant + 1
            else:
                return df, num_more_relavant

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
            >>> bpd.options.experiments.semantic_operators = True
            >>> bpd.options.compute.semantic_ops_confirmation_threshold = 25

            >>> import bigframes.ml.llm as llm
            >>> model = llm.TextEmbeddingGenerator(model_name="text-embedding-005") # doctest: +SKIP

            >>> df1 = bpd.DataFrame({'animal': ['monkey', 'spider']})
            >>> df2 = bpd.DataFrame({'animal': ['scorpion', 'baboon']})

            >>> df1.semantics.sim_join(df2, left_on='animal', right_on='animal', model=model, top_k=1) # doctest: +SKIP
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

        threshold = bigframes.options.compute.semantic_ops_confirmation_threshold

        if threshold is None or row_count <= threshold:
            return

        if bigframes.options.compute.semantic_ops_threshold_autofail:
            raise exceptions.OperationAbortedError(
                f"Operation was cancelled because your work estimate is {row_count} rows, which exceeds the threshold {threshold} rows."
            )

        # Separate the prompt out. In IDE such VS Code, leaving prompt in the
        # input function makes it less visible to the end user.
        print(f"This operation will process about {row_count} rows.")
        print(
            "You can raise the confirmation threshold by setting `bigframes.options.compute.semantic_ops_confirmation_threshold` to a higher value. To completely turn off the confirmation check, set the threshold to `None`."
        )
        print("Proceed? [Y/n]")
        reply = input().casefold()
        if reply not in {"y", "yes", ""}:
            raise exceptions.OperationAbortedError("Operation was cancelled.")
