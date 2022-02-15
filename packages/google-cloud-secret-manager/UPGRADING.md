# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-secret-manager` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-secret-manager/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with the `libcst` extra.

```py
python3 -m pip install google-cloud-secret-manager[libcst]
```

* The script `fixup_secretmanager_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_secretmanager_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import secretmanager_v1

client = secretmanager_v1.SecretManagerServiceClient()

secret = client.get_secret("secret_name")
```


**After:**
```py
from google.cloud import secretmanager_v1

client = secretmanager_v1.SecretManagerServiceClient()

secret = client.get_secret(request={'name': "secret_name"})
```

### More Details

In `google-cloud-secret-manager<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_secret(
        self,
        parent,
        secret_id,
        secret,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_secret(
        self,
        request: service.CreateSecretRequest = None,
        *,
        parent: str = None,
        secret_id: str = None,
        secret: resources.Secret = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Secret:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_secret(
    request={
        "parent": parent,
        "secret_id": secret_id,
        "secret": secret
    }
)
```

```py
response = client.create_secret(
    parent=parent,
    secret_id=secret_id,
    secret=secret
)
```

This call is invalid because it mixes `request` with a keyword argument `secret`. Executing this code
will result in an error.

```py
response = client.create_secret(
    request={
        "parent": parent,
        "secret_id": secret_id
    },
    secret=secret
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import secretmanager_v1

secret_version = secretmanager_v1.enums.SecretVersion.ENABLED
secret = secretmanager_v1.types.Secret(name="name")
```


**After:**
```py
from google.cloud import secretmanager_v1

secret_version = secretmanager_v1.SecretVersion.ENABLED
secret = secretmanager_v1.Secret(name="name")
```

## Path Helper Methods

The following path helper methods have been removed. Please construct
the paths manually.

```py
project = 'my-project'
secret = 'secret'
secret_version = 'secret_version'

project_path = f'projects/{project}'
secret_version_path = f'projects/{project}/secrets/{secret}/versions/{secret_version}'
```