# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import setuptools

name = 'gcp-sphinx-docfx-yaml'
description = 'Sphinx Python Domain to DocFX YAML Generator'
version = '1.4.8'
dependencies = [
    'black',
    'gcp-docuploader',
    'PyYAML',
    'sphinx',
    'sphinx-markdown-builder',
    'sphinxcontrib.napoleon',
    'unidecode',
    'wheel>=0.24.0'
]

packages = setuptools.find_packages('.', exclude=['tests'])

extra_setup = dict(
setup_requires=['pytest-runner'],
tests_require=['pytest', 'mock'],
)

setuptools.setup(
    name=name,
    version=version,
    description=description,
    author='Google LLC',
    author_email='dandhlee@google.com',
    license='Apache 2.0',
    url='https://github.com/googleapis/sphinx-docfx-yaml',
    package_dir={'': '.'},
    packages=packages,
    install_requires=dependencies,
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
    **extra_setup
)
