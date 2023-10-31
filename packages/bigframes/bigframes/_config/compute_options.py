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

    Attributes:
        maximum_bytes_billed (int, Options):
            Limits the bytes billed for query jobs. Queries that will have
            bytes billed beyond this limit will fail (without incurring a
            charge). If unspecified, this will be set to your project default.
            See `maximum_bytes_billed <https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig#google_cloud_bigquery_job_QueryJobConfig_maximum_bytes_billed>`_.

    """

    maximum_bytes_billed: Optional[int] = None
