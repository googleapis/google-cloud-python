# Copyright 2021 Google LLC
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

import pathlib
import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

extras_by_python = {
    # Use a middle version of Python to test when no extras are installed.
    "3.9": []
}
extras = ["tqdm"]
templated_files = common.py_library(
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11"],
    system_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11"],
    cov_level=96,
    unit_test_external_dependencies=["freezegun"],
    unit_test_extras=extras,
    unit_test_extras_by_python=extras_by_python,
    system_test_extras=extras,
    intersphinx_dependencies={
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/",
        "pydata-google-auth": "https://pydata-google-auth.readthedocs.io/en/latest/",
    },
)
s.move(
    templated_files,
    excludes=[
        # pandas-gbq was originally licensed BSD-3-Clause License
        "LICENSE",
        # Multi-processing note isn't relevant, as pandas_gbq is responsible for
        # creating clients, not the end user.
        "docs/multiprocessing.rst",
        "noxfile.py",
	    "README.rst",
    ],
)

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

s.replace(
    [".github/header-checker-lint.yml"], '"Google LLC"', '"pandas-gbq Authors"',
)

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=96")

# Add environment variables to build.sh to support conda virtualenv 
# installations
s.replace(
    [".kokoro/build.sh"],
    "export PYTHONUNBUFFERED=1",
    r"""export PYTHONUNBUFFERED=1
export CONDA_EXE=/root/conda/bin/conda
export CONDA_PREFIX=/root/conda
export CONDA_PROMPT_MODIFIER=(base) 
export _CE_CONDA=
export CONDA_SHLVL=1
export CONDA_PYTHON_EXE=/root/conda/bin/python
export CONDA_DEFAULT_ENV=base
export PATH=/root/conda/bin:/root/conda/condabin:${PATH}
""",
)


# Enable display of all environmental variables, not just KOKORO related vars
s.replace(
    [".kokoro/build.sh"],
    r"env \| grep KOKORO",
    "env",
)


# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
