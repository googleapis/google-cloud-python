# Copyright 2016 Google LLC
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
import os

from setuptools import find_packages
from setuptools import setup


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(PACKAGE_ROOT, 'README.rst'), 'r') as readme_file:
    readme = readme_file.read()


setup(
    author='Google Cloud Platform',
    author_email='googleapis-publisher@google.com',
    name='google-cloud-videointelligence',
    version='1.0.0',
    description='Python Client for Google Cloud Video Intelligence',
    long_description=readme,
    namespace_packages=[
        'google',
        'google.cloud',
    ],
    packages=find_packages(exclude=('tests*',)),
    install_requires=(
        'google-api-core>=0.1.0, <0.2.0dev',
        'google-auth>=1.0.2, <2.0dev',
        'googleapis-common-protos[grpc]>=1.5.2, <2.0dev',
        'requests>=2.18.4, <3.0dev',
    ),
    url='https://github.com/GoogleCloudPlatform/google-cloud-python',
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
    scripts=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ],
)
