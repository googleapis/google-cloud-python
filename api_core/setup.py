# Copyright 2018, Google LLC
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

import setuptools


# Package metadata.

name = 'google-api-core'
description = 'Google API client core library'
version = '0.1.5.dev1'
# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Stable'
release_status = 'Development Status :: 4 - Beta'
dependencies = [
    'googleapis-common-protos<2.0dev,>=1.5.3',
    'protobuf>=3.0.0',
    'google-auth<2.0.0dev,>=0.4.0',
    'requests<3.0.0dev,>=2.18.0',
    'setuptools>=34.0.0',
    'six>=1.10.0',
    'pytz',
]
extras = {
    'grpc': 'grpcio>=1.8.2',
    ':python_version < "3.2"': 'futures>=3.2.0',
}


# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(package_root, 'README.rst')) as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name=name,
    description=description,
    version=version,
    author='Google LLC',
    author_email='googleapis-packages@google.com',
    license='Apache 2.0',
    classifiers=[
        release_status,
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
    platforms='Posix; MacOS X; Windows',
    zip_safe=False,
    include_package_data=True,
    long_description=readme,
    install_requires=dependencies,
    extras_require=extras,
    packages=setuptools.find_packages(exclude=('tests*',)),
    namespace_packages=['google'],
    url='https://github.com/GoogleCloudPlatform/google-cloud-python',
)
