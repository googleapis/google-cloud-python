# `google-crc32c`
![GA](https://img.shields.io/badge/support-GA-gold.svg) [<img src="https://img.shields.io/pypi/v/google-crc32c.svg">](https://pypi.org/project/google-crc32c) ![Python Versions](https://img.shields.io/pypi/pyversions/google-crc32c)

This package wraps the [`google/crc32c`](https://github.com/google/crc32c)
hardware-based implementation of the CRC32C hashing algorithm. Multiple wheels
are distributed as well as source. If a wheel is not published for the python
version and platform you are using, you will need to compile crc32c using a
C toolchain.

# Currently Published Wheels

Wheels are currently published for Python 3.6, 3.7, 3.8, 3.9 for multiple
architectures. For information on building your own, please view [BUILDING.md](BUILDING.md).

## Linux
Wheels are published for the following platforms / architectures:

- `manylinux1` platform, `x86_64` architecture
- `manylinux2010` platform, `x86_64` architecture
- `manylinux2014` platform, `x86_64` architecture
- `manylinux2014` platform, `aarch64` architecture

## Mac OS
Wheels are published for `x86_64` architectures

## Windows
Wheels are published for `win32` and `win_amd64` architectures.
