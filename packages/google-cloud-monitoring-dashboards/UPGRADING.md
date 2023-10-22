# 2.0.0 Migration Guide

The 1.0 release of the `google-cloud-monitoring-dashboards` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-monitoring-dashboards/issues).

## Supported Python Versions

> **WARNING**: Breaking change
The 2.0.0 release requires Python 3.6+.

## Create Service Client
> **WARNING**: Breaking change
The namespace for importing the service gets changed in the new release.


**Before:**
```py
from google.cloud.monitoring_dashboard import v1
client = v1.DashboardsServiceClient()
```
**After:**
```py
from google.cloud import monitoring_dashboard_v1
client = monitoring_dashboard_v1.DashboardsServiceClient()
```

## Method Calls

> **WARNING**: Breaking change
Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-monitoring-dashboards[libcst]
```

* The scripts `fixup_dashboard_v1_keywords.py` shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_dashboard_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
# TODO: Initialize `parent`:
parent = ''
# TODO: Initialize `dashboard`:
dashboard = {}
response = client.create_dashboard(parent, dashboard)
```

**After:**
```py
response = client.create_dashboard(request={"parent": "''", "dashboard": "{}"})
```

### More Details

In `google-cloud-monitoring-dashboards<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_dashboard(
        self,
        parent,
        dashboard,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation] specified by the API producer.


**After:**
```py
    def create_dashboard(
        self,
        request: dashboards_service.CreateDashboardRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dashboard.Dashboard:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.
Both of these calls are valid:

```py
response = client.create_dashboard(
    request={
        "parent": parent,
        "dashboard": dashboard,
    }
)
```

```py
response = client.create_dashboard(
    parent=parent,
    dashboard=dashboard,
)
```

This call is invalid because it mixes `request` with a keyword argument `dashboard`. Executing this code will result in an error.

```py
response = client.create_dashboard(
    request={
        "parent": parent,
    },
    dashboard=dashboard
)
```
