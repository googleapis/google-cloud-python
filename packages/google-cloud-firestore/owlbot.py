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

# This library ships clients for 3 different APIs,
# firestore, firestore_admin and firestore_bundle. 
# firestore_bundle is not versioned
firestore_default_version = "v1"
firestore_admin_default_version = "v1"

# This is a customized version of the s.get_staging_dirs() function from synthtool to
# cater for copying 3 different folders from googleapis-gen
# which are firestore, firestore/admin and firestore/bundle.
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

def update_fixup_scripts(library):
    # Add message for missing 'libcst' dependency
    s.replace(
        library / "scripts/fixup*.py",
        """import libcst as cst""",
        """try:
    import libcst as cst
except ImportError:
    raise ImportError('Run `python -m pip install "libcst >= 0.2.5"` to install libcst.')


    """,
    )

for library in get_staging_dirs(default_version=firestore_default_version, sub_directory="firestore"):
    s.move(library / f"google/cloud/firestore_{library.name}", excludes=[f"__init__.py"])
    s.move(library / f"tests/", f"tests")
    update_fixup_scripts(library)
    s.move(library / "scripts")

for library in get_staging_dirs(default_version=firestore_admin_default_version, sub_directory="firestore_admin"):
    s.move(library / f"google/cloud/firestore_admin_{library.name}", excludes=[f"__init__.py"])
    s.move(library / f"tests", f"tests")
    update_fixup_scripts(library)
    s.move(library / "scripts")

for library in get_staging_dirs(sub_directory="firestore_bundle"):
    s.replace(
        library / "google/cloud/bundle/types/bundle.py",
        "from google.firestore.v1 import document_pb2  # type: ignore\n"
        "from google.firestore.v1 import query_pb2  # type: ignore",
        "from google.cloud.firestore_v1.types import document as document_pb2  # type: ignore\n"
        "from google.cloud.firestore_v1.types import query as query_pb2 # type: ignore"        
    )

    s.replace(
        library / "google/cloud/bundle/__init__.py",
        "from .types.bundle import BundleMetadata\n"
        "from .types.bundle import NamedQuery\n",
        "from .types.bundle import BundleMetadata\n"
        "from .types.bundle import NamedQuery\n"
        "\n"
        "from .bundle import FirestoreBundle\n",
    )

    s.replace(
        library / "google/cloud/bundle/__init__.py",
        "\'BundledQuery\',",
        "\"BundledQuery\",\n\"FirestoreBundle\",",
    )

    s.move(
        library / f"google/cloud/bundle",
        f"google/cloud/firestore_bundle",
    )
    s.move(library / f"tests", f"tests")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    system_test_python_versions=["3.7"],
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9", "3.10"],
    unit_test_external_dependencies=["aiounittest"],
    system_test_external_dependencies=["pytest-asyncio"],
    microgenerator=True,
    cov_level=100,
    split_system_tests=True,
)

s.move(templated_files)

python.py_samples(skip_readmes=True)

python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Customize noxfile.py
# ----------------------------------------------------------------------------

def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, '\\' + c)
    s.replace([path], text, replacement)

system_emulated_session = """
@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system_emulated(session):
    import subprocess
    import signal

    try:
        # https://github.com/googleapis/python-firestore/issues/472
        # Kokoro image doesn't have java installed, don't attempt to run emulator.
        subprocess.call(["java", "--version"])
    except OSError:
        session.skip("java not found but required for emulator support")

    try:
        subprocess.call(["gcloud", "--version"])
    except OSError:
        session.skip("gcloud not found but required for emulator support")

    # Currently, CI/CD doesn't have beta component of gcloud.
    subprocess.call(
        ["gcloud", "components", "install", "beta", "cloud-firestore-emulator",]
    )

    hostport = "localhost:8789"
    session.env["FIRESTORE_EMULATOR_HOST"] = hostport

    p = subprocess.Popen(
        [
            "gcloud",
            "--quiet",
            "beta",
            "emulators",
            "firestore",
            "start",
            "--host-port",
            hostport,
        ]
    )

    try:
        system(session)
    finally:
        # Stop Emulator
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)

"""

place_before(
    "noxfile.py",
    "@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)\n"
    "def system(session):",
    system_emulated_session,
    escape="()"
)

# add system_emulated + mypy nox session
s.replace("noxfile.py",
    """nox.options.sessions = \[
    "unit",
    "system",""",
    """nox.options.sessions = [
    "unit",
    "system_emulated",
    "system",
    "mypy",""",
)

s.replace(
    "noxfile.py",
    """\"--quiet\",
            f\"--junitxml=system_\{session.python\}_sponge_log.xml\",
            system_test""",
    """\"--verbose\",
            f\"--junitxml=system_{session.python}_sponge_log.xml\",
            system_test""",
)

# Add pytype support
s.replace(
    ".gitignore",
    """\
.pytest_cache
""",
    """\
.pytest_cache
.pytype
""",
)

s.replace(
    ".gitignore",
    """\
pylintrc
pylintrc.test
""",
    """\
pylintrc
pylintrc.test
.make/**
""",
)

s.replace(
    "setup.cfg",
    """\
universal = 1
""",
    """\
universal = 1
[pytype]
python_version = 3.8
inputs =
    google/cloud/
exclude =
    tests/
output = .pytype/
# Workaround for https://github.com/google/pytype/issues/150
disable = pyi-error
""",
)

s.replace(
    "noxfile.py",
    """\
BLACK_VERSION = "black==22.3.0"
""",
    """\
PYTYPE_VERSION = "pytype==2020.7.24"
BLACK_VERSION = "black==22.3.0"
""",
)

s.replace(
    "noxfile.py",
    """\
@nox.session\(python=DEFAULT_PYTHON_VERSION\)
def lint_setup_py\(session\):
""",
    '''\
@nox.session(python="3.7")
def pytype(session):
    """Verify type hints are pytype compatible."""
    session.install(PYTYPE_VERSION)
    session.run("pytype",)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session):
    """Verify type hints are mypy compatible."""
    session.install("-e", ".")
    session.install("mypy", "types-setuptools")
    # TODO: also verify types on tests, all of google package
    session.run("mypy", "-p", "google.cloud.firestore", "--no-incremental")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
''',
)

s.replace(
    ".coveragerc",
    """\
    raise NotImplementedError
omit =
""",
    """\
    raise NotImplementedError
    # Ignore setuptools-less fallback
    except pkg_resources.DistributionNotFound:
omit =
""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

s.replace(
    ".kokoro/build.sh",
    "# Setup service account credentials.",
    """\
# Setup firestore account credentials
export FIRESTORE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/firebase-credentials.json

# Setup service account credentials.""",
)


# Add a section on updating conformance tests to contributing.
s.replace(
    "CONTRIBUTING.rst",
    "\nTest Coverage",
    """*************
Updating Conformance Tests
**************************

The firestore client libraries use a shared set of conformance tests, the source of which can be found at https://github.com/googleapis/conformance-tests.

To update the copy of these conformance tests used by this repository, run the provided Makefile:

   $ make -f Makefile_v1

*************
Test Coverage"""
)

