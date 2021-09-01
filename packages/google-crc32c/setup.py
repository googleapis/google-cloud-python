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

import logging
import os
import shutil
import setuptools
import setuptools.command.build_ext

_EXTRA_DLL = "extra-dll"
_DLL_FILENAME = "crc32c.dll"

# Explicit environment variable disables pure-Python fallback
CRC32C_PURE_PYTHON_EXPLICIT = "CRC32C_PURE_PYTHON" in os.environ
_FALSE_OPTIONS = ("0", "false", "no", "False", "No", None)
CRC32C_PURE_PYTHON = os.getenv("CRC32C_PURE_PYTHON") not in _FALSE_OPTIONS


def copy_dll(build_lib):
    if os.name != "nt":
        return

    install_prefix = os.environ.get("CRC32C_INSTALL_PREFIX")
    if install_prefix is None:
        return

    installed_dll = os.path.join(install_prefix, "bin", _DLL_FILENAME)
    lib_dlls = os.path.join(build_lib, "google_crc32c", _EXTRA_DLL)
    os.makedirs(lib_dlls, exist_ok=True)
    relocated_dll = os.path.join(lib_dlls, _DLL_FILENAME)
    shutil.copyfile(installed_dll, relocated_dll)


class BuildExtWithDLL(setuptools.command.build_ext.build_ext):
    def run(self):
        copy_dll(self.build_lib)
        result = setuptools.command.build_ext.build_ext.run(self)
        return result


module_path = os.path.join("src", "google_crc32c", "_crc32c.c")
module = setuptools.Extension(
    "google_crc32c._crc32c",
    sources=[os.path.normcase(module_path)],
    libraries=["crc32c"],
)


if CRC32C_PURE_PYTHON:
    setuptools.setup(
        packages=["google_crc32c"],
        package_dir={"": "src"},
        ext_modules=[],
    )
else:
    try:
        setuptools.setup(
            packages=["google_crc32c"],
            package_dir={"": "src"},
            ext_modules=[module],
            cmdclass={"build_ext": BuildExtWithDLL},
        )
    except SystemExit:
        if "CRC32C_PURE_PYTHON" not in os.environ:
            # If build / install fails, it is likely a compilation error with
            # the C extension:  advise user how to enable the pure-Python
            # build.
            logging.error(
                "Compiling the C Extension for the crc32c library failed. "
                "To enable building / installing a pure-Python-only version, "
                "set 'CRC32C_PURE_PYTHON=1' in the environment."
            )
        raise
