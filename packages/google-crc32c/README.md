# `py-crc32c`

> Python / Cython wrapper for google/crc32c

## Building Wheel

```
$ docker pull quay.io/pypa/manylinux1_i686
$ docker pull quay.io/pypa/manylinux1_x86_64
$ git clone --recursive https://github.com/google/crc32c
$ docker run \
>   --rm \
>   --tty \
>   --interactive \
>   --volume $(pwd)/crc32c:/var/code/crc32c/ \
>   quay.io/pypa/manylinux1_x86_64 \
>   /bin/bash
[root@df9f7ccc7e04 /]#
[root@df9f7ccc7e04 /]# /opt/python/cp37-cp37m/bin/python -m pip install --upgrade pip
[root@df9f7ccc7e04 /]# /opt/python/cp37-cp37m/bin/python -m pip install --upgrade cmake
[root@df9f7ccc7e04 /]# /opt/python/cp37-cp37m/bin/cmake --version
cmake version 3.12.0

CMake suite maintained and supported by Kitware (kitware.com/cmake).
[root@df9f7ccc7e04 /]# cd /var/code/crc32c
[root@df9f7ccc7e04 crc32c]# mkdir build
[root@df9f7ccc7e04 crc32c]# cd build/
[root@df9f7ccc7e04 build]# /opt/python/cp37-cp37m/bin/cmake -DCRC32C_BUILD_TESTS=0 -DCRC32C_BUILD_BENCHMARKS=0 ..
...
[root@df9f7ccc7e04 build]# make all install
```
