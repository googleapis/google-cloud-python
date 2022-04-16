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

common = gcp.CommonTemplates()

default_version = "v2"

for library in s.get_staging_dirs(default_version):
    if library.name == "v2":
        # Fix generated unit tests
        s.replace(
            library / "tests/unit/gapic/logging_v2/test_logging_service_v2.py",
            "MonitoredResource\(\s*type_",
            "MonitoredResource(type"
        )

    s.move(
        library,
        excludes=[
            "setup.py",
            "README.rst",
            "google/cloud/logging/__init__.py",  # generated types are hidden from users
            "google/cloud/logging_v2/__init__.py",
            "docs/index.rst",
            "docs/logging_v2",  # Don't include gapic library docs. Users should use the hand-written layer instead
            "scripts/fixup_logging_v2_keywords.py",  # don't include script since it only works for generated layer
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=95,
    cov_level=99,
    microgenerator=True,
    system_test_external_dependencies=[
        "google-cloud-bigquery",
        "google-cloud-pubsub",
        "google-cloud-storage",
        "google-cloud-testutils",
    ],
    unit_test_external_dependencies=["flask", "webob", "django"],
    samples=True,
)
s.move(templated_files, 
    excludes=[
        ".coveragerc", 
        "docs/multiprocessing.rst",
        ".github/workflows", # exclude gh actions as credentials are needed for tests
        ".github/auto-label.yaml",
        ])

# adjust .trampolinerc for environment tests
s.replace(
    ".trampolinerc",
    "required_envvars[^\)]*\)",
    "required_envvars+=()"
)
s.replace(
    ".trampolinerc",
    "pass_down_envvars\+\=\(",
    'pass_down_envvars+=(\n    "ENVIRONMENT"\n    "RUNTIME"'
)

# don't lint environment tests
s.replace(
    ".flake8",
    "exclude =",
    'exclude =\n  # Exclude environment test code.\n  tests/environment/**\n'
)

# use conventional commits for renovate bot
s.replace(
    "renovate.json",
    """}
}""",
    """},
  "semanticCommits": "enabled"
}"""
)

# --------------------------------------------------------------------------
# Samples templates
# --------------------------------------------------------------------------

python.py_samples()

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

