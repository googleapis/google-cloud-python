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
    "gcsfs >=2023.3.0, !=2025.5.0",
    "geopandas >=0.12.2",
    "google-auth >=2.15.0,<3.0",
    "google-cloud-bigquery[bqstorage,pandas] >=3.31.0",
    # 2.30 needed for arrow support.
    "google-cloud-bigquery-storage >= 2.30.0, < 3.0.0",
    "google-cloud-functions >=1.12.0",
    "google-cloud-bigquery-connection >=1.12.0",
    "google-cloud-iam >=2.12.1",
    "google-cloud-resource-manager >=1.10.3",
    "google-cloud-storage >=2.0.0",
    "numpy >=1.24.0",
    "pandas >=1.5.3",
    "pandas-gbq >=0.26.1",
    "pyarrow >=15.0.2",
    "pydata-google-auth >=1.8.2",
    "requests >=2.27.1",
    "shapely >=1.8.5",
    "sqlglot >=23.6.3",
    "tabulate >=0.9",
    "ipywidgets >=7.7.1",
    "humanize >=4.6.0",
    "matplotlib >=3.7.1",
    "db-dtypes >=1.4.2",
    # For vendored ibis-framework.
    "atpublic>=2.3,<6",
    "python-dateutil>=2.8.2,<3",
    "pytz>=2022.7",
    "toolz>=0.11,<2",
    "typing-extensions>=4.5.0,<5",
    "rich>=12.4.4,<14",
]
extras = {
    # Optional test dependencies packages. If they're missed, may skip some tests.
    "tests": [
        "freezegun",
        "pytest-snapshot",
        "google-cloud-bigtable >=2.24.0",
        "google-cloud-pubsub >=2.21.4",
    ],
    # used for local engine, which is only needed for unit tests at present.
    "polars": ["polars >= 1.7.0"],
    "scikit-learn": ["scikit-learn>=1.2.2"],
    # Packages required for basic development flow.
    "dev": [
        "pytest",
        "pre-commit",
        "nox",
        "google-cloud-testutils",
    ],
    # install anywidget for SQL
    "anywidget": [
        "anywidget>=0.9.18",
    ],
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
    long_description_content_type="text/x-rst",
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
        "Programming Language :: Python :: 3.13",
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
