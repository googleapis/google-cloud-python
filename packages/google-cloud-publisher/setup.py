# Copyright 2025 Google LLC
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
#

import io
import os
from setuptools import find_namespace_packages, setup

# Package metadata.
name = "google-cloud-publisher"
description = "Google Cloud Publisher API client library"
version = "0.1.0"
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    "google-api-core[grpc] >= 1.34.0, <3.0.0dev",
    "proto-plus >= 1.22.0, <2.0.0dev",
]

package_root = os.path.abspath(os.path.dirname(__file__))

# Read the contents of the README file.
with io.open(os.path.join(package_root, "README.md"), "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    license="Apache 2.0",
    url="https://github.com/googleapis/google-cloud-python",
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
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    packages=find_namespace_packages(include=["google.cloud.*"]),
    namespace_packages=["google", "google.cloud"],
    platforms="Posix; MacOS X; Windows",
    include_package_data=True,
    install_requires=dependencies,
    python_requires=">=3.7",
    zip_safe=False,
)
