# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-redis` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-redis/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-redis[libcst]
```

* The script `fixup_redis_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_redis_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import redis_v1

client = redis_v1.CloudRedisClient()

instance = client.get_instance("instance_name")
```


**After:**
```py
from google.cloud import redis_v1

client = redis_v1.CloudRedisClient()

instance = client.get_instance(request={'name': "instance_name"})
```

### More Details

In `google-cloud-redis<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_instance(
        self,
        parent,
        instance_id,
        instance,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_instance(
        self,
        request: cloud_redis.CreateInstanceRequest = None,
        *,
        parent: str = None,
        instance_id: str = None,
        instance: cloud_redis.Instance = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_instance(
    request={
        "parent": parent,
        "instance_id": instance_id,
        "instance": instance,
    }
)
```

```py
response = client.create_instance(
    parent=parent,
    instance_id=instance_id,
    instance=instance,
)
```

This call is invalid because it mixes `request` with a keyword argument `instance`. Executing this code
will result in an error.

```py
response = client.create_instance(
    request={
        "parent": parent,
    },
    instance_id=instance_id,
    instance=instance,
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import redis_v1

state = redis_v1.enums.Instance.State.STATE_UNSPECIFIED
instance = redis_v1.types.Instance(name="name")
```


**After:**
```py
from google.cloud import redis_v1

state = redis_v1.Instance.State.STATE_UNSPECIFIED
instance = redis_v1.Instance(name="name")
```

## Location Path Helper Method

Location path helper method has been removed. Please construct
the path manually.

```py
project = 'my-project'
location = 'location'

location_path = f'projects/{project}/locations/{location}'
```
