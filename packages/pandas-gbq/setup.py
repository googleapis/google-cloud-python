#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versioneer
from setuptools import find_packages, setup

NAME = "pandas-gbq"


# versioning
cmdclass = versioneer.get_cmdclass()


def readme():
    with open("README.rst") as f:
        return f.read()


INSTALL_REQUIRES = [
    "setuptools",
    "pandas>=0.20.1",
    "pydata-google-auth",
    "google-auth",
    "google-auth-oauthlib",
    "google-cloud-bigquery[bqstorage,pandas]>=1.11.1,<3.0.0dev",
]

extras = {"tqdm": "tqdm>=4.23.0"}

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Pandas interface to Google BigQuery",
    long_description=readme(),
    license="BSD License",
    author="The PyData Development Team",
    author_email="pydata@googlegroups.com",
    url="https://github.com/pydata/pandas-gbq",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    keywords="data",
    install_requires=INSTALL_REQUIRES,
    extras_require=extras,
    python_requires=">=3.5",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    test_suite="tests",
)
