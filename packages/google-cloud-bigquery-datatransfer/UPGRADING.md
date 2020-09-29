<!-- 
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->


# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-bigquery-datatransfer` client is a significant
upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python),
and includes substantial interface changes. Existing code written for earlier versions
of this library will likely require updates to use this version. This document
describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an
[issue](https://github.com/googleapis/python-bigquery-datatransfer/issues).


## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Import Path

> **WARNING**: Breaking change


### Version 2.1.0

The library had its old namespace restored, since importing from
`google.cloud.bigquery` clashed with the `google-cloud-bigquery` library when the
latter was also installed.

The import paths that were changed in version `2.0.0` should be reverted:

```py
from google.cloud import bigquery_datatransfer
from google.cloud import bigquery_datatransfer_v1
```

### Version 2.0.0

(obsolete) The library was moved into `google.cloud.bigquery` namespace. Existing
imports need to be updated, unless using a version `>=2.1.0`.

**Before:**
```py
from google.cloud import bigquery_datatransfer
from google.cloud import bigquery_datatransfer_v1
```

**After:**
```py
from google.cloud.bigquery import datatransfer
from google.cloud.bigquery import datatransfer_v1
```


## Method Calls

> **WARNING**: Breaking change

Methods that send requests to the backend expect request objects. We provide a script
that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-bigquery-datatransfer
```

* The script `fixup_datatransfer_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ scripts/fixup_datatransfer_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import bigquery_datatransfer

client = bigquery_datatransfer.DataTransferServiceClient()

parent_project = "..."
transfer_config = {...}
authorization_code = "..."

response = client.create_transfer_config(
    parent_project, transfer_config, authorization_code=authorization_code
)
```


**After:**
```py
from google.cloud.bigquery import datatransfer

client = datatransfer.DataTransferServiceClient()

parent_project = "..."
transfer_config = {...}
authorization_code = "..."

response = client.create_transfer_config(
    request={
        "parent": parent_project,
        "transfer_config": transfer_config,
        "authorization_code": authorization_code,
    }
)
```

### More Details

In `google-cloud-bigquery-datatransfer<2.0.0`, parameters required by the API were positional
parameters and optional parameters were keyword parameters.

**Before:**
```py
def create_transfer_config(
    self,
    parent,
    transfer_config,
    authorization_code=None,
    version_info=None,
    service_account_name=None,
    retry=google.api_core.gapic_v1.method.DEFAULT,
    timeout=google.api_core.gapic_v1.method.DEFAULT,
    metadata=None,
):
```

In the `2.0.0` release, methods that interact with the backend have a single
positional parameter `request`. Method docstrings indicate whether a parameter is
required or optional.

Some methods have additional keyword only parameters. The available parameters depend
on the [`google.api.method_signature` annotation](https://github.com/googleapis/python-bigquery-datatransfer/blob/master/google/cloud/bigquery_datatransfer_v1/proto/datatransfer.proto#L80)
specified by the API producer.


**After:**
```py
def create_transfer_config(
    self,
    request: datatransfer.CreateTransferConfigRequest = None,
    *,
    parent: str = None,
    transfer_config: transfer.TransferConfig = None,
    retry: retries.Retry = gapic_v1.method.DEFAULT,
    timeout: float = None,
    metadata: Sequence[Tuple[str, str]] = (),
) -> transfer.TransferConfig:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are
> mutually exclusive. Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_transfer_config(
    request={
        "parent": project_path,
        "transfer_config": {"foo": "bar"},
    }
)
```

```py
response = client.create_transfer_config(
    parent=project_path,
    transfer_config={"foo": "bar"},
)
```

This call is _invalid_ because it mixes `request` with a keyword argument `transfer_config`.
Executing this code will result in an error:

```py
response = client.create_transfer_config(
    request={"parent": project_path},
    transfer_config= {"foo": "bar"},
)
```

> **NOTE:** The `request` parameter of some methods can also contain a more rich set of
> options that are otherwise not available as explicit keyword only parameters, thus
> these _must_ be passed through `request`.


## Removed Utility Methods

> **WARNING**: Breaking change

Most utility methods such as `project_path()` have been removed. The paths must
now be constructed manually:

```py
project_path = f"project/{PROJECT_ID}"
```

 The only two that remained are `transfer_config_path()` and `parse_transfer_config_path()`.


## Removed `client_config` Parameter

The client cannot be constructed with `client_config` argument anymore, this deprecated
argument has been removed. If you want to customize retry and timeout settings for a particular
method, you need to do it upon method invocation by passing the custom `timeout` and
`retry` arguments, respectively.
