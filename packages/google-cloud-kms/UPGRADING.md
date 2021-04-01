# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-kms` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-kms/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-kms[libcst]
```

* The script `fixup_kms_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_kms_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
 from google.cloud import kms

client = kms.KeyManagementServiceClient()
location_name = client.location_path(project_id, location_id)
key_ring = {}

created_key_ring = client.create_key_ring(location_name, id, key_ring)
```


**After:**
```py
from google.cloud import kms

client = kms.KeyManagementServiceClient()
location_name = f'projects/{project_id}/locations/{location_id}'
key_ring = {}

created_key_ring = client.create_key_ring(request={'parent': location_name, 'key_ring_id': id, 'key_ring': key_ring})
```

### More Details

In `google-cloud-kms<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_key_ring(
        self,
        parent,
        key_ring_id,
        key_ring,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_key_ring(
        self,
        request: service.CreateKeyRingRequest = None,
        *,
        parent: str = None,
        key_ring_id: str = None,
        key_ring: resources.KeyRing = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.KeyRing:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_key_ring(
    request={
        "parent": parent,
        "key_ring_id": key_ring_id,
        "key_ring": key_ring
    }
)
```

```py
response = client.create_key_ring(
    parent=parent,
    key_ring_id=key_ring_id,
    key_ring=key_ring
)
```

This call is invalid because it mixes `request` with a keyword argument `key_ring`. Executing this code
will result in an error.

```py
response = client.create_key_ring(
    request={
        "parent": parent,
        "key_ring_id": key_ring_id,
    },
    key_ring=key_ring
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

 from google.cloud import kms

purpose = kms.enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
key_ring = kms.types.KeyRing()
```


**After:**
```py
from google.cloud import kms

purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
key_ring = kms.KeyRing()
```

## Resource Path Helper Methods

The resource path helper method `location_path` has been removed. Please construct
this path manually.

```py
project = 'my-project'
location = 'us-east1'

location_path = f'projects/{project}/locations/{location}'
```

The resource path helper method `crypto_key_path_path` has been renamed to `crypto_key_path`.

```py
name = client.crypto_key_path('PROJECT_ID', 'LOCATION_ID', 'KEY_RING_ID', 'CRYPTO_KEY_ID')
```
