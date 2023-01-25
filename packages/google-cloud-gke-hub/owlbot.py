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

    # workaround bug in the generator
    s.replace(
      library / "google/cloud/gkehub_v1/configmanagement_v1/__init__.py",
      "from google.cloud.gkehub.configmanagement_v1 import gapic_version as package_version",
      "from google.cloud.gkehub_v1 import gapic_version as package_version"
    )

    # workaround bug in the generator
    s.replace(
      library / "google/cloud/gkehub_v1/multiclusteringress_v1/__init__.py",
      "from google.cloud.gkehub.multiclusteringress_v1 import gapic_version as package_version",
      "from google.cloud.gkehub_v1 import gapic_version as package_version"
    )

    excludes=[
        "setup.py",
        "testing/constraints-3.7.txt",
        "docs/index.rst",
        "docs/configmanagement_v1/**",
        "docs/multiclusteringress_v1/**",
        "google/cloud/gkehub/configmanagement/**",
        "google/cloud/gkehub/configmanagement_v1/**",
        "google/cloud/gkehub/multiclusteringress/**",
        "google/cloud/gkehub/multiclusteringress_v1/**",
        "**/gapic_version.py"
    ]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml", "docs/index.rst"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)
