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

common = gcp.CommonTemplates()

# This library ships clients for two different APIs,
# Datastore and Datastore Admin
datastore_default_version = "v1"
datastore_admin_default_version = "v1"

for library in s.get_staging_dirs(datastore_default_version):
    if library.parent.absolute() == 'datastore':
        s.move(library / f"google/cloud/datastore_{library.name}")
        s.move(library / f"tests/")
        s.move(library / "scripts")

for library in s.get_staging_dirs(datastore_admin_default_version):
    if library.parent.absolute() == 'datastore_admin':
        s.replace(
            library / "google/**/datastore_admin_client.py",
            "google-cloud-datastore-admin",
            "google-cloud-datstore"
        )

        # Remove spurious markup
        s.replace(
            "google/**/datastore_admin/client.py",
            "\s+---------------------------------(-)+",
            ""
        )

        s.move(library / f"google/cloud/datastore_admin_{library.name}")
        s.move(library / f"tests")
        s.move(library / "scripts")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
)
s.move(templated_files, excludes=["docs/multiprocessing.rst", ".coveragerc"])


# Preserve system tests w/ GOOGLE_DISABLE_GRPC set (#133, PR #136)
s.replace(
    "noxfile.py",
    """\
@nox.session\(python=SYSTEM_TEST_PYTHON_VERSIONS\)
def system\(session\):
""",
    """\
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
@nox.parametrize("disable_grpc", [False, True])
def system(session, disable_grpc):
""",
)

s.replace(
    "noxfile.py",
    """\
    # Run py.test against the system tests.
""",
    """\
    env = {}
    if disable_grpc:
        env["GOOGLE_CLOUD_DISABLE_GRPC"] = "True"

    # Run py.test against the system tests.
""",
)

s.replace(
    "noxfile.py",
    """session\.run\(
            "py\.test",
            "--quiet",
            f"--junitxml=system_\{session\.python\}_sponge_log\.xml",
            system_test_path,
            \*session\.posargs
        \)""",
    """session.run(
            "py.test",
            "--quiet",
            f"--junitxml=system_{session.python}_sponge_log.xml",
            system_test_path,
            env=env,
            *session.posargs
        )
""",
)

s.replace(
    "noxfile.py",
    """session\.run\(
            "py\.test",
            "--quiet",
            f"--junitxml=system_\{session\.python\}_sponge_log\.xml",
            system_test_folder_path,
            \*session\.posargs
        \)""",
    """session.run(
            "py.test",
            "--quiet",
            f"--junitxml=system_{session.python}_sponge_log.xml",
            system_test_folder_path,
            env=env,
            *session.posargs
        )
""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add documentation about creating indexes and populating data for system
# tests.
num = s.replace(
    "CONTRIBUTING.rst",
    """\
\*\*\*\*\*\*\*\*\*\*\*\*\*
Test Coverage
\*\*\*\*\*\*\*\*\*\*\*\*\*
""",
    """\
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

   $ python tests/system/utils/clear_datastore.py

*************
Test Coverage
*************
""")

if num != 1:
    raise Exception("Required replacement not made.")
