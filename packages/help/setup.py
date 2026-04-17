# Copyright 2026 Google LLC
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

name = "help"
description = "Client libraries help documentation"
release_status = "Development Status :: 5 - Production/Stable"
dependencies = []

# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.md")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

version = {}
with open(os.path.join(package_root, "help/version.py")) as fp:
    exec(fp.read(), version)
version_id = version["__version__"]

setuptools.setup(
    name=name,
    version=version_id,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Google LLC",
    author_email="cloud-sdk@google.com",
    license="Apache 2.0",
    url="https://github.com/googleapis/google-cloud-python/tree/main/packages/help",
    project_urls={
        "Source": "https://github.com/googleapis/google-cloud-python/tree/main/packages/help",
        "Changelog": "https://github.com/googleapis/google-cloud-python/tree/main/packages/help/CHANGELOG.md",
        "Issues": "https://github.com/googleapis/google-cloud-python/issues",
    },
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    install_requires=dependencies,
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    packages=["help"],
)
