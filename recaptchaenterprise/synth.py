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
# Generate recaptchaenterprise GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library("recaptchaenterprise", "v1beta1", include_protos=True)


# Rename client from (exclude V1Beta1 from Client name)
client = "google/cloud/recaptchaenterprise_v1beta1/gapic/recaptcha_enterprise_service_v1_beta1_client.py"
client_config = "google/cloud/recaptchaenterprise_v1beta1/gapic/recaptcha_enterprise_service_v1_beta1_client_config.py"
transport = "google/cloud/recaptchaenterprise_v1beta1/gapic/transports/recaptcha_enterprise_service_v1_beta1_grpc_transport.py"
unit_test = "tests/unit/gapic/v1beta1/test_recaptcha_enterprise_service_v1_beta1_client_v1beta1.py"

excludes = ["README.rst", "nox.py", "noxfile.py", "setup.py", "docs/index.rst", "tests", client, client_config, transport, unit_test]
s.move(library, excludes=excludes)

s.move(library / client, client.replace("_v1_beta1", ""))
s.move(library / client_config, client_config.replace("_v1_beta1", ""))
s.move(library / transport, transport.replace("_v1_beta1", ""))
s.move(library / unit_test, unit_test.replace("_v1beta1", ""))

s.replace(
    "*/**/*.py",
    "RecaptchaEnterpriseServiceV1Beta1Client",
    "RecaptchaEnterpriseServiceClient",
)

s.replace(
    "google/cloud/**/*.py",
    "recaptcha_enterprise_service_v1_beta1_client",
    "recaptcha_enterprise_service_client")

s.replace(
    "google/cloud/**/recaptcha_enterprise_service_client_config.py",
    "RecaptchaEnterpriseServiceV1Beta1",
    "RecaptchaEnterpriseService")

s.replace(
    "*/cloud/**/*.py",
    "RecaptchaEnterpriseServiceV1Beta1GrpcTransport",
    "RecaptchaEnterpriseServiceGrpcTransport"
)

s.replace(
    "google/cloud/**/*.py",
    "recaptcha_enterprise_service_v1_beta1_grpc_transport",
    "recaptcha_enterprise_service_grpc_transport")


# Fix docstring issue for classes with no summary line
s.replace(
    "google/cloud/**/proto/recaptchaenterprise_pb2.py",
    '''__doc__ = """Attributes:''',
    '''__doc__ = """
    Attributes:''',
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files, excludes=['noxfile.py'])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
