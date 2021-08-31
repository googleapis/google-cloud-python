# 1.0.0 Migration Guide

The 1.0 release of the `google-cloud-trace` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-trace/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Handwritten Client Wrapper Removal

The handwritten client wrapper `trace_v1.Client()` and `trace_v2.Client()` have been removed. Please use `TraceServiceClient` directly. The primary diference is that a `project_id` must always be supplied to method calls.


```py
from google.cloud import trace_v1

client = trace_v1.TraceServiceClient()
```

```py
from google.cloud import trace_v2

client = trace_v2.TraceServiceClient()
```

**NOTE**: The following sections identify changes between the previous `TraceServiceClient()` and the current `TraceServiceClient()` (not the handwritten wrapper `Client()`). If you were previously using `Client()`, it may be more helpful to reference the [samples](https://github.com/googleapis/python-trace/tree/main/samples/snippets).

## Method Calls

> **WARNING**: Breaking change
Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-trace
```

* The scripts `fixup_trace_v1_keywords.py` and `fixup_trace_v2_keywords.py` are shipped with the library. The script expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_trace_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import trace_v1

client = trace_v1.TraceServiceClient()
project_id = "my-project"
response = client.list_traces(project_id)
```


**After:**
```py
from google.cloud import trace_v1

client = trace_v1.TraceServiceClient()
project_id = "my-project"
response = client.list_traces(project_id=project_id)
```

### More Details

In `google-cloud-trace<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def get_trace(
        self,
        project_id,
        trace_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/devtools/cloudtrace/v2/tracing.proto#L53) specified by the API producer.


**After:**
```py
    def get_trace(
        self,
        request: trace.GetTraceRequest = None,
        *,
        project_id: str = None,
        trace_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> trace.Trace:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.get_trace(
    request={
        "project_id": project_id,
        "trace_id", trace_id,
    }
)
```

```py
response = client.get_trace(
    project_id=project_id,
    trace_id=trace_id,
)
```

This call is invalid because it mixes `request` with a keyword argument `trace_id`. Executing this code
will result in an error.

```py
response = client.get_trace(
    request={
        "project_id": project_id,
    },
    trace_id=trace_id,
)
```



## Enums and Types


**WARNING**: Breaking change

The submodules `types` is no longer available on the unversioned path `trace`.

**Before:**
```py
from google.cloud import trace

trace_ = trace.types.TraceSpan()
```


**After:**
```py
from google.cloud

trace_ = trace_v1.TraceSpan()
trace_ = trace_v1.types.TraceSpan()
```
