# 1.0.0 Migration Guide

The 1.0 release of the `google-cloud-securitycenter` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-securitycenter/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-securitycenter
```

* The script `fixup_securitycenter_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_securitycenter_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import securitycenter

client = securitycenter.SecurityCenterClient()

assets = client.list_assets(
    org_name, filter_=project_filter, read_time=timestamp_proto
)
```


**After:**
```py
from google.cloud import securitycenter

client = securitycenter.securitycenterClient()

assets = client.list_assets(
   request={
    "org_name": org_name, 
    "filter_:": project_filter,
    "read_time": timestamp_proto
    }
)
```

### More Details

In `google-cloud-securitycenter<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_assets(
        self,
        parent,
        filter_=None,
        order_by=None,
        read_time=None,
        compare_duration=None,
        field_mask=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def list_assets(
        self,
        request: securitycenter_service.ListAssetsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAssetsPager:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.set_finding_state(
    request={
        "name": name,
        "state": state,
        "start_time": start_time,
    }
)
```

```py
response = client.set_finding_state(
    name=name,
    state=state,
    start_time=start_time
)
```

This call is invalid because it mixes `request` with a keyword argument `start_time`. Executing this code
will result in an error.

```py
response = client.set_finding_state(
    request={
        "name": name,
        "state": state,
    },
    start_time=start_time
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import securitycenter

finding = securitycenter.types.Finding()
```

**After:**
```py

from google.cloud import securitycenter

finding = securitycenter.Finding()
```

## Datetime and Timedelta

Native Python datetime and timedeltas can be passed to the library.

```py
from google.cloud import securitycenter

client = securitycenter.SecurityCenterClient()

read_time = datetime.utcnow() - timedelta(days=1)

group_result_iterator = client.group_findings(
    request={
        "parent": source_name,
        "group_by": "category",
        "read_time": read_time,
    }
)
```

