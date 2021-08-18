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
    dependencies = [
      "configmanagement",
      "multiclusteringress",
    ]

    # rename dependencies google.cloud.gkehub.dep.vX to google.cloud.gkehub.dep_vX
    for dep in dependencies:
        s.replace(
          [
            library  / f"google/cloud/gkehub_{library.name}/**/*.py",
            library  / f"tests/unit/gapic/gkehub_{library.name}/**/*.py",
            library  / f"google/cloud/gkehub/{dep}_{library.name}/**/*.py",
          ],
          f"from google.cloud.gkehub.{dep}.{library.name} import",
          f"from google.cloud.gkehub import {dep}_{library.name} as"
        )

    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/**/types/*.py",
              r""".
    Attributes:""",
              r""".\n
    Attributes:""",
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

    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst", "google/cloud/gkehub/configmanagement", "google/cloud/gkehub/multiclusteringress"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = common.py_library(cov_level=98, microgenerator=True)
python.py_samples(skip_readmes=True)

# the microgenerator has a good coveragerc file
excludes = [".coveragerc"]
s.move(
  templated_files, excludes=excludes
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
