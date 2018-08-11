#!/usr/bin/env python

from setuptools import setup

setup(
    name="pybigquery",
    version='0.3.2',
    description="SQLAlchemy dialect for BigQuery",
    author="Maxim Zudilov",
    author_email="maxim.zudilov@gmail.com",
    packages=['pybigquery'],
    url="https://github.com/mxmzdlv/pybigquery",
    download_url='https://github.com/mxmzdlv/pybigquery/archive/v0.3.2.tar.gz',
    keywords=['bigquery', 'sqlalchemy'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'sqlalchemy>=1.1.9',
        'google-cloud-bigquery>=0.30.0',
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
