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

def update_fixup_scripts(path):
    # Add message for missing 'libcst' dependency
    s.replace(
        library / "scripts" / path,
        """import libcst as cst""",
        """try:
    import libcst as cst
except ImportError:
    raise ImportError('Run `python -m pip install "libcst >= 0.2.5"` to install libcst.')


    """,
    )

for library in s.get_staging_dirs(default_version=firestore_default_version):
    s.move(library / f"google/cloud/firestore_{library.name}", excludes=[f"__init__.py", "noxfile.py"])
    s.move(library / f"tests/", f"tests")
    fixup_script_path = "fixup_firestore_v1_keywords.py"
    update_fixup_scripts(fixup_script_path)
    s.move(library / "scripts" / fixup_script_path)

for library in s.get_staging_dirs(default_version=firestore_admin_default_version):
    s.move(library / f"google/cloud/firestore_admin_{library.name}", excludes=[f"__init__.py", "noxfile.py"])
    s.move(library / f"tests", f"tests")
    fixup_script_path = "fixup_firestore_admin_v1_keywords.py"
    update_fixup_scripts(fixup_script_path)
    s.move(library / "scripts" / fixup_script_path)

for library in s.get_staging_dirs():
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
        excludes=["noxfile.py"],
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
    default_python_version="3.14",
    system_test_python_versions=["3.14"],
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"],
)

s.move(templated_files,
       excludes=[".github/**", ".kokoro/**", "renovate.json"])

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
