# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-firestore` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library may require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-firestore/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

If you previously were using modules or functions under the namespace
`google.cloud.firestore_v1.gapic` there is a high likelihood you have incompatible code.
To assist with this, we have includes some helpful scripts to make some of the code
modifications required to use 2.0.0.

* Install the library

```py
python3 -m pip install google-cloud-firestore
```

* The scripts `fixup_firestore_v1_keywords.py` and `fixup_firestore_admin_v1_keywords.py` 
is shipped with the library. It expects an input directory (with the code to convert)
and an empty destination directory.

```sh
$ fixup_firestore_v1_keywords.py --input-directory .samples/ --output-directory samples/
$ fixup_firestore_admin_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

### More Details

In `google-cloud-firestore<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def a_method(
        self,
        param1,
        param2,
        param3,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def a_method(
        self,
        request: RequestType = None,
        *
        param1,
        param2,
        param3,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.a_method(
    request={
        "param1": param1,
        "param2": param2,
        "param3": param3
    }
)
```

```py
response = client.a_method(
    param1=param1,
    param2=param2,
    param3=param3
)
```

This call is invalid because it mixes `request` with a keyword argument `param1`. Executing this code
will result in an error.

```py
response = client.a_method(
    request={
        "param1": param1,
        "param2": param2
    },
    param2=param2
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import firestore_v1

direction = firestore_v1.enums.StructuredQuery.Direction.ASCENDING
```


**After:**
```py
from google.cloud import firestore_v1

direction = firestore_v1.types.StructuredQuery.Direction.ASCENDING
```
