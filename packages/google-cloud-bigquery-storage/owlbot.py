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
default_version = json.load(open(".repo-metadata.json", "rt")).get("default_version")

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # We don't want the generated client to be accessible through
    # "google.cloud.bigquery_storage", replace it with the hand written client that
    # wraps it.
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        f"from google\\.cloud\\.bigquery_storage_{library.name}\\.services.big_query_read.client import",
        f"from google.cloud.bigquery_storage_{library.name} import",
    )

    # We also don't want to expose the async client just yet, at least not until
    # it is wrapped in its own manual client class.
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        (
            f"from google\\.cloud\\.bigquery_storage_{library.name}\\.services.big_query_read.async_client "
            r"import BigQueryReadAsyncClient\n"
        ),
        "",
    )
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        r"""["']BigQueryReadAsyncClient["'],\n""",
        "",
    )

    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        r"""["']ArrowRecordBatch["']""",
        ('"__version__",\n' '    "types",\n' "    \\g<0>"),
    )

    # We want types to be accessible through the "main" library
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        f"from google\\.cloud\\.bigquery_storage_{library.name}\\.types\\.arrow import ArrowRecordBatch",
        (
            f"from google.cloud.bigquery_storage_{library.name} import gapic_types as types\n"
            "\\g<0>"
        ),
    )

    # The DataFormat enum is not exposed in bigquery_storage_v1/types, add it there.
    s.replace(
        library / f"google/cloud/bigquery_storage_{library.name}*/types/__init__.py",
        r"from \.stream import \(",
        "\\g<0>\n    DataFormat,",
    )
    s.replace(
        library / f"google/cloud/bigquery_storage_{library.name}*/types/__init__.py",
        r"""["']ReadSession["']""",
        '"DataFormat",\n    \\g<0>',
    )

    s.move(
        [library],
        excludes=[
            "setup.py",
            f"google/cloud/bigquery_storage_{library.name}/__init__.py",
            # v1beta2 was first generated after the microgenerator migration.
            "scripts/fixup_bigquery_storage_v1beta2_keywords.py",
            "**/gapic_version.py",
            "docs/index.rst",
            "testing/constraints-3.7.txt",
        ],
    )
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

extras = ["fastavro", "pandas", "pyarrow"]
unit_test_extras = ["tests"] + extras

templated_files = gcp.CommonTemplates().py_library(
    cov_level=98,
    microgenerator=True,
    unit_test_extras=unit_test_extras,
    system_test_extras=extras,
    system_test_external_dependencies=["google-cloud-bigquery"],
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(
    templated_files,
    excludes=[".coveragerc", ".github/release-please.yml", "docs/index.rst"],
)

python.py_samples(skip_readmes=True)

# The format session in the sample folders conflict with the root noxfile,
# which ends up formatting samples because of a symlink in the docs/ directory.
s.shell.run(["nox", "-s", "format"], hide_output=False)

# TODO(swast): run format session for all directories which have a noxfile
# for noxfile in Path(".").glob("**/noxfile.py"):
#    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)
