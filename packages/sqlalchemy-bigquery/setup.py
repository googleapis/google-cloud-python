#!/usr/bin/env python
# Copyright (c) 2017 The PyBigQuery Authors
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
from setuptools import setup


def readme():
    with io.open("README.rst", "r", encoding="utf8") as f:
        return f.read()


setup(
    name="pybigquery",
    version='0.5.0',
    description="SQLAlchemy dialect for BigQuery",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    author="Maxim Zudilov",
    author_email="maxim.zudilov@gmail.com",
    packages=['pybigquery'],
    url="https://github.com/mxmzdlv/pybigquery",
    download_url='https://github.com/mxmzdlv/pybigquery/archive/v0.4.14.tar.gz',
    keywords=['bigquery', 'sqlalchemy'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'sqlalchemy>=1.1.9',
        'google-cloud-bigquery>=1.6.0',
        'future',
    ],
    tests_require=[
        'pytz'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'bigquery = pybigquery.sqlalchemy_bigquery:BigQueryDialect'
        ]
    }
)
