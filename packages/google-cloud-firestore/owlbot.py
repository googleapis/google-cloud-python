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
    s.move(library / f"google/cloud/firestore_{library.name}", excludes=[f"__init__.py", "**/gapic_version.py", "noxfile.py"])
    s.move(library / f"tests/", f"tests")
    update_fixup_scripts(library)
    s.move(library / "scripts")

for library in get_staging_dirs(default_version=firestore_admin_default_version, sub_directory="firestore_admin"):
    s.move(library / f"google/cloud/firestore_admin_{library.name}", excludes=[f"__init__.py", "**/gapic_version.py", "noxfile.py"])
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
        "from google.cloud.bundle import gapic_version as package_version\n",
        "from google.cloud.firestore_bundle import gapic_version as package_version\n",
    )

    s.replace(
        library / "google/cloud/bundle/__init__.py",
        "\'BundledQuery\',",
        "\"BundledQuery\",\n\"FirestoreBundle\",",)

    s.move(
        library / f"google/cloud/bundle",
        f"google/cloud/firestore_bundle",
        excludes=["**/gapic_version.py", "noxfile.py"],
    )
    s.move(library / f"tests", f"tests")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    unit_test_external_dependencies=["aiounittest", "six", "freezegun"],
    system_test_external_dependencies=["pytest-asyncio", "six"],
    microgenerator=True,
    cov_level=100,
    split_system_tests=True,
    default_python_version="3.13",
    system_test_python_versions=["3.13"],
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"],
)

s.move(templated_files,
       excludes=[".github/release-please.yml", "renovate.json"])

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

s.replace(
    ".kokoro/build.sh",
    "# Setup service account credentials.",
    """\
# Setup firestore account credentials
export FIRESTORE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/firebase-credentials.json

# Setup service account credentials.""",
)
