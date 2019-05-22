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
import os
from pathlib import Path

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate phishingprotection GAPIC layer
# ----------------------------------------------------------------------------
versions = ["v1beta1"]
for version in versions:
    library = gapic.py_library(
        "phishingprotection",
        version,
        config_path=f"/google/cloud/phishingprotection/artman_phishingprotection_{version}.yaml",
        include_protos=True,
        generator_args=["--dev_samples"],
    )

    excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst"]

    s.move(library, excludes=excludes)

    # Files to be renamed (remove v1_beta1 from name)
    gapic_dir = Path(f"google/cloud/phishingprotection_{version}/gapic")
    client = gapic_dir / "phishing_protection_service_v1_beta1_client.py"
    client_config = gapic_dir / "phishing_protection_service_v1_beta1_client_config.py"
    transport = (
        gapic_dir / "transports/phishing_protection_service_v1_beta1_grpc_transport.py"
    )
    unit_test = Path(
        "tests/unit/gapic/v1beta1/test_phishing_protection_service_v1_beta1_client_v1beta1.py"
    )

    s.replace(
        client,
        "google-cloud-phishingprotection",
        "google-cloud-phishing-protection",
    )

    files = [client, client_config, transport, unit_test]
    for file_ in files:
        new_name = str(file_).replace("v1_beta1_", "")
        os.rename(file_, new_name)

# Rename classes in google/cloud and in tests/
class_names = [
    "PhishingProtectionServiceV1Beta1Client",
    "PhishingProtectionServiceV1Beta1GrpcTransport",
]

for name in class_names:
    new_name = name.replace("V1Beta1", "")
    s.replace("google/cloud/**/*.py", name, new_name)
    s.replace("tests/**/*.py", name, new_name)

# Rename references to modules

module_names = [
    "phishing_protection_v1_beta1_service_client",
    "phishing_protection_service_v1_beta1_grpc_transport",
    "phishing_protection_service_v1_beta1_client",
]

for name in module_names:
    new_name = name.replace("v1_beta1_", "")
    s.replace("google/cloud/**/*.py", name, new_name)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
