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
$ rm -f _crc32c_cffi.*
$ [sudo] rm -fr crc32c/build/
```

(Similar work will need to be done for `quay.io/pypa/manylinux1_i686`.)
