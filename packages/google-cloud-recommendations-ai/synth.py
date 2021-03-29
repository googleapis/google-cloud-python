# Copyright 2020 Google LLC
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
import os
import re

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate Recommendations AI GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="recommendationengine",
    version="v1beta1",
    bazel_target="//google/cloud/recommendationengine/v1beta1:recommendationengine-v1beta1-py",
)

s.move(library, excludes=["setup.py", "docs/index.rst", "README.rst"])


# rename library to recommendations ai, to be consistent with product branding
s.replace(
    ["google/**/*.py", "tests/**/*.py"],
    "google-cloud-recommendationengine",
    "google-cloud-recommendations-ai",
)

# surround path with * with ``
s.replace("google/**/*.py", """"(projects/\*/.*)"\.""", "``\g<1>``")
s.replace(
    "google/**/*client.py",
    '''"projects/\*/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations/\<YOUR_API_KEY\>"''',
    """``projects/*/locations/global/catalogs/default_catalog/eventStores/default_event_store/predictionApiKeyRegistrations/<YOUR_API_KEY>``"""
)
s.replace(
    "google/**/import_.py",
    "gs://bucket/directory/\*\.json",
    "``gs://bucket/directory/*.json``",
)


# Delete broken path helper 'catalog_item_path_path'
# https://github.com/googleapis/gapic-generator-python/issues/701
s.replace(
    "google/**/client.py",
    """\s+@staticmethod
\s+def catalog_item_path_path.*?
\s+return m\.groupdict\(\) if m else \{\}
""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)

s.replace(
    "google/**/async_client.py",
    """parse_catalog_item_path_path =.*?\)""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)
s.replace(
    "google/**/async_client.py",
    """catalog_item_path_path =.*?\)""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)

# Delete unit tests for 'catalog_item_path_path'
s.replace(
    "tests/**/test_catalog_service.py",
    """def test_catalog_item_path_path.*?assert expected == actual""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)

s.replace(
    "tests/**/test_catalog_service.py",
    """def test_parse_catalog_item_path_path.*?assert expected == actual""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=98, microgenerator=True)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
