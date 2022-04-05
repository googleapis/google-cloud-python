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

from pathlib import Path
import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    s.move(library, excludes=["setup.py", "README.rst"])
s.remove_staging_dirs()

# Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/1083
s.replace(
    "google/cloud/**/types/compute.py",
    """A request message for InstanceGroupManagers.AbandonInstances.
    See the method description for details.\n
    Attributes""",
    """A request message for InstanceGroupManagers.AbandonInstances.
    See the method description for details.\n
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields\n
    Attributes"""
)

# Work around formatting issues with docstrings
s.replace("google/cloud/**/types/compute.py", """\"IT_\"""", """`IT_`""")
s.replace("google/cloud/**/types/compute.py", """\"NS_\"""", """`NS_`""")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    cov_level=98,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)

s.move(templated_files, excludes=[".coveragerc"]) # the microgenerator has a good coveragerc file

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=98")

python.py_samples(skip_readmes=True)

python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Run blacken session for all directories with a noxfile
# ----------------------------------------------------------------------------

for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
