# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os

from setuptools import find_packages, setup


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(PACKAGE_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()

setup(
    name='gapic-generator',
    version='0.0.4',
    license='Apache 2.0',
    author='Luke Sneeringer',
    author_email='lukesneeringer@google.com',
    url='https://github.com/googleapis/gapic-generator-python.git',
    packages=find_packages(exclude=['docs', 'tests']),
    description='Python client library generator for APIs defined by protocol'
                'buffers',
    long_description=README,
    entry_points="""[console_scripts]
        protoc-gen-dump=gapic.cli.dump:dump
        protoc-gen-python_gapic=gapic.cli.generate:generate
    """,
    platforms='Posix; MacOS X',
    include_package_data=True,
    install_requires=(
        'click >= 6.7',
        'googleapis-common-protos >= 1.6.0b6',
        'jinja2 >= 2.10',
        'protobuf >= 3.5.1',
        'pypandoc >= 1.4',
    ),
    extras_require={
        ':python_version<"3.7"': ('dataclasses >= 0.4',),
    },
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    zip_safe=False,
)
