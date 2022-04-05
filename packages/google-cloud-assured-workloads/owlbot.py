# Copyright 2021 Google LLC
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

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # fix the package name in samples/generated_samples to reflect
    # the package on pypi. https://pypi.org/project/google-cloud-assured-workloads/
    s.replace(
        library / "samples/generated_samples/**/*.py",
        "pip install google-cloud-assuredworkloads",
        "pip install google-cloud-assured-workloads",
    )

    s.move(library, excludes=["setup.py", "README.rst"])
s.remove_staging_dirs()

# Work around gapic generator bug. https://github.com/googleapis/gapic-generator-python/issues/1083
s.replace(
    "google/cloud/**/types/assuredworkloads.py",
    """Signed Access Approvals \(SAA\) enrollment response.\n
        Attributes""",
    """Signed Access Approvals (SAA) enrollment response.\n
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields\n
        Attributes"""
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc"]) # the microgenerator has a good coveragerc file

python.py_samples(skip_readmes=True)

python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
