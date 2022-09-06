# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
import io
import os
import setuptools  # type: ignore

version = '0.1.0'

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, 'README.rst')
with io.open(readme_filename, encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='google-iam-credentials',
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    url="https://github.com/googleapis/python-google-iam-credentials",
    version=version,
    long_description=readme,
    packages=setuptools.PEP420PackageFinder.find(),
    namespace_packages=('google', 'google.iam'),
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    install_requires=(
        'google-api-core[grpc] >= 2.10.0, < 3.0.0dev',
        'libcst >= 0.2.5',
        'googleapis-common-protos >= 1.55.0, <2.0.0dev',
        'proto-plus >= 1.19.7',
    ),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
