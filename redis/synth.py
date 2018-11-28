# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
excludes = ["README.rst", "setup.py", "nox*.py", "docs/conf.py", "docs/index.rst"]

# ----------------------------------------------------------------------------
# Generate redis GAPIC layer
# ----------------------------------------------------------------------------
for version in ["v1beta1", "v1"]:
    library = gapic.py_library(
        "redis", version, config_path=f"artman_redis_{version}.yaml"
    )

    s.copy(library, excludes=excludes)

# Fix docstrings
s.replace(
    "google/cloud/**/cloud_redis_client.py",
    r"resources of the form:\n      ``",
    r"resources of the form:\n\n      ``",
)

s.replace(
    "google/cloud/**/cloud_redis_client.py",
    r"""
            parent \(str\): Required. The resource name of the instance location using the form:
                ::

                    `projects/{project_id}/locations/{location_id}`
                where ``location_id`` refers to a GCP region""",
    r"""
            parent (str): Required. The resource name of the instance location using the form ``projects/{project_id}/locations/{location_id}``
                where ``location_id`` refers to a GCP region""",
)


s.replace(
    "google/cloud/**/cloud_redis_client.py",
    r"""
                with the following restrictions:

                \* Must contain only lowercase letters, numbers, and hyphens\.""",
    r"""
                with the following restrictions:
                * Must contain only lowercase letters, numbers, and hyphens.""",
)

s.replace(
    "google/cloud/**/cloud_redis_client.py",
    r"""
            name \(str\): Required. Redis instance resource name using the form:
                ::

                    `projects/{project_id}/locations/{location_id}/instances/{instance_id}`
                where ``location_id`` refers to a GCP region""",
    r"""
            name (str): Required. Redis instance resource name using the form ``projects/{project_id}/locations/{location_id}/instances/{instance_id}```
                where ``location_id`` refers to a GCP region""",
)

s.replace(
    "google/cloud/**/cloud_redis_client.py",
    r"""
                fields from ``Instance``:

                 \*   ``displayName``
                 \*   ``labels``
                 \*   ``memorySizeGb``
                 \*   ``redisConfig``""",
    r"""
                fields from ``Instance``: ``displayName``, ``labels``, ``memorySizeGb``, and ``redisConfig``.""",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)
