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


package_root = os.path.abspath(os.path.dirname(__file__))

# Package metadata.

name = "google-cloud-bigtable"
description = "Google Cloud Bigtable API client library"

version = {}
with open(os.path.join(package_root, "google/cloud/bigtable/gapic_version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]


# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    "google-api-core[grpc] >= 2.17.0, <3.0.0",
    "google-cloud-core >= 1.4.4, <3.0.0",
    "google-auth >= 2.14.1, <3.0.0,!=2.24.0,!=2.25.0",
    "grpc-google-iam-v1 >= 0.12.4, <1.0.0",
    "proto-plus >= 1.22.3, <2.0.0",
    "proto-plus >= 1.25.0, <2.0.0; python_version>='3.13'",
    "protobuf>=3.20.2,<7.0.0,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
    "google-crc32c>=1.5.0, <2.0.0dev",
]
extras = {"libcst": "libcst >= 0.2.5"}


# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package
    for package in setuptools.find_namespace_packages()
    if package.startswith("google")
]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    license="Apache 2.0",
    url="https://github.com/googleapis/python-bigtable",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    scripts=[
        "scripts/fixup_bigtable_v2_keywords.py",
        "scripts/fixup_admin_v2_keywords.py",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
