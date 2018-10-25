# `py-crc32c`

> Python / CFFI wrapper for `google/crc32c`

## Checking Out

Be sure to check out all submodules:

```
$ git clone --recursive https://github.com/dhermes/py-crc32c
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
New WHEEL info tags: cp37-cp37m-manylinux1_x86_64

Fixed-up wheel written to /var/code/py-crc32c/py_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl
...
```

(Similar work will need to be done for `quay.io/pypa/manylinux1_i686`.)

## Verify Wheel

To verify that the `manylinux` wheel works as expected,
run `check-37.sh` on a host Linux OS:

```
$ ./check-37.sh
...
+ venv/bin/python check_cffi_crc32c.py
_crc32c_cffi: <module 'crc32c._crc32c_cffi' from '.../py-crc32c/venv/lib/python3.7/site-packages/crc32c/_crc32c_cffi.abi3.so'>
_crc32c_cffi.lib: <Lib object for 'crc32c._crc32c_cffi'>
dir(_crc32c_cffi.lib): ['crc32c_extend', 'crc32c_value']
+ unzip -l wheels/py_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl
Archive:  wheels/py_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
    26120  2018-10-25 00:09   crc32c/_crc32c_cffi.abi3.so
      765  2018-10-24 23:57   crc32c/__init__.py
    29552  2018-10-25 00:09   crc32c/.libs/libcrc32c-f865a225.so
      109  2018-10-25 00:09   py_crc32c-0.0.1.dist-info/WHEEL
      766  2018-10-25 00:09   py_crc32c-0.0.1.dist-info/METADATA
      652  2018-10-25 00:09   py_crc32c-0.0.1.dist-info/RECORD
        1  2018-10-25 00:09   py_crc32c-0.0.1.dist-info/zip-safe
        7  2018-10-25 00:09   py_crc32c-0.0.1.dist-info/top_level.txt
---------                     -------
    57972                     8 files
...
```
