# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-build` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-cloudbuild/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-build[libcst]
```

* The script `fixup_cloudbuild_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_cloudbuild_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud.devtools import cloudbuild

client = cloudbuild.CloudBuildClient()

build = client.get_build("project_id")
```


**After:**
```py
from google.cloud.devtools import cloudbuild

client = cloudbuild.CloudBuildClient()

build = client.get_build(request = {'project_id': "project_id"})
```

### More Details

In `google-cloud-build<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_builds(
        self,
        project_id,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/devtools/cloudbuild/v1/cloudbuild.proto#L82) specified by the API producer.


**After:**
```py
    def list_builds(
        self,
        request: cloudbuild.ListBuildsRequest = None,
        *,
        project_id: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildsPager:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.list_builds(
    request={
        "project_id": project_id,
        "filter": filter,
    }
)
```

```py
response = client.list_builds(
    project_id=project_id,
    filter=filter,
)
```

This call is invalid because it mixes `request` with a keyword argument `filter`. Executing this code
will result in an error.

```py
response = client.list_builds(
    request={
        "project_id": project_id,
    },
    filter=filter
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud.devtools import cloudbuild

build_status = cloudbuild.enums.Build.Status.SUCCESS
built_image = cloudbuild.types.BuiltImage(name="name")
```


**After:**
```py
from google.cloud.devtools import cloudbuild

build_status = cloudbuild.Build.Status.SUCCESS
built_image = cloudbuild.BuiltImage(name="name")
```
