#!/usr/bin/env python

from setuptools import setup

setup(
    name="pybigquery",
    version='0.1',
    description="DB-API interface and SQLAlchemy dialect for BigQuery",
    author="Maxim Zudilov",
    author_email="maxim.zudilov@gmail.com",
    packages=['bigquery'],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'sqlalchemy>=1.1.9',
        'google-cloud>=0.25.0'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'bigquery = bigquery.sqlalchemy_bigquery:BigQueryDialect'
        ]
    }
)
