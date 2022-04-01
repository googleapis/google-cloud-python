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
import re

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python
import logging

AUTOSYNTH_MULTIPLE_COMMITS = True

logging.basicConfig(level=logging.DEBUG)

common = gcp.CommonTemplates()

default_version = "v3"

for library in s.get_staging_dirs(default_version):
    # Synth hack due to googleapis and python-api-common-protos out of sync.
    for pattern in [
        "monitored_resource_types=\['monitored_resource_types_value'\],",
        "assert response.monitored_resource_types == \['monitored_resource_types_value'\]",
        "launch_stage=launch_stage_pb2.LaunchStage.UNIMPLEMENTED,",
        "assert response.launch_stage == launch_stage_pb2.LaunchStage.UNIMPLEMENTED",
    ]:
        s.replace(library / "tests/unit/gapic/monitoring_v3/test_*.py",
            pattern,
            ""
        )

    # Synth hack due to microgenerator uses "type_" while api-common-protos uses "type".
    for file in ["test_uptime_check_service.py", "test_metric_service.py"]:
        s.replace(library / f"tests/unit/gapic/monitoring_v3/{file}",
            "type_",
            "type"
        )

    # Comment out broken path helper 'metric_descriptor_path'
    # https://github.com/googleapis/gapic-generator-python/issues/701
    s.replace(
        library / "google/cloud/**/metric_service/client.py",
        "(@staticmethod\n\s+def metric_descriptor_path.*?return m\.groupdict\(\) if m else \{\})",
        """'''\g<1>'''""",
        re.MULTILINE| re.DOTALL
    )

    s.replace(
        library / "google/cloud/**/metric_service/async_client.py",
        """(metric_descriptor_path =.*?parse_metric_descriptor_path = staticmethod\(.*?\))""",
        '''"""\g<1>"""''',
        re.MULTILINE| re.DOTALL
    )

    s.replace(
        library / "tests/**/test_metric_service.py",
        "(def test_metric_descriptor_path.*?def test_parse_metric_descriptor_path.*?)def",
        '''"""\g<1>"""\ndef''',
        re.MULTILINE| re.DOTALL
    )

    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/monitoring_{library.name}/types/service.py",
                r""".
    Attributes:""",
                r""".\n
    Attributes:""",
    )

    # don't copy nox.py, setup.py, README.rst, docs/index.rst
    excludes = ["nox.py", "setup.py", "README.rst", "docs/index.rst"]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    unit_test_extras=["pandas"],
    system_test_extras=["pandas"],
    cov_level=99
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# master --> main edits; context: https://github.com/googleapis/google-cloud-python/issues/10579
# ----------------------------------------------------------------------------

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

s.replace(
    ".kokoro/test-samples-impl.sh",
    "https://github.com/googleapis/repo-automation-bots/tree/master/packages/flakybot.",
    "https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.",
)

s.replace(
    ".kokoro/build.sh",
    "https://github.com/googleapis/repo-automation-bots/tree/master/packages/flakybot.",
    "https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.",
)

s.replace(
    "CONTRIBUTING.rst",
    "master",
    "main",
)

# Revert the change from above, because kubernetes is still using master:
s.replace(
    "CONTRIBUTING.rst",
    r"https://github.com/kubernetes/community/blob/main/contributors/guide/pull-requests.md#best-practices-for-faster-reviews",
    r"https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md#best-practices-for-faster-reviews",
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples(skip_readmes=True)

# Work around bug in templates https://github.com/googleapis/synthtool/pull/1335
s.replace(".github/workflows/unittest.yml", "--fail-under=100", "--fail-under=99")

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
