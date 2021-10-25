# Copyright 2017 Google Inc.
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

import os

import setuptools


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()


REQUIREMENTS = [
    'google-crc32c >= 1.0, < 2.0dev',
]
EXTRAS_REQUIRE = {
    'requests': [
        'requests >= 2.18.0, < 3.0.0dev',
    ],
    'aiohttp': 'aiohttp >= 3.6.2, < 4.0.0dev'
}

setuptools.setup(
    name='google-resumable-media',
    version = "2.1.0",
    description='Utilities for Google Media Downloads and Resumable Uploads',
    author='Google Cloud Platform',
    author_email='googleapis-publisher@google.com',
    long_description=README,
    namespace_packages=['google'],
    scripts=[],
    url='https://github.com/googleapis/google-resumable-media-python',
    packages=setuptools.find_packages(exclude=('tests*',)),
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>= 3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
    ],
)
