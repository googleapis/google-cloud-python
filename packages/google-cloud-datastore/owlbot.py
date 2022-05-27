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
from pathlib import Path
from typing import List, Optional

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()


# This is a customized version of the s.get_staging_dirs() function from synthtool to
# cater for copying 2 different folders from googleapis-gen
# which are datastore and datastore/admin
# Source https://github.com/googleapis/synthtool/blob/master/synthtool/transforms.py#L280
def get_staging_dirs(
    default_version: Optional[str] = None, sub_directory: Optional[str] = None
) -> List[Path]:
    """Returns the list of directories, one per version, copied from
    https://github.com/googleapis/googleapis-gen. Will return in lexical sorting
    order with the exception of the default_version which will be last (if specified).
    Args:
      default_version (str): the default version of the API. The directory for this version
        will be the last item in the returned list if specified.
      sub_directory (str): if a `sub_directory` is provided, only the directories within the
        specified `sub_directory` will be returned.
    Returns: the empty list if no file were copied.
    """

    staging = Path("owl-bot-staging")

    if sub_directory:
        staging /= sub_directory

    if staging.is_dir():
        # Collect the subdirectories of the staging directory.
        versions = [v.name for v in staging.iterdir() if v.is_dir()]
        # Reorder the versions so the default version always comes last.
        versions = [v for v in versions if v != default_version]
        versions.sort()
        if default_version is not None:
            versions += [default_version]
        dirs = [staging / v for v in versions]
        for dir in dirs:
            s._tracked_paths.add(dir)
        return dirs
    else:
        return []


# This library ships clients for two different APIs,
# Datastore and Datastore Admin
datastore_default_version = "v1"
datastore_admin_default_version = "v1"

for library in get_staging_dirs(datastore_default_version, "datastore"):
    s.move(library / f"google/cloud/datastore_{library.name}")
    s.move(library / "tests/")
    s.move(library / "scripts")

for library in get_staging_dirs(datastore_admin_default_version, "datastore_admin"):
    s.replace(
        library / "google/**/datastore_admin_client.py",
        "google-cloud-datastore-admin",
        "google-cloud-datstore",
    )

    # Remove spurious markup
    s.replace(
        library / "google/**/datastore_admin/client.py",
        r"\s+---------------------------------(-)+",
        "",
    )

    s.move(library / f"google/cloud/datastore_admin_{library.name}")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    split_system_tests=True,
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9", "3.10"],
    cov_level=99,
)
s.move(
    templated_files,
    excludes=["docs/multiprocessing.rst", ".coveragerc", ".github/CODEOOWNERS"],
)

python.py_samples(skip_readmes=True)

python.configure_previous_major_version_branches()

# Preserve system tests w/ GOOGLE_DISABLE_GRPC set (#133, PR #136)
assert 1 == s.replace(
    "noxfile.py",
    r"""\
@nox.session\(python=SYSTEM_TEST_PYTHON_VERSIONS\)
def system\(session\):
""",
    """\
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
@nox.parametrize("disable_grpc", [False, True])
def system(session, disable_grpc):
""",
)

assert 1 == s.replace(
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

assert 1 == s.replace(
    "noxfile.py",
    """\
    system_test_path,
""",
    """\
    system_test_path,
    env=env,
""",
)

assert 1 == s.replace(
    "noxfile.py",
    """\
    system_test_folder_path,
""",
    """\
    system_test_folder_path,
    env=env,
""",
)

# Add nox session to exercise doctests
assert 1 == s.replace(
    "noxfile.py",
    r"""\
    "blacken",
    "docs",
""",
    """\
    "blacken",
    "docs",
    "doctests",
""",
)

assert 1 == s.replace(
    "noxfile.py",
    r"""\
@nox.session\(python=DEFAULT_PYTHON_VERSION\)
def docfx\(session\):
""",
    """\
@nox.session(python="3.6")
def doctests(session):
    # Doctests run against Python 3.6 only.
    # It is difficult to make doctests run against both Python 2 and Python 3
    # because they test string output equivalence, which is difficult to
    # make match (e.g. unicode literals starting with "u").

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install("mock", "pytest", "sphinx", "google-cloud-testutils")
    session.install("-e", ".")

    # Run py.test against the system tests.
    session.run("py.test", "tests/doctests.py")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docfx(session):
""",
)

# Work around: https://github.com/googleapis/gapic-generator-python/issues/689
s.replace(
    [
        "google/**/datastore_admin/async_client.py",
        "google/**/datastore_admin/client.py",
        "google/**/types/datastore_admin.py",
    ],
    r"Sequence\[.*\.LabelsEntry\]",
    r"Dict[str, str]",
)

# Add documentation about creating indexes and populating data for system
# tests.
assert 1 == s.replace(
    "CONTRIBUTING.rst",
    r"""
\*\*\*\*\*\*\*\*\*\*\*\*\*
Test Coverage
\*\*\*\*\*\*\*\*\*\*\*\*\*
""",
    """
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
""",
)

# add type checker nox session
s.replace(
    "noxfile.py",
    """nox.options.sessions = \[
    "unit",
    "system",""",
    """nox.options.sessions = [
    "unit",
    "system",
    "mypy",""",
)


s.replace(
    "noxfile.py",
    """\
@nox.session\(python=DEFAULT_PYTHON_VERSION\)
def lint_setup_py\(session\):
""",
    '''\
@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".")
    session.install(
        "mypy", "types-setuptools", "types-mock", "types-protobuf", "types-requests"
    )
    session.run("mypy", "google/", "tests/")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
''',
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
