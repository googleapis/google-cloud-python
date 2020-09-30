# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-os-login` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-oslogin/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-os-login
```

* The script `fixup_oslogin_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_oslogin_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import oslogin_v1

client = oslogin_v1.OsLoginServiceClient()

login_profile = client.get_login_profile("login_profile_name")
```


**After:**
```py
from google.cloud import oslogin_v1

client = oslogin_v1.OsLoginServiceClient()

login_profile = client.get_login_profile(request={'name': "login_profile_name"})
```

### More Details

In `google-cloud-os-login<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def update_ssh_public_key(
        self,
        name,
        ssh_public_key,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def update_ssh_public_key(
        self,
        request: oslogin.UpdateSshPublicKeyRequest = None,
        *,
        name: str = None,
        ssh_public_key: common.SshPublicKey = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> common.SshPublicKey:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.update_ssh_public_key(
    request={
        "name": name,
        "ssh_public_key": ssh_public_key,
        "update_mask": update_mask,
    }
)
```

```py
response = client.update_ssh_public_key(
    name=name,
    ssh_public_key=ssh_public_key,
    update_mask=update_mask,
)
```

This call is invalid because it mixes `request` with a keyword argument `update_mask`. Executing this code
will result in an error.

```py
response = client.update_ssh_public_key(
    request={
        "name": name,
        "ssh_public_key": ssh_public_key
    },
    update_mask=update_mask,
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import oslogin_v1

system_type = oslogin_v1.enums.OperatingSystemType.LINUX
login_profile = oslogin_v1.types.LoginProfile(name="name")
```


**After:**
```py
from google.cloud import oslogin_v1

system_type = oslogin_v1.OperatingSystemType.LINUX
login_profile = oslogin_v1.LoginProfile(name="name")
```

## Path Helper Methods

The following path helper methods have been removed. Please construct these paths manually.

```py
project = 'my-project'
user = 'user'

posix_account_path = f'users/{user}/projects/{project}'
user_path = f'users/{user}'
```