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

AUTOSYNTH_MULTIPLE_PRS = True
AUTOSYNTH_MULTIPLE_COMMITS = True

common = gcp.CommonTemplates()

def update_fixup_scripts(library):
    # Add message for missing 'libcst' dependency
    s.replace(
        library / "scripts/fixup*.py",
        """\
    import libcst as cst
    """,
        """\

    try:
        import libcst as cst
    except ImportError:
        raise ImportError('Run `python -m pip install "libcst >= 0.2.5"` to install libcst.')


    """,
    )

# This library ships clients for 3 different APIs,
# firestore, firestore_admin and firestore_bundle
default_version = "v1"
admin_default_version = "v1"
bundle_default_version = "v1"

for library in s.get_staging_dirs(default_version):
    if library.parent.absolute() == 'firestore':
        s.move(
            library / f"google/cloud/firestore_{library.name}",
            f"google/cloud/firestore_{library.name}",
            excludes=[f"google/cloud/firestore_{library.name}/__init__.py"],
        )

        s.move(library / f"tests/", f"tests")
        update_fixup_scripts(library)
        s.move(library / "scripts")

for library in s.get_staging_dirs(admin_default_version):
    if library.parent.absolute() == 'admin':
        s.move(
            library / f"google/cloud/firestore_admin_{library.name}",
            f"google/cloud/firestore_admin_{library.name}",
            excludes=[f"google/cloud/firestore_admin_{library.name}/__init__.py"],
        )
        s.move(library / f"tests", f"tests")
        update_fixup_scripts(library)
        s.move(library / "scripts")

for library in s.get_staging_dirs(bundle_default_version):
    if library.parent.absolute() == 'bundle':
        s.replace(
            library / "google/cloud/firestore_bundle/types/bundle.py",
            "from google.firestore.v1 import document_pb2 as gfv_document  # type: ignore\n",
            "from google.cloud.firestore_v1.types import document as gfv_document\n",
        )

        s.replace(
            library / "google/cloud/firestore_bundle/types/bundle.py",
            "from google.firestore.v1 import query_pb2 as query  # type: ignore\n",
            "from google.cloud.firestore_v1.types import query\n",
        )

        s.replace(
            library / "google/cloud/firestore_bundle/__init__.py",
            "from .types.bundle import NamedQuery\n",
            "from .types.bundle import NamedQuery\n\nfrom .bundle import FirestoreBundle\n",
        )

        s.replace(
            library / "google/cloud/firestore_bundle/__init__.py",
            "\'BundledQuery\',",
            "\"BundledQuery\",\n    \"FirestoreBundle\",",
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
    unit_test_external_dependencies=["aiounittest"],
    system_test_external_dependencies=["pytest-asyncio"],
    microgenerator=True,
    cov_level=100,
)

s.move(
    templated_files,
)

s.replace(
    "noxfile.py",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "FIRESTORE_APPLICATION_CREDENTIALS",
)

s.replace(
    "noxfile.py",
    '"--quiet", system_test',
    '"--verbose", system_test',
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
BLACK_VERSION = "black==19.10b0"
""",
    """\
PYTYPE_VERSION = "pytype==2020.7.24"
BLACK_VERSION = "black==19.10b0"
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
    """Run pytype
    """
    session.install(PYTYPE_VERSION)
    session.run("pytype",)
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
