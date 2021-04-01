# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-containeranalysis` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-containeranalysis/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-containeranalysis[libcst]
```

* The script `fixup_containeranalysis_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_containeranalysis_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud.devtools import containeranalysis_v1

client = containeranalysis_v1.ContainerAnalysisClient()
resource = "projects/[PROJECT_ID]/notes/[NOTE_ID]"
policy = client.get_iam_policy(resource)
```


**After:**
```py
from google.cloud.devtools import containeranalysis_v1

client = containeranalysis_v1.ContainerAnalysisClient()
request = {"resource": "projects/[PROJECT_ID]/notes/[NOTE_ID]"}
policy = client.get_iam_policy(request=request)
```

### More Details

In `google-cloud-containeranalysis<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/b77cacf1ed06e0301a39d6328b599e24102f04be/google/devtools/containeranalysis/v1/containeranalysis.proto#L67) specified by the API producer.


**After:**
```py
    def get_iam_policy(
        self,
        request: iam_policy.GetIamPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.test_iam_permissions(
    request={
        "resource": resource,
        "permissions": permissions,
    }
)
```

```py
response = client.test_iam_permissions(
    resource=resource,
    permissions=permissions,
)
```

This call is invalid because it mixes `request` with a keyword argument `permissions`. Executing this code
will result in an error.

```py
response = client.test_iam_permissions(
    request={
        "resource": resource,
    },
    permissions=permissions
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodule `types` has been removed.

**Before:**
```py
from google.cloud.devtools import containeranalysis_v1

audit_config = containeranalysis_v1.types.AuditConfigDelta()
```


**After:**
```py
from google.cloud.devtools import containeranalysis_v1

audit_config = containeranalysis_v1.AuditConfigDelta()
```
