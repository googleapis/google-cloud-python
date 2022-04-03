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
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(
        library / f"google/cloud/bigquery_storage_{library.name}/types/arrow.py",
        r""".
    Attributes:""",
        r""".\n
    Attributes:""",
    )

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

    # We want types and __version__ to be accessible through the "main" library
    # entry point.
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        f"from google\\.cloud\\.bigquery_storage_{library.name}\\.types\\.arrow import ArrowRecordBatch",
        (
            f"from google.cloud.bigquery_storage_{library.name} import types\n"
            f"from google.cloud.bigquery_storage_{library.name} import __version__\n"
            "\\g<0>"
        ),
    )
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        r"""["']ArrowRecordBatch["']""",
        ('"__version__",\n' '    "types",\n' "    \\g<0>"),
    )

    # We want to expose all types through "google.cloud.bigquery_storage.types",
    # not just the types generated for the BQ Storage library. For example, we also
    # want to include common proto types such as Timestamp.
    s.replace(
        library / "google/cloud/bigquery_storage/__init__.py",
        r"import types",
        "import gapic_types as types",
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

    # The append_rows method doesn't contain keyword arguments that build request
    # objects, so flattened tests are not needed and break with TypeError.
    s.replace(
        library
        / f"tests/unit/gapic/bigquery_storage_{library.name}*/test_big_query_write.py",
        r"(@[a-z.()\n]*\n)?(async )?"
        r"def test_append_rows_flattened[_a-z]*\(\):\n"
        r"( {4}.*|\n)+",
        "\n",
    )

    s.move(
        library,
        excludes=[
            "bigquery-storage-*-py.tar.gz",
            "docs/conf.py",
            "docs/index.rst",
            f"google/cloud/bigquery_storage_{library.name}/__init__.py",
            # v1beta2 was first generated after the microgenerator migration.
            "scripts/fixup_bigquery_storage_v1beta2_keywords.py",
            "README.rst",
            "nox*.py",
            "setup.py",
            "setup.cfg",
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
extras = ["fastavro", "pandas", "pyarrow"]
unit_test_extras = ["tests"] + extras

templated_files = common.py_library(
    microgenerator=True,
    samples=True,
    unit_test_extras=unit_test_extras,
    system_test_extras=extras,
    system_test_external_dependencies=["google-cloud-bigquery"],
    cov_level=98,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
