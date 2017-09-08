#!/usr/bin/env python

from setuptools import setup

setup(
    name="pybigquery",
    version='0.2',
    description="SQLAlchemy dialect for BigQuery",
    author="Maxim Zudilov",
    author_email="maxim.zudilov@gmail.com",
    packages=['pybigquery'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'sqlalchemy>=1.1.9',
        'google-cloud-bigquery>=0.27.0'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'bigquery = pybigquery.sqlalchemy_bigquery:BigQueryDialect'
        ]
    }
)
