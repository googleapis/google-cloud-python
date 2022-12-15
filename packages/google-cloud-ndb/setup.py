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

import setuptools


def main():
    package_root = os.path.abspath(os.path.dirname(__file__))
    readme_filename = os.path.join(package_root, "README.md")
    with io.open(readme_filename, encoding="utf-8") as readme_file:
        readme = readme_file.read()
    dependencies = [
        "google-api-core[grpc] >= 1.34.0, <3.0.0dev,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,!=2.10.*",
        "google-cloud-datastore >= 2.7.2, <3.0.0dev",
        "protobuf >= 3.19.5, <5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
        "pymemcache >= 2.1.0, < 5.0.0dev",
        "redis >= 3.0.0, < 5.0.0dev",
        "pytz >= 2018.3"
    ]

    setuptools.setup(
        name="google-cloud-ndb",
        version = "2.1.0",
        description="NDB library for Google Cloud Datastore",
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Google LLC",
        author_email="googleapis-packages@google.com",
        license="Apache 2.0",
        url="https://github.com/googleapis/python-ndb",
        project_urls={
            'Documentation': 'https://googleapis.dev/python/python-ndb/latest',
            'Issue Tracker': 'https://github.com/googleapis/python-ndb/issues'
        },
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
            "Topic :: Internet",
        ],
        platforms="Posix; MacOS X; Windows",
        packages=setuptools.find_packages(),
        namespace_packages=["google", "google.cloud"],
        install_requires=dependencies,
        extras_require={},
        python_requires=">=3.7",
        include_package_data=False,
        zip_safe=False,
    )


if __name__ == "__main__":
    main()
