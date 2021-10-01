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
# which are bigtable and bigtable/admin.
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
# BigTable and BigTable Admin
bigtable_default_version = "v2"
bigtable_admin_default_version = "v2"

for library in get_staging_dirs(bigtable_default_version, "bigtable"):
    s.move(library / "google/cloud/bigtable_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

for library in get_staging_dirs(bigtable_admin_default_version, "bigtable_admin"):
    s.move(library / "google/cloud/bigtable_admin_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    split_system_tests=True,
    microgenerator=True,
    cov_level=100,
)

s.move(templated_files, excludes=[".coveragerc", ".github/CODEOWNERS"])

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
@nox.session(python="3.8")
def system_emulated(session):
    import subprocess
    import signal

    try:
        subprocess.call(["gcloud", "--version"])
    except OSError:
        session.skip("gcloud not found but required for emulator support")

    # Currently, CI/CD doesn't have beta component of gcloud.
    subprocess.call(["gcloud", "components", "install", "beta", "bigtable"])

    hostport = "localhost:8789"
    p = subprocess.Popen(
        ["gcloud", "beta", "emulators", "bigtable", "start", "--host-port", hostport]
    )

    session.env["BIGTABLE_EMULATOR_HOST"] = hostport
    system(session)

    # Stop Emulator
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)

"""

place_before(
    "noxfile.py",
    "@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)\n"
    "def system(session):",
    system_emulated_session,
    escape="()"
)

# add system_emulated nox session
s.replace("noxfile.py",
    """nox.options.sessions = \[
    "unit",
    "system",""",
    """nox.options.sessions = [
    "unit",
    "system_emulated",
    "system",""",
)


# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(samples=True)
for path in sample_files:
    s.move(path)

# Note: python-docs-samples is not yet using 'main':
#s.replace(
#    "samples/**/*.md",
#    r"python-docs-samples/blob/master/",
#    "python-docs-samples/blob/main/",
#)
s.replace(
    "samples/**/*.md",
    r"google-cloud-python/blob/master/",
    "google-cloud-python/blob/main/",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
