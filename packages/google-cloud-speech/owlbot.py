# Copyright 2019 Google LLC
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
    # Add the manually written SpeechHelpers to v1 and v1p1beta1
    # See google/cloud/speech_v1/helpers.py for details
    count = s.replace(library / f"google/cloud/speech_{library.name}/__init__.py",
                        """__all__ = \(""",
                        """from google.cloud.speech_v1.helpers import SpeechHelpers

class SpeechClient(SpeechHelpers, SpeechClient):
    __doc__ = SpeechClient.__doc__

__all__ = (
                        """,
                    )

    if library.name == "v1":
        # Import from speech_v1 to get the client with SpeechHelpers
        count = s.replace(library / "google/cloud/speech/__init__.py",
            """from google\.cloud\.speech_v1\.services\.speech\.client import SpeechClient""",
            """from google.cloud.speech_v1 import SpeechClient"""
            )

    # Don't move over __init__.py, as we modify it to make the generated client
    # use helpers.py.
    s.move(library, excludes=["setup.py", "docs/index.rst", "README.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=100,
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
