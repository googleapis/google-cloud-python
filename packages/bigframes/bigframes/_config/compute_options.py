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

"""Options for displaying objects."""

import dataclasses
from typing import Any, Dict, Optional


@dataclasses.dataclass
class ComputeOptions:
    """
    Encapsulates the configuration for compute options.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

        >>> bpd.options.compute.maximum_bytes_billed = 500
        >>> # df.to_pandas() # this should fail
        google.api_core.exceptions.InternalServerError: 500 Query exceeded limit for bytes billed: 500. 10485760 or higher required.

        >>> bpd.options.compute.maximum_bytes_billed = None  # reset option

    To add multiple extra labels to a query configuration, use the `assign_extra_query_labels`
    method with keyword arguments:

        >>> bpd.options.compute.assign_extra_query_labels(test1=1, test2="abc")
        >>> bpd.options.compute.extra_query_labels
        {'test1': 1, 'test2': 'abc'}

    Alternatively, you can add labels individually by directly accessing the `extra_query_labels`
    dictionary:

        >>> bpd.options.compute.extra_query_labels["test3"] = False
        >>> bpd.options.compute.extra_query_labels
        {'test1': 1, 'test2': 'abc', 'test3': False}

    To remove a label from the configuration, use the `del` keyword on the desired label key:

        >>> del bpd.options.compute.extra_query_labels["test1"]
        >>> bpd.options.compute.extra_query_labels
        {'test2': 'abc', 'test3': False}

    Attributes:
        ai_ops_confirmation_threshold (int | None):
            Guards against unexpected processing of large amount of rows by semantic operators.
            If the number of rows exceeds the threshold, the user will be asked to confirm
            their operations to resume. The default value is 0. Set the value to None
            to turn off the guard.

        ai_ops_threshold_autofail (bool):
            Guards against unexpected processing of large amount of rows by semantic operators.
            When set to True, the operation automatically fails without asking for user inputs.

        allow_large_results (bool | None):
            Specifies whether query results can exceed 10 GB. Defaults to False. Setting this
            to False (the default) restricts results to 10 GB for potentially faster execution;
            BigQuery will raise an error if this limit is exceeded. Setting to True removes
            this result size limit.

        enable_multi_query_execution (bool | None):
            If enabled, large queries may be factored into multiple smaller queries
            in order to avoid generating queries that are too complex for the query
            engine to handle. However this comes at the cost of increase cost and latency.

        extra_query_labels (Dict[str, Any] | None):
            Stores additional custom labels for query configuration.

        maximum_bytes_billed (int | None):
            Limits the bytes billed for query jobs. Queries that will have
            bytes billed beyond this limit will fail (without incurring a
            charge). If unspecified, this will be set to your project default.
            See `maximum_bytes_billed`: https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig#google_cloud_bigquery_job_QueryJobConfig_maximum_bytes_billed.

        maximum_result_rows (int | None):
            Limits the number of rows in an execution result. When converting
            a BigQuery DataFrames object to a pandas DataFrame or Series (e.g.,
            using ``.to_pandas()``, ``.peek()``, ``.__repr__()``, direct
            iteration), the data is downloaded from BigQuery to the client
            machine. This option restricts the number of rows that can be
            downloaded.  If the number of rows to be downloaded exceeds this
            limit, a ``bigframes.exceptions.MaximumResultRowsExceeded``
            exception is raised.

        semantic_ops_confirmation_threshold (int | None):
            .. deprecated:: 1.42.0
                Semantic operators are deprecated. Please use AI operators instead

        semantic_ops_threshold_autofail (bool):
            .. deprecated:: 1.42.0
                Semantic operators are deprecated. Please use AI operators instead
    """

    ai_ops_confirmation_threshold: Optional[int] = 0
    ai_ops_threshold_autofail: bool = False
    allow_large_results: Optional[bool] = None
    enable_multi_query_execution: bool = False
    extra_query_labels: Dict[str, Any] = dataclasses.field(
        default_factory=dict, init=False
    )
    maximum_bytes_billed: Optional[int] = None
    maximum_result_rows: Optional[int] = None
    semantic_ops_confirmation_threshold: Optional[int] = 0
    semantic_ops_threshold_autofail = False

    def assign_extra_query_labels(self, **kwargs: Any) -> None:
        """
        Assigns additional custom labels for query configuration. The method updates the
        `extra_query_labels` dictionary with new labels provided through keyword arguments.

        Args:
            kwargs (Any):
                Custom labels provided as keyword arguments. Each key-value pair
                in `kwargs` represents a label name and its value.

        Raises:
            ValueError: If a key matches one of the reserved attribute names,
                specifically 'maximum_bytes_billed' or 'enable_multi_query_execution',
                to prevent conflicts with built-in settings.
        """
        reserved_keys = ["maximum_bytes_billed", "enable_multi_query_execution"]
        for key in kwargs:
            if key in reserved_keys:
                raise ValueError(
                    f"'{key}' is a reserved attribute name. Please use "
                    "a different key for your custom labels to avoid "
                    "conflicts with built-in settings."
                )

        self.extra_query_labels.update(kwargs)
