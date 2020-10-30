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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate datastore GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="datastore",
    version="v1",
    bazel_target="//google/datastore/v1:datastore-v1-py",
    include_protos=True,
)

s.move(library / "google/cloud/datastore_v1")

s.move(
    library / f"tests/",
    f"tests",
)
s.move(library / "scripts")

# ----------------------------------------------------------------------------
# Generate datastore admin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="datastore_admin",
    version="v1",
    bazel_target="//google/datastore/admin/v1:datastore-admin-v1-py",
    include_protos=True,
)

s.move(
    library / "google/cloud/datastore_admin_v1",
    "google/cloud/datastore_admin_v1"
)


s.move(
    library / f"tests/",
    f"tests",
)

s.move(library / "scripts")
s.replace(
    "google/**/datastore_admin_client.py",
    "google-cloud-datastore-admin",
    "google-cloud-datstore"
)

# Remove spurious markup
s.replace(
    "google/**/datastore_admin_client.py",
    "-----------------------------------------------------------------------------",
    ""
)

# TODO(busunkim): Remove during the microgenerator transition.
# This re-orders the parameters to avoid breaking existing code.
num = s.replace(
"google/**/datastore_client.py",
"""def commit\(
\s+self,
\s+project_id,
\s+mode=None,
\s+transaction=None,
\s+mutations=None,
\s+retry=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+timeout=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+metadata=None\):""",
"""def commit(
        self,
        project_id,
        mode=None,
        mutations=None,
        transaction=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):"""
)

#if num != 1:
#    raise Exception("Required replacement not made.")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=99)
s.move(templated_files, excludes=["docs/multiprocessing.rst", ".coveragerc"])

s.replace("noxfile.py", """["']sphinx['"]""", '''"sphinx<3.0.0"''')

# Add the `sphinx-ext-doctest` extenaion
s.replace(
    "docs/conf.py",
    """\
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
""",
    """\
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add documentation about creating indexes and populating data for system
# tests.
num = s.replace(
    "CONTRIBUTING.rst",
    'app_credentials.json"',
    """app_credentials.json"

- You'll need to create composite
  `indexes <https://cloud.google.com/datastore/docs/tools/indexconfig>`__
  with the ``gcloud`` command line
  `tool <https://developers.google.com/cloud/sdk/gcloud/>`__::

   # Install the app (App Engine Command Line Interface) component.
   $ gcloud components install app-engine-python

   # Authenticate the gcloud tool with your account.
   $ GOOGLE_APPLICATION_CREDENTIALS="path/to/app_credentials.json"
   $ gcloud auth activate-service-account \
   > --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

   # Create the indexes
   $ gcloud datastore indexes create tests/system/index.yaml

- You'll also need stored data in your dataset. To populate this data, run::

   $ python tests/system/utils/populate_datastore.py

- If you make a mistake during development (i.e. a failing test that
  prevents clean-up) you can clear all system test data from your
  datastore instance via::

   $ python tests/system/utils/clear_datastore.py""")

if num != 1:
    raise Exception("Required replacement not made.")
