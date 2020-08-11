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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta1", "v1"]


# ----------------------------------------------------------------------------
# Generate automl GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="automl",
        version=version,
        bazel_target=f"//google/cloud/automl/{version}:automl-{version}-py",
        include_protos=True
    )

    s.move(library / f"google/cloud/automl_{version}")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"docs/gapic/{version}")

s.move(library / f"docs/conf.py")

# Use the highest version library to generate import alias.
s.move(library / "google/cloud/automl.py")

# Add TablesClient and GcsClient to v1beta1
s.replace(
    f"google/cloud/automl_v1beta1/__init__.py",
    f"from google.cloud.automl_v1beta1.gapic import prediction_service_client",
    f"from google.cloud.automl_v1beta1.gapic import prediction_service_client\n"
    f"from google.cloud.automl_v1beta1.tables import tables_client\n"
    f"from google.cloud.automl_v1beta1.tables import gcs_client"
    f"\n\n"
    f"class TablesClient(tables_client.TablesClient):"
    f"    __doc__ = tables_client.TablesClient.__doc__"
    f"\n\nclass GcsClient(gcs_client.GcsClient):"
    f"    __doc__ = gcs_client.GcsClient.__doc__",
)

s.replace(
    f"google/cloud/automl_v1beta1/__init__.py",
    f"""__all__ = \(
    'enums',
    'types',
    'AutoMlClient',
    'PredictionServiceClient',
\)""",
    f'__all__ = ("enums", "types", "AutoMlClient", "PredictionServiceClient", "TablesClient", "GcsClient")',
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
    flags=re.DOTALL,
)


s.replace("google/cloud/**/io_pb2.py", r":raw-latex:`\\t `", r"\\\\t")

# Remove html bits that can't be rendered correctly
s.replace(
    "google/cloud/automl_v1/**/io_pb2.py",
    r""".. raw:: html.+?
     \</.+?\>""",
    r"",
    flags=re.DOTALL,
)

# Remove raw-latex wrapping newline
s.replace("google/cloud/automl_v1/**/io_pb2.py", r""":raw-latex:`\\n`""", r"``\\\\n``")

# Make \n visible in JSONL samples
s.replace("google/cloud/**/io_pb2.py", r"\}\\n", r"}\\\\n")

# properly escape emphasis
s.replace("google/cloud/**/*.py",
"""image_classification_dataset_metadata:\*""",
"""``image_classification_dataset_metadata``""")

s.replace("google/cloud/**/*.py",
"""video_classification_model_metadata:\*""",
"""``video_classification_model_metadata:*``""")

# Escape '_' at the end of the line in pb2 docstrings
s.replace(
"google/cloud/**/*_pb2.py",
"""\_$""",
"""\_""",
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=82, cov_level=83, samples=True
)

python.py_samples(skip_readmes=True)

s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')
# TODO(busunkim): Remove after microgenerator transition.
# This is being added to AutoML because the proto comments are long and
# regex replaces are a brittle temporary solution. 
s.replace(
"noxfile.py", 
"""'-W',  # warnings as errors
\s+'-T',  \# show full traceback on exception""",
""""-T",  # show full traceback on exception""")


# install with extras (pandas, storage)
s.replace(
    "noxfile.py",
    """session\.install\(['"]-e['"], ['"]\.['"]\)""",
    """session.install("-e", ".[pandas,storage]")""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
