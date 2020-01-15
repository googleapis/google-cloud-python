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
    "monitoring-dashboard", "v1", proto_path="/google/monitoring/dashboard/v1"
)

s.move(
    library,
    excludes=[
        "google/cloud/monitoring/dashboard_v1/proto",  # Protos (pb2s) are copied to the incorrect location
        "nox.py",
        "README.rst",
        "setup.py",
        "docs/index.rst",
    ],
)

s.move(
    library / "google/cloud/monitoring/dashboard_v1/proto",
    "google/cloud/monitoring_dashboard/v1/proto",
)

# correct license headers
python.fix_pb2_headers()
python.fix_pb2_grpc_headers()

# Fix imports
s.replace(
    "google/cloud/**/proto/*_pb2*.py",
    "from google\.cloud\.monitoring\.dashboard\_v1\.proto",
    "from google.cloud.monitoring_dashboard.v1.proto",
)

# Fix docstring with trailing backticks
s.replace(
    "google/cloud/**/dashboards_service_pb2.py",
    """          Required\. The resource name of the Dashboard\. The format is ``
          "projects/\{project\_id\_or\_number\}/dashboards/\{dashboard\_id\}"``""",
    """          Required. The resource name of the Dashboard. The format is
          ``"projects/{project_id_or_number}/dashboards/{dashboard_id}"``""",
)

# Keep cloud in package names for consistency
s.replace(
    "google/**/*.py", "google-monitoring-dashboard", "google-cloud-monitoring-dashboards"
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=79)
s.move(templated_files)

# No local dependencies in a split repo
# Manually remove from noxfile until the template is updated
s.replace("noxfile.py", "LOCAL_DEPS = .*", "LOCAL_DEPS = []")


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
