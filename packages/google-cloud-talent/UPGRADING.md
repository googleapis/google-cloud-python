# 1.0.0 Migration Guide

The 1.0.0 release of the `google-cloud-talent` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-talent/issues).

## Supported Python Versions

> **WARNING**: Breaking change
The 1.0.0 release requires Python 3.6+.

## Method Calls

> **WARNING**: Breaking change
Methods expect request objects. We provide a script that will convert most common use cases.
* Install the library
```py
python3 -m pip install google-cloud-talent
```

* The scripts `fixup_talent_v4beta1_keywords.py` shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_talent_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import talent_v4beta1
client = talent_v4beta1.JobServiceClient()
parent = client.project_path('[PROJECT]')
# TODO: Initialize `jobs`:
jobs = []
response = client.batch_create_jobs(parent, jobs)
```

**After:**
```py
response = client.batch_create_jobs(request={"parent": "''", "jobs": "[]"})
```

### More Details

In `google-cloud-talent<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def batch_create_jobs(
        self,
        parent,
        jobs,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation] (https://github.com/googleapis/googleapis/blob/master/google/cloud/talent/v4beta1/job_service.proto#L73) specified by the API producer.


**After:**
```py
    def batch_create_jobs(
        self,
        request: job_service.BatchCreateJobsRequest = None,
        *,
        parent: str = None,
        jobs: Sequence[job.Job] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.
Both of these calls are valid:
```py
response = client.batch_create_jobs(
    request={
        "parent": parent,
        "jobs": jobs,
    }
)
```

```py
response = client.batch_create_jobs(
    parent=parent,
    jobs=jobs,
)
```

This call is invalid because it mixes `request` with a keyword argument `jobs`. Executing this code will result in an error.

```py
response = client.batch_create_jobs(
    request={
        "parent": parent,
    },
    jobs=jobs
)
```