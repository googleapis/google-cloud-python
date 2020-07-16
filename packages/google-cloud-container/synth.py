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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta1", "v1"]

# ----------------------------------------------------------------------------
# Generate container GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="container",
        version=version,
        bazel_target=f"//google/container/{version}:container-{version}-py",
        include_protos=True,
        proto_output_path=f"google/container_{version}/proto",
    )

    s.move(library / "google/container", "google/cloud/container")
    s.move(
        library / f"google/container_{version}",
        f"google/cloud/container_{version}"
    )
    s.move(library / "tests")
    s.move(library / "scripts")
    s.move(library / "docs", excludes=[library / "docs/index.rst"])

    # Fix namespace
    s.replace(
        f"google/cloud/**/*.py",
        f"google.container_{version}",
        f"google.cloud.container_{version}",
    )
    s.replace(
        f"tests/unit/gapic/**/*.py",
        f"google.container_{version}",
        f"google.cloud.container_{version}",
    )
    s.replace(
        f"google/cloud/**/*.py",
        f"google.container_{version}",
        f"google.cloud.container_{version}",
    )
    s.replace(
        f"docs/**/*.rst",
        f"google.container_{version}",
        f"google.cloud.container_{version}",
    )

# Issues exist where python files should define the source encoding
# https://github.com/googleapis/gapic-generator/issues/2097
s.replace(
    "google/**/proto/*_pb2.py",
    r"(^.*$\n)*",
    r"# -*- coding: utf-8 -*-\n\g<0>")


# Workaround https://github.com/googleapis/gapic-generator/issues/2449
s.replace(
    "google/**/proto/cluster_service_pb2.py",
    r"nodePool>\n",
    r"nodePool>`__\n",
)
s.replace(
    "google/**/proto/cluster_service_pb2.py",
    r"(\s+)`__ instead",
    r"\g<1>instead",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file


# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

# Temporarily disable warnings due to
# https://github.com/googleapis/gapic-generator-python/issues/525
s.replace("noxfile.py", '[\"\']-W[\"\']', '# "-W"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
