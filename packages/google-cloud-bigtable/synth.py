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
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate bigtable and bigtable_admin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="bigtable",
    version="v2",
    bazel_target="//google/bigtable/v2:bigtable-v2-py",
    include_protos=True,
)

s.move(library / "google/cloud/bigtable_v2")
s.move(library / "tests")

# Generate admin client
library = gapic.py_library(
    service="bigtable_admin",
    version="v2",
    bazel_target="//google/bigtable/admin/v2:bigtable-admin-v2-py",
    include_protos=True,
)

s.move(library / "google/cloud/bigtable_admin_v2")
s.move(library / "tests")

# ----------------------------------------------------------------------------
# Work around non-standard installations (missing setuptools).
#
# These replacements can be removed after migrating to the microgenerator,
# which will generate them directly.
# ----------------------------------------------------------------------------

admin_clients = [
    "google/cloud/bigtable_admin_v2/gapic/bigtable_instance_admin_client.py",
    "google/cloud/bigtable_admin_v2/gapic/bigtable_table_admin_client.py",
]

s.replace(
    admin_clients,
    """\
_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution\(
    'google-cloud-bigtable-admin',
\).version
""",
    """\
try:
    _GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
        "google-cloud-bigtable"
    ).version
except pkg_resources.DistributionNotFound:  # pragma: NO COVER
    _GAPIC_LIBRARY_VERSION = None
"""
)

s.replace(
    "google/cloud/bigtable_v2/gapic/bigtable_client.py",
    """\
_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution\(
    'google-cloud-bigtable',
\).version
""",
    """\
try:
    _GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
        "google-cloud-bigtable"
    ).version
except pkg_resources.DistributionNotFound:  # pragma: NO COVER
    _GAPIC_LIBRARY_VERSION = None
"""
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=99, samples=True)
s.move(templated_files, excludes=['noxfile.py'])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(samples=True)
for path in sample_files:
    s.move(path, excludes=['noxfile.py'])


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
