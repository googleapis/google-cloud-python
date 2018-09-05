#!/usr/bin/env python
import io
from setuptools import setup


def readme():
    with io.open("README.rst", "r", encoding="utf8") as f:
        return f.read()

setup(
    name="pybigquery",
    version='0.4.2',
    description="SQLAlchemy dialect for BigQuery",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    author="Maxim Zudilov",
    author_email="maxim.zudilov@gmail.com",
    packages=['pybigquery'],
    url="https://github.com/mxmzdlv/pybigquery",
    download_url='https://github.com/mxmzdlv/pybigquery/archive/v0.4.2.tar.gz',
    keywords=['bigquery', 'sqlalchemy'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'sqlalchemy>=1.1.9',
        'google-cloud-bigquery>=1.5.0',
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
