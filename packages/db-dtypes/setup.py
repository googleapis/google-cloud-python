#!/usr/bin/env python
# Copyright (c) 2017 The db-dtypes Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import io
import os
import re
from setuptools import setup

# Package metadata.

name = "db-dtypes"
description = "SQLAlchemy dialect for BigQuery"

# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = "Development Status :: 4 - Beta"

package_root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(package_root, "db_dtypes", "version.py")) as f:
    version = re.search('__version__ = "([^"]+)"', f.read()).group(1)


def readme():
    with io.open("README.rst", "r", encoding="utf8") as f:
        return f.read()


setup(
    name=name,
    version=version,
    description=description,
    long_description=readme(),
    long_description_content_type="text/x-rst",
    author="The db-dtypes Authors",
    author_email="googleapis-packages@google.com",
    packages=["db_dtypes"],
    url="https://github.com/googleapis/python-db-dtypes-pandas",
    keywords=["sql", "pandas"],
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
    ],
    platforms="Posix; MacOS X; Windows",
    install_requires=[],
    python_requires=">=3.6, <3.10",
    tests_require=["packaging", "pytz"],
    entry_points={"sqlalchemy.dialects": ["bigquery = db_dtypes:BigQueryDialect"]},
)
