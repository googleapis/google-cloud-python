# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-dlp` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-dlp/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library and `libcst`.

```py
python3 -m pip install google-cloud-dlp[libcst]
```

* The script `fixup_dlp_v2_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_dlp_v2_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import dlp

client = dlp.DlpServiceClient()

template = client.get_inspect_template(name="name")
```


**After:**
```py
from google.cloud import dlp

client = dlp.DlpServiceClient()

template = client.get_inspect_template(request={"name": "name"})
```

### More Details

In `google-cloud-dlp<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_inspect_template(
        self,
        parent,
        inspect_template,
        template_id=None,
        location_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_inspect_template(
        self,
        request: dlp.CreateInspectTemplateRequest = None,
        *,
        parent: str = None,
        inspect_template: dlp.InspectTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_inspect_template(
    request={
        "parent": parent,
        "inspect_template": inspect_template,
    }
)
```

```py
response = client.create_inspect_template(
    parent=parent,
    inspect_template=inspect_template,
)
```

This call is invalid because it mixes `request` with a keyword argument `inspect_template`. Executing this code will result in an error.

```py
response = client.list_builds(
    request={
        "parent": parent,
    },
    inspect_template=inspect_template
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import dlp

file_type = dlp.enums.FileType.IMAGE
finding = dlp.types.Finding(name="name")
```


**After:**
```py
from google.cloud import dlp

file_type = dlp.FileType.IMAGE
finding = dlp.Finding(name="name")
```

## Path Helper Methods

The following path helper methods have been removed. Please construct
these paths manually.

```py
project = 'my-project'
dlp_job = 'dlp-job'
location = 'location'

project_path = f'projects/{project}'
dlp_job_path = f'projects/{project}/dlpJobs/{dlp_job}'
location_path = f'projects/{project}/locations/{location}'
```
