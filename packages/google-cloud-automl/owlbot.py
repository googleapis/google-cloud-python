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

import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Add TablesClient and GcsClient to v1beta1
    if library.name == "v1beta1":
        s.replace(
            library / f"google/cloud/automl_v1beta1/__init__.py",
            "from .services.auto_ml import AutoMlClient\n"
            "from .services.auto_ml import AutoMlAsyncClient\n"
            "from .services.prediction_service import PredictionServiceClient\n",
            "from .services.auto_ml import AutoMlClient\n"
            "from .services.auto_ml import AutoMlAsyncClient\n"
            "from .services.prediction_service import PredictionServiceClient\n"
            "from .services.tables.gcs_client import GcsClient\n"
            "from .services.tables.tables_client import TablesClient\n"
        )

        s.replace(
            library / f"google/cloud/automl_v1beta1/__init__.py",
            f"""__all__ = \(""",
            """__all__ = ("GcsClient", "TablesClient","""
        )

        s.replace(
            library / "docs/automl_v1beta1/services.rst",
            """auto_ml
    prediction_service""",
            """auto_ml
    prediction_service
    tables"""
        )

    s.move(library, excludes=["README.rst", "docs/index.rst", "setup.py", "*.tar.gz"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=99,
    samples=True,
    unit_test_extras=["pandas", "storage"],
    system_test_extras=["pandas", "storage"]
)

s.move(templated_files, excludes=["README.rst"])
python.configure_previous_major_version_branches()

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=99")

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
