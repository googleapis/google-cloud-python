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
from typing import Optional


@dataclasses.dataclass
class ComputeOptions:
    """
    Encapsulates configuration for compute options.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

        >>> bpd.options.compute.maximum_bytes_billed = 500
        >>> # df.to_pandas() # this should fail
        google.api_core.exceptions.InternalServerError: 500 Query exceeded limit for bytes billed: 500. 10485760 or higher required.

        >>> bpd.options.compute.maximum_bytes_billed = None  # reset option

    Attributes:
        maximum_bytes_billed (int, Options):
            Limits the bytes billed for query jobs. Queries that will have
            bytes billed beyond this limit will fail (without incurring a
            charge). If unspecified, this will be set to your project default.
            See `maximum_bytes_billed <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig#google_cloud_bigquery_job_QueryJobConfig_maximum_bytes_billed>`_.
        enable_multi_query_execution (bool, Options):
            If enabled, large queries may be factored into multiple smaller queries
            in order to avoid generating queries that are too complex for the query
            engine to handle. However this comes at the cost of increase cost and latency.
    """

    maximum_bytes_billed: Optional[int] = None
    enable_multi_query_execution: bool = False
