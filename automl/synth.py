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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
versions = ["v1beta1"]


# ----------------------------------------------------------------------------
# Generate automl GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("automl", version, include_protos=True)
    s.move(library / f"google/cloud/automl_{version}")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"docs/gapic/{version}")

s.move(library / f"docs/conf.py")

# Use the highest version library to generate import alias.
s.move(library / "google/cloud/automl.py")

# Add tables client to v1beta1
s.replace(
    f"google/cloud/automl_v1beta1/__init__.py",
    f"from google.cloud.automl_v1beta1.gapic import prediction_service_client",
    f"from google.cloud.automl_v1beta1.gapic import prediction_service_client\n"
    f"from google.cloud.automl_v1beta1.tables import tables_client"
    f"\n\n"
    f"class TablesClient(tables_client.TablesClient):"
    f"    __doc__ = tables_client.TablesClient.__doc__"
)

s.replace(
    f"google/cloud/automl_v1beta1/__init__.py",
    f"""__all__ = \(
    'enums',
    'types',
    'AutoMlClient',
    'PredictionServiceClient',
\)""",
    f"__all__ = (\"enums\", \"types\", \"AutoMlClient\", \"PredictionServiceClient\", \"TablesClient\")"
)

# Fixup issues in generated code
s.replace(
    "**/gapic/*_client.py",
    r"metadata_type=operations_pb2.OperationMetadata",
    r"metadata_type=proto_operations_pb2.OperationMetadata",
)

# Fix spacing/'::' issues in docstrings
s.replace(
    "google/cloud/automl_v1beta1/gapic/prediction_service_client.py", "^\s+::", ""
)

s.replace(
    "google/cloud/automl_v1beta1/gapic/auto_ml_client.py",
    "^(\s+)(::)\n\n\s+?([^\s])",
    "    \g<1>\g<2>\n    \g<1>\g<3>",
)

# Remove 'raw-latex' sections with sample JSON Lines files
s.replace(
    "google/cloud/**/io_pb2.py",
    r"""Sample in-line
     JSON Lines file.*?\}`\n""",
    "\n",
    flags=re.DOTALL,
)

# Remove 'raw-latex' sections with sample JSON Lines files
s.replace(
    "google/cloud/**/io_pb2.py",
    r"""Sample
     in-line JSON Lines.*?(\n\s+-\s+For Text Classification.*\n)""",
     "\g<1>",
     flags=re.DOTALL
)

# Replace docstring with no summary line
s.replace(
"google/cloud/**/io_pb2.py",
r"""__doc__ = \"\"\"-  For Translation: CSV file ``translation\.csv``, with each """,
r'''__doc__ = """
-  For Translation: CSV file ``translation.csv``, with each ''',
flags=re.DOTALL,
)

s.replace(
"google/cloud/**/io_pb2.py",
r":raw-latex:`\\t `",
r"\\\\t")
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=82, cov_level=83)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
