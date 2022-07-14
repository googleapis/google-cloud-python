# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    submodules = [
      "configmanagement",
      "multiclusteringress",
    ]

    for submodule in submodules:
        # Move v1 submodule namespace from google.cloud.gkehub.{submodule}_v1 to google.cloud.gkehub_vX.{submodule}_v1
        s.move(library / f"google/cloud/gkehub/{submodule}_v1", library / f"google/cloud/gkehub_{library.name}/{submodule}_v1")

        # Adjust docs based on new submodule namespace google.cloud.gkehub_vX.{submodule}_v1.types"
        s.replace(
          library  / f"docs/{submodule}_v1/types.rst",
          f"google.cloud.gkehub.{submodule}_v1.types",
          f"google.cloud.gkehub_{library.name}.{submodule}_v1.types",
        )

        # Move docs to correct location /docs/gkehub_vX/{submodule}_v1
        s.move(library / f"docs/{submodule}_v1", library / f"docs/gkehub_{library.name}/{submodule}_v1")

        # Rename v1 submodule imports from google.cloud.gkehub.submodule.v1 to google.cloud.gkehub_vX.submodule_v1
        s.replace(
          [
            library  / f"google/cloud/gkehub_{library.name}/**/*.py",
            library  / f"tests/unit/gapic/gkehub_{library.name}/**/*.py",
          ],
          f"from google.cloud.gkehub.{submodule}.v1 import {submodule}_pb2",
          f"from google.cloud.gkehub_{library.name} import {submodule}_v1"
        )

        s.replace(
          library / f"google/cloud/gkehub_{library.name}/types/feature.py",
          f"google.cloud.gkehub.{submodule}.v1.{submodule}_pb2",
          f"google.cloud.gkehub_v1.{submodule}_v1"
        )

        s.replace(
          library / f"google/cloud/gkehub_{library.name}/types/feature.py",
          f"{submodule}_pb2",
          f"{submodule}_v1"
        )

    # Work around docs issue. Fix proposed upstream in cl/382492769
    s.replace(library / f"google/cloud/gkehub_{library.name}/types/feature.py",
        "    projects/{p}/locations/{l}/memberships/{m}",
        "`projects/{p}/locations/{l}/memberships/{m}`"
    )

     # Work around docs issue. Fix proposed upstream in cl/382492769
    s.replace(library / f"google/cloud/gkehub_{library.name}/types/membership.py",
        """the GKE cluster. For example:
                //container.googleapis.com/projects/my-""",
        """the GKE cluster. For example:
            //container.googleapis.com/projects/my-"""
    )

    # work around issues with docstrings
    s.replace(
        library / "google/cloud/**/*.py",
        """resource.
                \*\*JSON Example\*\*
                ::""",
        """resource. JSON Example.

                .. code-block:: python\n""",
    )

    s.replace(
        library / "google/cloud/**/*.py",
        """\*\*YAML Example\*\*
                ::""",
        """\n                **YAML Example**

                ::\n""",
    )

    s.replace(library / "google/cloud/**/*.py",
        """                For a description of IAM and its features, see the `IAM
                developer's""",
        """\n                For a description of IAM and its features, see the `IAM
                developer's"""
    )

    excludes=[
        "setup.py",
        "README.rst",
        "docs/index.rst",
        "docs/configmanagement_v1/**",
        "docs/multiclusteringress_v1/**",
        "google/cloud/gkehub/configmanagement/**",
        "google/cloud/gkehub/configmanagement_v1/**",
        "google/cloud/gkehub/multiclusteringress/**",
        "google/cloud/gkehub/multiclusteringress_v1/**"
    ]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/pull/1071
s.replace(
    "google/cloud/**/types/*.py",
    """\.
            This field is a member of `oneof`_""",
    """.

            This field is a member of `oneof`_"""
)

# Work around gapic generator bug
s.replace(
    "google/cloud/**/types/configmanagement.py",
    """Configuration for Policy Controller\n
    Attributes""",
    """Configuration for Policy Controller\n
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields\n
    Attributes"""
)

# Work around issue with docstring
s.replace("google/cloud/gkehub_v1beta1/types/membership.py",
"""For example:
             //gkeonprem.googleapis.com/projects/my-""",
"""For example:
            //gkeonprem.googleapis.com/projects/my-""",
)


# Work around issue with docstring
s.replace("google/cloud/gkehub_v1beta1/types/membership.py",
"""For example:

             //gkemulticloud.googleapis.com/projects/my-""",
"""For example:

            //gkemulticloud.googleapis.com/projects/my-""",
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = common.py_library(cov_level=99, microgenerator=True)
python.py_samples(skip_readmes=True)

# the microgenerator has a good coveragerc file
excludes = [".coveragerc"]
s.move(
  templated_files, excludes=excludes
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

