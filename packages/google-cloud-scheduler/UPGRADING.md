# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-scheduler` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-scheduler/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst.

```py
python3 -m pip install google-cloud-scheduler[libcst]
```

* The script `fixup_scheduler_{version}_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_scheduler_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import scheduler

client = scheduler.CloudSchedulerClient()

parent = client.location_path("<PROJECT_ID>", "<LOCATION>")
job = {
        'app_engine_http_target': {
            'app_engine_routing': {
                'service': service_id
            },
            'relative_uri': '/log_payload',
            'http_method': 'POST',
            'body': 'Hello World'.encode()
        },
        'schedule': '* * * * *',
        'time_zone': 'America/Los_Angeles'
    }

response = client.create_job(parent, job)
```


**After:**
```py
from google.cloud import scheduler

client = scheduler.CloudSchedulerClient()
parent = "projects/<PROJECT_ID>/locations/<LOCATION>"
job = {
        'app_engine_http_target': {
            'app_engine_routing': {
                'service': service_id
            },
            'relative_uri': '/log_payload',
            'http_method': 'POST',
            'body': 'Hello World'.encode()
        },
        'schedule': '* * * * *',
        'time_zone': 'America/Los_Angeles'
    }

response = client.create_job(
    request={
        "parent": parent,
        "job": job
    }
)
```

### More Details

In `google-cloud-scheduler<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_jobs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/scheduler/v1/cloudscheduler.proto#L45) specified by the API producer.


**After:**
```py
    def list_jobs(
        self,
        request: cloudscheduler.ListJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsPager:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.list_jobs(
    request={
        "parent": parent,
        "timeout": timeout
    }
)
```

```py
response = client.list_jobs(
    parent=parent,
    timeout=timeout
)
```

This call is invalid because it mixes `request` with a keyword argument `metadata`. Executing this code
will result in an error.

```py
response = client.list_jobs(
    request={
        "parent": parent,
        "timeout": timeout,
    },
    metadata=metadata
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import scheduler

http_method = scheduler.enums.HttpMethod.GET
job = scheduler.types.Job(name="name")
```


**After:**
```py
from google.cloud import scheduler

http_method = scheduler.HttpMethod.GET
job = scheduler.Job(name="name")
```
