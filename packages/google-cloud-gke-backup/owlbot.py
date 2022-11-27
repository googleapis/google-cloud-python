# Copyright 2022 Google LLC
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

import json
from pathlib import Path
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get(
    "default_version"
)

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # Apply workarounds to fix the generated docstrings.
    # Issue filed upstream in https://github.com/googleapis/gapic-generator-python/issues/1345
    s.replace(
        library / f"google/cloud/gke_backup_{library.name}/**/*.py",
        """must:[\n]*
                 - be between 1 and 63 characters long
                \(inclusive\)  - consist of only
                lower-case ASCII letters, numbers, and
                dashes  - start with a lower-case letter
                 - end with a lower-case letter or
                number""",
        """must:

                 - be between 1 and 63 characters long (inclusive) 
                 - consist of only lower-case ASCII letters, numbers, and dashes
                 - start with a lower-case letter
                 - end with a lower-case letter or number"""
    )
    s.replace(
        library / f"google/cloud/gke_backup_{library.name}/**/*.py",
        """must:[\n]*
            - be between 1 and 63 characters long
            \(inclusive\) - consist of only lower-case ASCII
            letters, numbers, and dashes - start with a
            lower-case letter
            - end with a lower-case letter or number
            - be unique within the set of BackupPlans in
            this location""",
        """must:

            - be between 1 and 63 characters long (inclusive)
            - consist of only lower-case ASCII letters, numbers, and dashes 
            - start with a lower-case letter
            - end with a lower-case letter or number
            - be unique within the set of BackupPlans in this location""")
    s.replace(
        library / f"google/cloud/gke_backup_{library.name}/**/*.py",
        """must:[\n]*
             - be between 1 and 63 characters long
            \(inclusive\)  - consist of only lower-case ASCII
            letters, numbers, and dashes  - start with a
            lower-case letter
             - end with a lower-case letter or number
             - be unique within the set of Backups in this
            BackupPlan""",
        """must:

            - be between 1 and 63 characters long (inclusive)  
            - consist of only lower-case ASCII letters, numbers, and dashes 
            - start with a lower-case letter
            - end with a lower-case letter or number
            - be unique within the set of Backups in this BackupPlan""")         
    s.replace(
        library / f"google/cloud/gke_backup_{library.name}/**/*.py",
        """must:[\n]*
             - be between 1 and 63 characters long
            \(inclusive\)  - consist of only lower-case ASCII
            letters, numbers, and dashes  - start with a
            lower-case letter
             - end with a lower-case letter or number
             - be unique within the set of RestorePlans in
            this location""",
        """must:

            - be between 1 and 63 characters long (inclusive)
            - consist of only lower-case ASCII letters, numbers, and dashes
            - start with a lower-case letter
            - end with a lower-case letter or number
            - be unique within the set of RestorePlans in this location""")
    s.replace(
        library / f"google/cloud/gke_backup_{library.name}/**/*.py",
        """must:[\n]*
             - be between 1 and 63 characters long
            \(inclusive\)  - consist of only lower-case ASCII
            letters, numbers, and dashes  - start with a
            lower-case letter
             - end with a lower-case letter or number
             - be unique within the set of Restores in this
            RestorePlan.""",
        """must:

            - be between 1 and 63 characters long (inclusive)
            - consist of only lower-case ASCII letters, numbers, and dashes
            - start with a lower-case letter
            - end with a lower-case letter or number
            - be unique within the set of Restores in this RestorePlan.""")

    s.replace(library / f"google/cloud/gke_backup_{library.name}/services/**/*.py",
    """be unique within the set of Backups
                in this BackupPlan""",
    """be unique within the set of Backups in this BackupPlan""")
    s.replace(library / f"google/cloud/gke_backup_{library.name}/services/**/*.py",
    """be unique within the set of Restores
                in this RestorePlan""",
    """be unique within the set of Restores in this RestorePlan""")
    s.replace(library / f"google/cloud/gke_backup_{library.name}/services/**/*.py",
    """be unique within the set of
                RestorePlans in this location""",
    """be unique within the set of RestorePlans in this location""")

    # workaround issue with docstrings
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*\n""",
        "``projects/*/locations/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*/backupPlans/\\\\\*\n""",
        "``projects/*/locations/*/backupPlans/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*/backupPlans/\*.\n""",
        "``projects/*/locations/*/backupPlans/*``.\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*/backupPlans/\*/backups/\*\n""",
        "``projects/*/locations/*/backupPlans/*/backups/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*/backupPlans/\*/backups/\*.\n""",
        "``projects/*/locations/*/backupPlans/*/backups/*``.\n",
    )

    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/backupPlans/\*/backups/\*/volumeBackups/\\\\\*\n",
        "``projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/backupPlans/\*/backups/\*/volumeBackups/\*.\n",
        "``projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*``.\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/restorePlans/\\\\\*\n",
        "``projects/*/locations/*/restorePlans/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/restorePlans/\*.\n",
        "``projects/*/locations/*/restorePlans/*``.\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/restorePlans/\*/restores/\*\n",
        "``projects/*/locations/*/restorePlans/*/restores/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/restorePlans/\*/restores/\*/volumeRestores/\\\\\*\n",
        "``projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*``\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        "projects/\\\ \*/locations/\*/restorePlans/\*/restores/\*/volumeRestores/\*.\n",
        "``projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*``.\n",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """-  projects/\\\ \*/locations/\*/clusters/\\\\\*
            -  projects/\\\ \*/zones/\*/clusters/\\\\\*""",
        """-  ``projects/*/locations/*/clusters/*``
            -  ``projects/*/zones/*/clusters/*``""",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """-  projects/\\\ \*/locations/\*/clusters/\\\\\*
                -  projects/\\\ \*/zones/\*/clusters/\\\\\*""",
        """-  ``projects/*/locations/*/clusters/*``
                -  ``projects/*/zones/*/clusters/*``""",
    )
    s.replace(
        library / f"google/cloud/**/*.py",
        """projects/\\\ \*/locations/\*/keyRings/\*/cryptoKeys/\*""",
        """``projects/*/locations/*/keyRings/*/cryptoKeys/*``""",
    )

    s.move([library], excludes=["**/gapic_version.py"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)
