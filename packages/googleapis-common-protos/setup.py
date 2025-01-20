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

import io
import os

import setuptools
from setuptools import find_namespace_packages

name = "googleapis-common-protos"
description = "Common protobufs used in Google APIs"
version = "1.67.0"
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    "protobuf>=3.20.2,<6.0.0.dev0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
]

extras = {"grpc": ["grpcio >= 1.44.0, <2.0.0.dev0"]}
url = "https://github.com/googleapis/google-cloud-python/tree/main/packages/googleapis-common-protos"

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

packages = [
    package
    for package in setuptools.find_namespace_packages(exclude=("tests*", "testing*"))
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
    url=url,
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    python_requires=">=3.7",
    install_requires=dependencies,
    extras_require=extras,
    include_package_data=True,
    zip_safe=False,
)
