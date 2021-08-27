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

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Issues exist where python files should define the source encoding
    # https://github.com/googleapis/gapic-generator/issues/2097
    s.replace(
        library / "google/**/proto/*_pb2.py",
        r"(^.*$\n)*",
        r"# -*- coding: utf-8 -*-\n\g<0>")

    # Workaround https://github.com/googleapis/gapic-generator/issues/2449
    s.replace(
        library / "google/**/proto/cluster_service_pb2.py",
        r"nodePool>\n",
        r"nodePool>`__\n",
    )
    s.replace(
        library / "google/**/proto/cluster_service_pb2.py",
        r"(\s+)`__ instead",
        r"\g<1>instead",
    )

    # Fix namespace
    s.replace(
        library / f"google/**/*.py",
        f"google.container_{library.name}",
        f"google.cloud.container_{library.name}",
    )

    s.replace(
        library / f"tests/unit/gapic/**/*.py",
        f"google.container_{library.name}",
        f"google.cloud.container_{library.name}",
    )

    s.replace(
        library / f"docs/**/*.rst",
        f"google.container_{library.name}",
        f"google.cloud.container_{library.name}",
    )

    # Fix package name
    s.replace(
        library / "google/**/*.py",
        "google-container",
        "google-cloud-container"
    )

    s.move(library / "google/container", "google/cloud/container")
    s.move(
        library / f"google/container_{library.name}",
        f"google/cloud/container_{library.name}"
    )

    # Fix DeprecationWarning
    # Fix incorrect DeprecationWarning
    # Fixed in https://github.com/googleapis/gapic-generator-python/pull/943
    s.replace(
        "google/**/*client.py",
        "warnings\.DeprecationWarning",
        "DeprecationWarning"
    )
    s.move(library / "tests")
    s.move(library / "scripts")
    s.move(library / "docs", excludes=["index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

python.py_samples(skip_readmes=True)

# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

# Customize CONTRIBUTING.rst to replace master with main
s.replace(
    "CONTRIBUTING.rst",
    "fetch and merge changes from upstream into master",
    "fetch and merge changes from upstream into main",
)

s.replace(
    "CONTRIBUTING.rst",
    "git merge upstream/master",
    "git merge upstream/main",
)

s.replace(
    "CONTRIBUTING.rst",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"master\"""",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"main\"""",
)

s.replace(
    "CONTRIBUTING.rst",
    "remote \(``master``\)",
    "remote (``main``)",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/CONTRIBUTING.rst",
    "blob/main/CONTRIBUTING.rst",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/noxfile.py",
    "blob/main/noxfile.py",
)

s.replace(
    "docs/conf.py",
    "master_doc",
    "root_doc",
)

s.replace(
    "docs/conf.py",
    "# The master toctree document.",
    "# The root toctree document.",
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

# Temporarily disable warnings due to
# https://github.com/googleapis/gapic-generator-python/issues/525
s.replace("noxfile.py", '[\"\']-W[\"\']', '# "-W"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
