# 1.0.0 Migration Guide

The 1.0 release of the `grafeas` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/grafeas/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install grafeas
```

* The script `fixup_grafeas_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_grafeas_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from grafeas import grafeas_v1
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport

address = "[SERVICE_ADDRESS]"
scopes = ("[SCOPE]")
transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

client = grafeas_v1.GrafeasClient(transport)

parent = "projects/my-project"
notes = client.list_notes(parent)
```


**After:**
```py
from grafeas import grafeas_v1
from grafeas.grafeas_v1.services.grafeas.transports import GrafeasGrpcTransport

address = "[SERVICE_ADDRESS]"
scopes = ("[SCOPE]")
transport = GrafeasGrpcTransport(host=address scopes=scopes)

client = grafeas_v1.GrafeasClient(transport=transport)

parent = "projects/my-project"
request = {"parent": parent}
notes = client.list_notes(request=request)
```

### More Details

In `grafeas<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_notes(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/b77cacf1ed06e0301a39d6328b599e24102f04be/grafeas/v1/grafeas.proto#L763) specified by the API producer.


**After:**
```py
    def list_notes(self,
            request: grafeas.ListNotesRequest = None,
            *,
            parent: str = None,
            filter: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListNotesPager:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.list_notes(
    request={
        "parent": parent,
        "filter": filter,
    }
)
```

```py
response = client.list_notes(
    parent=parent,
    filter=filter,
)
```

This call is invalid because it mixes `request` with a keyword argument `filter`. Executing this code
will result in an error.

```py
response = client.list_notes(
    request={
        "parent": parent,
    },
    filter=filter
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from grafeas import grafeas_v1

severity = grafeas_v1.gapic.enums.Severity.HIGH
request = grafeas_v1.types.ListOccurrencesRequest()
```


**After:**
```py
from grafeas import grafeas_v1

severity = grafeas_v1.Severity.HIGH
request = grafeas_v1.ListOccurrencesRequest()
```

## Project Path Helper Method

The project path helper method `project_path` has been removed. Please construct this path manually.

```py
project = 'my-project'
project_path = f'projects/{project}'
```