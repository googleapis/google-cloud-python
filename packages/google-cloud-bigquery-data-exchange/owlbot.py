# Copyright 2022 Google LLC
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

import json
from pathlib import Path
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get(
    "default_version"
)

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    s.replace(
        [
            library / f"google/cloud/bigquery_data_exchange_{library.name}/**/*.py",
            library / f"tests/unit/gapic/bigquery_data_exchange_{library.name}/**/*.py",
        ],
        f"from google.cloud.bigquery.dataexchange.common import common_pb2",
        f"from google.cloud.bigquery_data_exchange_{library.name} import common",
    )
    s.replace(
        library / f"google/cloud/bigquery_data_exchange_{library.name}/**/*.py",
        "google.cloud.bigquery.dataexchange.common.common_pb2.Category",
        f"google.cloud.bigquery_data_exchange_{library.name}.common.Category",
    )
    s.replace(
        library / f"docs/common/types.rst",
        "google.cloud.bigquery.data_exchange.common.types",
        f"google.cloud.bigquery_data_exchange_{library.name}.common.types",
    )
    s.replace(
        [
            library / f"google/cloud/bigquery_data_exchange_{library.name}/**/*.py",
            library / f"tests/unit/gapic/bigquery_data_exchange_{library.name}/**/*.py",
        ],
        "common_pb2",
        "common",
    )
    s.move(
        library / "google/cloud/bigquery_data_exchange/common",
        library / "google/cloud/bigquery_data_exchange_v1beta1/common",
    )
    s.move(
        library,
        excludes=[
            "docs/index.rst", "**/gapic_version.py"
        ],
    )
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",  # the microgenerator has a good coveragerc file
        ".github/auto-label.yaml",  # the templated file is missing a license header
        "docs/index.rst",  # there is an additional module common which is added
        ".github/release-please.yml", # configure release-please to use manifest
    ],
)

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Run format session
# ----------------------------------------------------------------------------

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)

