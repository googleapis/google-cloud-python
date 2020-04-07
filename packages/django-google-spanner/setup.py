# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from setuptools import find_packages, setup

install_requires = [
    'sqlparse >= 0.3.0',
    'google-cloud >= 0.34.0',
    'google-cloud-spanner >= 1.8.0',
]

setup(
        name='django-spanner',
        # Duplicate version here rather than using
        # __import__('django_spanner').__version__ because that file imports
        # django and google.cloud which may not be installed.
        version='2.2a0',
        author='Google LLC',
        author_email='cloud-spanner-developers@googlegroups.com',
        description=('Bridge to enable using Django with Spanner.'),
        license='BSD',
        packages=find_packages(exclude=['tests']),
        install_requires=install_requires,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Utilities',
            'Framework :: Django',
            'Framework :: Django :: 2.2',
        ],
)
