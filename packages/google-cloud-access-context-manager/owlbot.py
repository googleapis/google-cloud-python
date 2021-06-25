# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import synthtool as s
import synthtool.gcp as gcp
from synthtool import tmp
from synthtool.languages import python
from synthtool.sources import git

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------
common = gcp.CommonTemplates()
templated_files = common.py_library(microgenerator=True)
s.move(
    templated_files, excludes=[".coveragerc", ".gitignore",],
)

# ----------------------------------------------------------------------------
#  Customize noxfile.py
# ----------------------------------------------------------------------------

old_sessions = """
    "unit",
    "system",
    "cover",
    "lint",
"""

new_sessions = """
    "system",
    "lint",
    "test",
    "generate_protos",
"""

# Remove `unit` and `cover` sessions.
# Add `test` and `generate_protos` sessions.
s.replace("noxfile.py", old_sessions, new_sessions)

# Remove unit* sessions
s.replace("noxfile.py",
    """@nox.session\(python=UNIT_TEST_PYTHON_VERSIONS\)
def unit\(session\):""",
    """def unit(session):""",
)

# Remove cover session
s.replace("noxfile.py",
    """@nox.session\(python=DEFAULT_PYTHON_VERSION\)
def cover.*
    session.run\("coverage", "erase"\)""",
    """""",
    flags=re.MULTILINE | re.DOTALL,
)

def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, '\\' + c)
    s.replace([path], text, replacement)

custom_nox_sessions = """
@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
@nox.parametrize(
    "library", ["python-asset"], ids=["asset"],
)
def test(session, library):
    \"\"\"Run tests from a downstream libraries.
    To verify that any changes we make here will not break downstream libraries, clone
    a few and run their unit and system tests.
    NOTE: The unit and system test functions above are copied from the templates.
    They will need to be updated when the templates change.
    \"\"\"
    try:
        session.run("git", "-C", library, "pull", external=True)
    except nox.command.CommandFailed:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{library}",
            external=True,
        )

    session.cd(library)
    unit(session)
    # system tests are run 3.7 only
    if session.python == "3.7":
        system(session)


@nox.session(python="3.8")
def generate_protos(session):
    \"\"\"Generates the protos using protoc.
    Some notes on the `google` directory:
    1. The `_pb2.py` files are produced by protoc.
    2. The .proto files are non-functional but are left in the repository
       to make it easier to understand diffs.
    3. The `google` directory also has `__init__.py` files to create proper modules.
       If a new subdirectory is added, you will need to create more `__init__.py`
       files.
    \"\"\"
    session.install("grpcio-tools")
    protos = [str(p) for p in (pathlib.Path(".").glob("google/**/*.proto"))]

    # Clone googleapis/api-common-protos
    api_common_protos = "api-common-protos"
    try:
        session.run("git", "-C", api_common_protos, "pull", external=True)
    except nox.command.CommandFailed:
        session.run(
            "git",
            "clone",
            "--single-branch",
            f"https://github.com/googleapis/{api_common_protos}",
            external=True,
        )

    session.run(
        "python",
        "-m",
        "grpc_tools.protoc",
        "--proto_path=api-common-protos",
        "--proto_path=.",
        "--python_out=.",
        *protos,
    )
"""

# `google-cloud-context-manager` contains only protos
# and has a customized `test` session to test
# downstream client `google-cloud-asset`
place_before(
    "noxfile.py",
    "@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)\n"
    "def system(session):",
    custom_nox_sessions,
    escape="()"
)

s.shell.run(["nox", "-s", "generate_protos"])
s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()

LICENSE = """
# Copyright 2020 Google LLC
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
# limitations under the License."""

PB2_GRPC_HEADER = r"""(\# Generated by the gRPC Python protocol compiler plugin\. DO NOT EDIT!$)
(.*?$)"""

s.replace(
    "**/*_pb2_grpc.py",
    PB2_GRPC_HEADER,
    fr"{LICENSE}\n\n\g<1>\n\n\g<2>",  # add line breaks to avoid stacking replacements
)
