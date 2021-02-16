# Copyright 2021 Google LLC
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

from setuptools import setup

setup(
    author="QLogic LLC",
    author_email="cloud-spanner-developers@googlegroups.com",
    classifiers=["Intended Audience :: Developers"],
    description="SQLAlchemy dialect integrated into Cloud Spanner database",
    entry_points={
        "sqlalchemy.dialects": [
            "spanner = google.cloud.sqlalchemy_spanner:SpannerDialect"
        ]
    },
    install_requires=["sqlalchemy>=1.1.13", "google-cloud-spanner>=3.0.0"],
    name="sqlalchemy-spanner",
    packages=["google.cloud.sqlalchemy_spanner"],
    url="https://github.com/q-logic/python-sqlalchemy-spanner/",
    version="0.1",
)
