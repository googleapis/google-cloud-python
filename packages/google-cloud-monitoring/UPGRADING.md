# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-monitoring` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-monitoring/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library and `libcst.`

```py
python3 -m pip install google-cloud-monitoring libcst
```

* The script `fixup_monitoring_v3_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_monitoring_v3_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

metric_descriptor = client.get_metric_descriptor("name")
```


**After:**
```py
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

metric_descriptor = client.get_metric_descriptor(request={"name": "name"})
```

### More Details

In `google-cloud-monitoring<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_metric_descriptor(
        self,
        name,
        metric_descriptor,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_metric_descriptor(
        self,
        request: metric_service.CreateMetricDescriptorRequest = None,
        *,
        name: str = None,
        metric_descriptor: ga_metric.MetricDescriptor = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ga_metric.MetricDescriptor:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_metric_descriptor(
    request={
        "name": name,
        "metric_descriptor": metric_descriptor
    }
)
```

```py
response = client.create_metric_descriptor(
    name=name,
    metric_descriptor=metric_descriptor
)
```

This call is invalid because it mixes `request` with a keyword argument `metric_descriptor`. Executing this code
will result in an error.

```py
response = client.create_metric_descriptor(
    request={
        "name": name,
    },
    metric_descriptor=metric_descriptor
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import monitoring_v3

launch_stage = monitoring_v3.enums.LaunchStage.ALPHA
policy = monitoring_v3.types.AlertPolicy(name="name")
```


**After:**
```py
from google.cloud import monitoring_v3

launch_stage = monitoring_v3.LaunchStage.ALPHA
policy = monitoring_v3.AlertPolicy(name="name")
```

## Project Path Helper Method

`project_path` method is renamed `common_project_path`.

**Before:**
```py
project_path = client.project_path("project_id")
```

**After:**
```py
project_path = client.common_project_path("project_id")
```
