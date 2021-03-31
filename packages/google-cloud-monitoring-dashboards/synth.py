# Copyright 2020 Google LLC
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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate monitoring dashboards GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="monitoring_dashboard",
    version="v1",
    bazel_target="//google/monitoring/dashboard/v1:monitoring-dashboard-v1-py",
    include_protos=True,
)

s.move(library / "google/cloud/monitoring_dashboard_v1/proto")
s.move(library / "google/monitoring/dashboard", "google/cloud/monitoring_dashboard")
s.move(
    library / "google/monitoring/dashboard_v1",
    "google/cloud/monitoring_dashboard_v1"
)
s.move(library / "tests")
s.move(library / "scripts")
s.move(library / "docs", excludes=[library / "docs/index.rst"])

# Fix namespace
s.replace(
    "google/cloud/**/*.py",
    "google.monitoring.dashboard_v1",
    "google.cloud.monitoring_dashboard_v1",
)
s.replace(
    "tests/unit/gapic/**/*.py",
    "google.monitoring.dashboard_v1",
    "google.cloud.monitoring_dashboard_v1",
)
s.replace(
    "docs/**/*.rst",
    "google.monitoring.dashboard_v1",
    "google.cloud.monitoring_dashboard_v1",
)

# Keep cloud in package names for consistency
s.replace(
    "google/**/*.py", "google-cloud-monitoring-dashboard", "google-cloud-monitoring-dashboards"
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=96
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file


# Temporarily disable warnings due to
# https://github.com/googleapis/gapic-generator-python/issues/525
s.replace("noxfile.py", '[\"\']-W[\"\']', '# "-W"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
