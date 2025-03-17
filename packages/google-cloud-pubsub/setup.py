# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

import setuptools  # type: ignore

package_root = os.path.abspath(os.path.dirname(__file__))

name = "google-cloud-pubsub"


description = "Google Cloud Pub/Sub API client library"

version = {}
with open(os.path.join(package_root, "google/pubsub/gapic_version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

if version[0] == "0":
    release_status = "Development Status :: 4 - Beta"
else:
    release_status = "Development Status :: 5 - Production/Stable"

dependencies = [
    "grpcio >= 1.51.3, < 2.0.0",  # https://github.com/googleapis/python-pubsub/issues/609
    # google-api-core >= 1.34.0 is allowed in order to support google-api-core 1.x
    "google-auth >= 2.14.1, <3.0.0",
    "google-api-core[grpc] >= 1.34.0, <3.0.0,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,!=2.10.*",
    "proto-plus >= 1.22.0, <2.0.0",
    "proto-plus >= 1.22.2, <2.0.0; python_version>='3.11'",
    "proto-plus >= 1.25.0, < 2.0.0; python_version >= '3.13'",
    "protobuf>=3.20.2,<7.0.0,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
    "grpc-google-iam-v1 >= 0.12.4, < 1.0.0",
    "grpcio-status >= 1.33.2",
    "opentelemetry-api <= 1.22.0; python_version<='3.7'",
    "opentelemetry-api >= 1.27.0; python_version>='3.8'",
    "opentelemetry-sdk <= 1.22.0; python_version<='3.7'",
    "opentelemetry-sdk >= 1.27.0; python_version>='3.8'",
]
extras = {"libcst": "libcst >= 0.3.10"}
url = "https://github.com/googleapis/python-pubsub"

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

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
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.7",
    scripts=["scripts/fixup_pubsub_v1_keywords.py"],
    include_package_data=True,
    zip_safe=False,
)
