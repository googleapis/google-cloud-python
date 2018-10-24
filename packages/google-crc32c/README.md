# `py-crc32c`

> Python / Cython wrapper for `google/crc32c`

## Checking Out

Be sure to check out all submodules:

```
$ git clone --recursive git@github.com:dhermes/py-crc32c.git
```

## Building Wheel

```
$ docker pull quay.io/pypa/manylinux1_x86_64
$ docker run \
>   --rm \
>   --tty \
>   --interactive \
>   --volume $(pwd):/var/code/py-crc32c/ \
>   quay.io/pypa/manylinux1_x86_64 \
>   /var/code/py-crc32c/build.sh
...
_crc32c_cffi: <module '_crc32c_cffi' from '/var/code/py-crc32c/_crc32c_cffi.cpython-37m-x86_64-linux-gnu.so'>
_crc32c_cffi.lib: <Lib object for '_crc32c_cffi'>
dir(_crc32c_cffi.lib): ['crc32c_extend', 'crc32c_value']
```

(Similar work will need to be done for `quay.io/pypa/manylinux1_i686`.)
