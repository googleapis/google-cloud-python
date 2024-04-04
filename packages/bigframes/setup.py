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

import io
import itertools
import os
from typing import Dict

import setuptools

# Package metadata.

name = "bigframes"
description = (
    "BigQuery DataFrames -- scalable analytics and machine learning with BigQuery"
)

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 5 - Production/Stable"
dependencies = [
    # please keep these in sync with the minimum versions in testing/constraints-3.9.txt
    "cloudpickle >= 2.0.0",
    "fsspec >=2023.3.0",
    "gcsfs >=2023.3.0",
    "geopandas >=0.12.2",
    "google-auth >=2.15.0,<3.0dev",
    "google-cloud-bigquery[bqstorage,pandas] >=3.10.0",
    "google-cloud-functions >=1.12.0",
    "google-cloud-bigquery-connection >=1.12.0",
    "google-cloud-iam >=2.12.1",
    "google-cloud-resource-manager >=1.10.3",
    "google-cloud-storage >=2.0.0",
    "ibis-framework[bigquery] >=8.0.0,<9.0.0dev",
    # TODO: Relax upper bound once we have fixed `system_prerelease` tests.
    "pandas >=1.5.0",
    "pyarrow >=8.0.0",
    "pydata-google-auth >=1.8.2",
    "requests >=2.27.1",
    "scikit-learn >=1.2.2",
    "sqlalchemy >=1.4,<3.0dev",
    # Keep sqlglot versions in sync with ibis-framework. This avoids problems
    # where the incorrect version of sqlglot is installed, such as
    # https://github.com/googleapis/python-bigquery-dataframes/issues/315
    "sqlglot >=20.8.0,<=20.11",
    "tabulate >= 0.9",
    "ipywidgets >=7.7.1",
    "humanize >= 4.6.0",
    "matplotlib >= 3.7.1",
]
extras = {
    # Optional test dependencies packages. If they're missed, may skip some tests.
    "tests": [
        "pandas-gbq >=0.19.0",
    ],
    # Packages required for basic development flow.
    "dev": ["pytest", "pytest-mock", "pre-commit", "nox", "google-cloud-testutils"],
}
extras["all"] = list(sorted(frozenset(itertools.chain.from_iterable(extras.values()))))

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

version: Dict[str, str] = {}
with open(os.path.join(package_root, "bigframes/version.py")) as fp:
    exec(fp.read(), version)
version_id = version["__version__"]

# Only include packages under the 'bigframes' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package
    for package in setuptools.find_namespace_packages()
    if package.startswith("bigframes")
] + [
    package
    for package in setuptools.find_namespace_packages("third_party")
    if package.startswith("bigframes_vendored")
]

setuptools.setup(
    name=name,
    version=version_id,
    description=description,
    long_description=readme,
    author="Google LLC",
    author_email="bigframes-feedback@google.com",
    license="Apache 2.0",
    url="https://github.com/googleapis/python-bigquery-dataframes",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    install_requires=dependencies,
    extras_require=extras,
    platforms="Posix; MacOS X; Windows",
    package_dir={
        "bigframes": "bigframes",
        "bigframes_vendored": "third_party/bigframes_vendored",
    },
    packages=packages,
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
)
