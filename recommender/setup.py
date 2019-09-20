# -*- coding: utf-8 -*-
import setuptools  # type: ignore


setuptools.setup(
    name="google-cloud-recommender",
    version="0.0.1",
    packages=setuptools.PEP420PackageFinder.find(),
    namespace_packages=("google", "google.cloud"),
    platforms="Posix; MacOS X; Windows",
    include_package_data=True,
    install_requires=(
        "google-api-core >= 1.8.0, < 2.0.0dev",
        "googleapis-common-protos >= 1.5.8",
        "grpcio >= 1.10.0",
        "proto-plus >= 0.4.0",
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False,
)
