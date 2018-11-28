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
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate monitoring GAPIC layer
# ----------------------------------------------------------------------------
v3_library = gapic.py_library(
    "monitoring",
    "v3",
    config_path="/google/monitoring/artman_monitoring.yaml",
    artman_output_name="monitoring-v3",
)

# don't copy nox.py, setup.py, README.rst, docs/index.rst
excludes = ["nox.py", "setup.py", "README.rst", "docs/index.rst"]
s.move(v3_library, excludes=excludes)

# metadata in tests in none but should be empty list.
# https://github.com/googleapis/gapic-generator/issues/2014
s.replace(
    "google/cloud/*/gapic/*_client.py",
    'def .*\(([^\)]+)\n.*metadata=None\):\n\s+"""(.*\n)*?\s+"""\n',
    "\g<0>"
    "        if metadata is None:\n"
    "            metadata = []\n"
    "        metadata = list(metadata)\n",
)

# Issues exist where python files should defined the source encoding
# https://github.com/googleapis/gapic-generator/issues/2097
files = ["google/cloud/monitoring_v3/proto/common_pb2.py"]
for f in files:
    s.replace(f, r"(^.*$\n)*", r"# -*- coding: utf-8 -*-\n\g<0>")

# GAPIC-Generator is mangling some docstrings
# Missing blank line after bulleted list
s.replace(
    "google/cloud/monitoring_v3/gapic/alert_policy_service_client.py",
    "then a new `\[CONDITION_ID\]` is created.\n",
    "\g<0>\n",
)

s.replace(
    "google/cloud/monitoring_v3/gapic/alert_policy_service_client.py",
    "                ::\n\n",
    "",
)

s.replace(
    "google/cloud/monitoring_v3/proto/metric_service_pb2.py",
    "^(\s+)have an ``id`` label:  ::      resource.type =\n.*",
    "\g<1>have an ``id`` label::\n\n"
    '\g<1>    resource.type = starts_with("gce_") AND resource.label:id\n',
)

# the metric service grpc transport channel shouldn't limit the size of
# a grpc message at the default 4mb
s.replace(
    "google/cloud/monitoring_v3/gapic/transports/*_service_grpc_transport.py",
    "return google.api_core.grpc_helpers.create_channel\(\n(\s+)address,\n"
    "\s+credentials=.*,\n\s+scopes=.*,\n",
    "\g<0>\g<1>options={\n"
    "\g<1>    'grpc.max_send_message_length': -1,\n"
    "\g<1>    'grpc.max_receive_message_length': -1,\n"
    "\g<1>}.items(),\n",
)

# Deal with long lines due to long proto name
s.replace(
    ["google/cloud/monitoring_v3/__init__.py"],
    "from google.cloud.monitoring_v3.gapic import "
    "notification_channel_service_client\n",
    "from google.cloud.monitoring_v3.gapic import (\n"
    "    notification_channel_service_client as notification_client)\n",
)
s.replace(
    ["google/cloud/monitoring_v3/__init__.py"],
    "notification_channel_service_client.NotificationChannelServiceClient",
    "notification_client.NotificationChannelServiceClient",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=97)
s.move(templated_files)
