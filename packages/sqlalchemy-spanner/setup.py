# Copyright 2021 Google LLC
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
import warnings

import setuptools


# Package metadata.

name = "sqlalchemy-spanner"
description = "SQLAlchemy dialect integrated into Cloud Spanner database"
dependencies = [
    "sqlalchemy>=1.1.13",
    "google-cloud-spanner>=3.55.0",
    "alembic",
]
extras = {
    "tracing": [
        "opentelemetry-api >= 1.1.0",
        "opentelemetry-sdk >= 1.1.0",
        "opentelemetry-instrumentation >= 0.20b0",
    ]
}

BASE_DIR = os.path.dirname(__file__)
VERSION_FILENAME = os.path.join(BASE_DIR, "version.py")
PACKAGE_INFO = {}
with open(VERSION_FILENAME) as f:
    exec(f.read(), PACKAGE_INFO)
version = PACKAGE_INFO["__version__"]

package_root = os.path.abspath(os.path.dirname(__file__))
readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package
    for package in setuptools.PEP420PackageFinder.find()
    if package.startswith("google")
]

# Determine which namespaces are needed.
namespaces = ["google"]
if "google.cloud" in packages:
    namespaces.append("google.cloud")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    setuptools.setup(
        author="Google LLC",
        author_email="cloud-spanner-developers@googlegroups.com",
        classifiers=["Intended Audience :: Developers"],
        description=description,
        long_description=readme,
        entry_points={
            "sqlalchemy.dialects": [
                "spanner.spanner = google.cloud.sqlalchemy_spanner:SpannerDialect"
            ]
        },
        install_requires=dependencies,
        extras_require=extras,
        name=name,
        namespace_packages=namespaces,
        packages=packages,
        url="https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy",
        version=version,
        include_package_data=True,
        zip_safe=False,
    )
