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

# Disable version normalization performed by setuptools.setup()
try:
    # Try the approach of using sic(), added in setuptools 46.1.0
    from setuptools import sic
except ImportError:
    # Try the approach of replacing packaging.version.Version
    sic = lambda v: v
    try:
        # setuptools >=39.0.0 uses packaging from setuptools.extern
        from setuptools.extern import packaging
    except ImportError:
        # setuptools <39.0.0 uses packaging from pkg_resources.extern
        from pkg_resources.extern import packaging
    packaging.version.Version = packaging.version.LegacyVersion

name = "google-cloud-audit-log"
description = "Google Cloud Audit Protos"
version = "0.1.0"
release_status = "Development Status :: 4 - Beta"
dependencies = ["protobuf >= 3.6.0", "googleapis-common-protos >= 1.52.0"]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.md")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=name,
    version=sic(version),
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=dependencies,
    license="Apache-2.0",
    packages=setuptools.find_packages(),
    package_data={"": ["*.proto"]},
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    namespace_packages=["google", "google.cloud"],
    url="https://github.com/googleapis/python-audit-log",
    include_package_data=True,
)
