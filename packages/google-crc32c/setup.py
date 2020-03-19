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
import shutil

import setuptools
import setuptools.command.build_ext
import warnings

_EXTRA_DLL = "extra-dll"
_DLL_FILENAME = "crc32c.dll"


def copy_dll(build_lib):
    if os.name != "nt":
        return

    install_prefix = os.environ.get("CRC32C_INSTALL_PREFIX")
    if install_prefix is None:
        return

    installed_dll = os.path.join(install_prefix, "bin", _DLL_FILENAME)
    lib_dlls = os.path.join(build_lib, "crc32c", _EXTRA_DLL)
    os.makedirs(lib_dlls)
    relocated_dll = os.path.join(lib_dlls, _DLL_FILENAME)
    shutil.copyfile(installed_dll, relocated_dll)


class BuildExtWithDLL(setuptools.command.build_ext.build_ext):
    def run(self):
        copy_dll(self.build_lib)
        result = setuptools.command.build_ext.build_ext.run(self)
        return result


def main(build_cffi=True):
    build_path = os.path.join("src", "crc32c_build.py")
    builder = "{}:FFIBUILDER".format(build_path)
    cffi_dep = "cffi >= 1.0.0"

    setuptools.setup(
        packages=["crc32c"],
        package_dir={"": "src"},
        package_data={"crc32c": [os.path.join(_EXTRA_DLL, _DLL_FILENAME)]},
        setup_requires=[cffi_dep] if build_cffi else [],
        cffi_modules=[builder] if build_cffi else [],
        install_requires=[cffi_dep] if build_cffi else [],
        cmdclass={"build_ext": BuildExtWithDLL},
    )


if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        raise
    except SystemExit:
        # If installation fails, it is likely a compilation error with CFFI
        # Try to install again.
        warnings.warn(
            "Compiling the CFFI Extension crc32c has failed. Only a pure "
            "python implementation will be usable."
        )
        main(build_cffi=False)

