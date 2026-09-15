# Copyright 2026 Google LLC
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

import logging
import os
import setuptools

# Explicit environment variable disables pure-Python fallback
SPANNER_ARROW_PURE_PYTHON_EXPLICIT = "SPANNER_ARROW_PURE_PYTHON" in os.environ
_FALSE_OPTIONS = ("0", "false", "no", "False", "No", None)
SPANNER_ARROW_PURE_PYTHON = os.getenv("SPANNER_ARROW_PURE_PYTHON") not in _FALSE_OPTIONS


def build_pure_python():
    setuptools.setup(
        packages=["google_cloud_spanner_arrow"],
        package_dir={"": "src"},
        ext_modules=[],
    )


def build_c_extension():
    module_sources = [
        os.path.normcase(os.path.join("src", "google_cloud_spanner_arrow", "_spanner_arrow.c")),
        os.path.normcase(os.path.join("src", "google_cloud_spanner_arrow", "nanoarrow", "nanoarrow.c")),
    ]
    include_dirs = [
        os.path.normcase(os.path.join("src", "google_cloud_spanner_arrow")),
        os.path.normcase(os.path.join("src", "google_cloud_spanner_arrow", "nanoarrow")),
    ]

    module = setuptools.Extension(
        "google_cloud_spanner_arrow._spanner_arrow",
        sources=module_sources,
        include_dirs=include_dirs,
    )

    setuptools.setup(
        packages=["google_cloud_spanner_arrow"],
        package_dir={"": "src"},
        ext_modules=[module],
    )


if SPANNER_ARROW_PURE_PYTHON:
    build_pure_python()
else:
    try:
        build_c_extension()
    except SystemExit:
        if SPANNER_ARROW_PURE_PYTHON_EXPLICIT:
            logging.error(
                "Compiling the C Extension for google-cloud-spanner-arrow failed. "
                "To enable building / installing a pure-Python-only version, "
                "set 'SPANNER_ARROW_PURE_PYTHON=1' in the environment."
            )
            raise

        logging.info(
            "Compiling the C Extension for google-cloud-spanner-arrow failed. "
            "Falling back to pure Python build."
        )
        build_pure_python()
