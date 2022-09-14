# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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

name = "gapic-generator"
description = "Google API Client Generator for Python"
url = "https://github.com/googleapis/gapic-generator-python"
version = "1.4.2"
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    "click >= 6.7",
    "google-api-core >= 2.8.0",
    "googleapis-common-protos >= 1.55.0",
    "grpcio >= 1.24.3",
    "jinja2 >= 2.10",
    "protobuf >= 3.18.0, <4.0.0dev",
    "pypandoc >= 1.4",
    "PyYAML >= 5.1.1",
    "grpc-google-iam-v1 >= 0.12.4, < 1.0.0dev",
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    entry_points="""[console_scripts]
        protoc-gen-dump=gapic.cli.dump:dump
        protoc-gen-python_gapic=gapic.cli.generate:generate
    """,
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    license="Apache 2.0",
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    url=url,
    classifiers=[
        release_status,
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms="Posix; MacOS X",
    python_requires=">=3.7",
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False,
)
