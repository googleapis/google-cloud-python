#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import versioneer


NAME = 'pandas-gbq'


# versioning
cmdclass = versioneer.get_cmdclass()


def readme():
    with open('README.rst') as f:
        return f.read()


INSTALL_REQUIRES = [
    'pandas',
    'httplib2>=0.9.2',
    'google-api-python-client>=1.6.0',
    'google-auth>=1.0.0',
    'google-auth-httplib2>=0.0.1',
    'google-auth-oauthlib>=0.0.1',
]


setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Pandas interface to Google Big Query",
    long_description=readme(),
    license='BSD License',
    author='The PyData Development Team',
    author_email='pydata@googlegroups.com',
    url='https://github.com/pydata/pandas-gbq',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
    keywords='data',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    test_suite='tests',
)
