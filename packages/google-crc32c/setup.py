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

import setuptools


def main():
    setuptools.setup(
        name="py_crc32c",
        version="0.0.1",
        description="TODO",
        author="Danny Hermes",
        author_email="daniel.j.hermes@gmail.com",
        long_description="TODO",
        scripts=(),
        url="https://github.com/dhermes/py-crc32c",
        packages=[],
        package_dir={"": "src"},
        license="Apache 2.0",
        platforms="Posix; MacOS X; Windows",
        zip_safe=True,
        setup_requires=["cffi >= 1.0.0"],
        cffi_modules=["src/crc32c_build.py:FFIBUILDER"],
        install_requires=["cffi >= 1.0.0"],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
    )


if __name__ == "__main__":
    main()
