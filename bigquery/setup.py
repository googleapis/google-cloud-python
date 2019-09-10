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

import io
import os

import setuptools


# Package metadata.

name = "google-cloud-bigquery"
description = "Google BigQuery API client library"
version = "1.19.0"
# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    'enum34; python_version < "3.4"',
    "google-cloud-core >= 1.0.3, < 2.0dev",
    "google-resumable-media >= 0.3.1",
    "protobuf >= 3.6.0",
]
extras = {
    "bqstorage": [
        "google-cloud-bigquery-storage >= 0.6.0, <2.0.0dev",
        # Bad Linux release for 0.14.0.
        # https://issues.apache.org/jira/browse/ARROW-5868
        "pyarrow>=0.13.0, != 0.14.0",
    ],
    "pandas": ["pandas>=0.17.1"],
    # Exclude PyArrow dependency from Windows Python 2.7.
    'pyarrow: platform_system != "Windows" or python_version >= "3.4"': [
        # Bad Linux release for 0.14.0.
        # https://issues.apache.org/jira/browse/ARROW-5868
        "pyarrow>=0.4.1, != 0.14.0"
    ],
    "tqdm": ["tqdm >= 4.0.0, <5.0.0dev"],
    "fastparquet": ["fastparquet", "python-snappy"],
}

all_extras = []

for extra in extras:
    if extra == "fastparquet":
        # Skip fastparquet from "all" because it is redundant with pyarrow and
        # creates a dependency on pre-release versions of numpy. See:
        # https://github.com/googleapis/google-cloud-python/issues/8549
        continue
    all_extras.extend(extras[extra])

extras["all"] = all_extras

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package for package in setuptools.find_packages() if package.startswith("google")
]

# Determine which namespaces are needed.
namespaces = ["google"]
if "google.cloud" in packages:
    namespaces.append("google.cloud")


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    license="Apache 2.0",
    url="https://github.com/GoogleCloudPlatform/google-cloud-python",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    namespace_packages=namespaces,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    include_package_data=True,
    zip_safe=False,
)
