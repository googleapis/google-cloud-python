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


name = "googleapis-common-protos"
description = "Common protobufs used in Google APIs"
version = "1.59.1"
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    "protobuf>=3.19.5,<5.0.0.dev0,!=3.20.0,!=3.20.1,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
]

extras_require = {"grpc": ["grpcio >= 1.44.0, <2.0.0.dev0"]}

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

packages = [
    package
    for package in setuptools.PEP420PackageFinder.find()
    if package.startswith("google")
]

setuptools.setup(
    name=name,
    version=version,
    author="Google LLC",
    author_email="googleapis-packages@google.com",
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
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=dependencies,
    extras_require=extras_require,
    license="Apache-2.0",
    packages=packages,
    package_data={"": ["*.proto"]},
    python_requires=">=3.7",
    namespace_packages=["google", "google.logging"],
    url="https://github.com/googleapis/python-api-common-protos",
    include_package_data=True,
)
