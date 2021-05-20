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
import synthtool.gcp as gcp
from synthtool.languages import python
import logging

logging.basicConfig(level=logging.DEBUG)

common = gcp.CommonTemplates()

default_version = "v2"

for library in s.get_staging_dirs(default_version):
    # Fix docstring.
    s.replace(library / "google/cloud/*/types/target.py", "X-Google-\*", "X-Google-\\*")
    s.replace(library / "google/cloud/*/types/target.py", "X-AppEngine-\*", "X-AppEngine-\\*")

    # Comment out broken assertion in unit test
    # https://github.com/googleapis/gapic-generator-python/issues/897
    s.replace(
        library / "tests/**/test_cloud_tasks.py",
        "assert args\[0\]\.lease_duration == duration_pb2\.Duration\(seconds=751\)",
        "# assert args[0].lease_duration == duration_pb2.Duration(seconds=751)"
    )
    s.replace(
        library / "tests/**/test_cloud_tasks.py",
        "assert args\[0\].schedule_time == timestamp_pb2\.Timestamp\(seconds=751\)",
        "# assert args[0].schedule_time == timestamp_pb2.Timestamp(seconds=751)"
    )

    excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst", "*.tar.gz"]
    s.copy(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
