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

The 2.0 release of the `google-cloud-bigquery-storage` client is a significant
upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python),
and includes substantial interface changes. Existing code written for earlier versions
of this library will likely require updates to use this version. This document
describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an
[issue](https://github.com/googleapis/python-bigquery-storage/issues).


## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Import Path

The library's top-level namespace is `google.cloud.bigquery_storage`. Importing
from `google.cloud.bigquery_storage_v1` still works, but it is advisable to use
the `google.cloud.bigquery_storage` path in order to reduce the chance of future
compatibility issues should the library be restuctured internally.

**Before:**
```py
from google.cloud.bigquery_storage_v1 import BigQueryReadClient
```

**After:**
```py
from google.cloud.bigquery_storage import BigQueryReadClient
```


## Enum Types

> **WARNING**: Breaking change

Enum types have been moved. Access them through the `types` module.

**Before:**
```py
from google.cloud.bigquery_storage_v1 import enums

data_format = enums.DataFormat.ARROW
```

data_format = BigQueryReadClient.enums.DataFormat.ARROW

**After:**
```py
from google.cloud.bigquery_storage import types

data_format = types.DataFormat.ARROW
```

Additionally, enums cannot be accessed through the client anymore. The following
code wil _not_ work:
```py
data_format = BigQueryReadClient.enums.DataFormat.ARROW
```


## Clients for Beta APIs

> **WARNING**: Breaking change

Clients for beta APIs have been removed. The following import will _not_ work:

```py
from google.cloud.bigquery_storage_v1beta1 import BigQueryStorageClient
from google.cloud.bigquery_storage_v1beta2.gapic.big_query_read_client import BigQueryReadClient
```

The beta APIs are still available on the server side, but you will need to use
the 1.x version of the library to access them.


## Changed Default Value of the `read_rows()` Method's `metadata` Argument

The `client.read_rows()` method does not accept `None` anymore as a valid value
for the optional `metadata` argument. If not given, an empty tuple is used, but
if you want to explicitly pass an "empty" value, you should use an empty tuple, too.

**Before:**
```py
client.read_rows("stream_name", metadata=None)
```

**After:**
```py
client.read_rows("stream_name", metadata=())
```

OR

```py
client.read_rows("stream_name")
```


## Method Calls

> **WARNING**: Breaking change

Most of the client methods that send requests to the backend expect request objects.
We provide a script that will convert most common use cases.

> One exception to this is the `BigQueryReadClient.read_rows()` which is a hand-written
wrapper around the auto-generated `read_rows()` method.

* Install the library

```py
python3 -m pip install google-cloud-bigquery-storage
```

* The script `fixup_storage_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ scripts/fixup_storage_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import bigquery_storage_v1

client = bigquery_storage_v1.BigQueryReadClient()

requested_session = bigquery_storage_v1.types.ReadSession()
requested_session.table = "projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID"
requested_session.data_format = bigquery_storage_v1.enums.DataFormat.ARROW

session = client.create_read_session(
    "projects/parent_project",
    requested_session,
    max_stream_count=1,
)
```

**After:**
```py
from google.cloud import bigquery_storage

client = bigquery_storage.BigQueryReadClient()

requested_session = bigquery_storage.types.ReadSession(
    table="projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID",
    data_format=bigquery_storage.types.DataFormat.ARROW,
)
session = client.create_read_session(
    request={
        "parent": "projects/parent_project",
        "read_session": requested_session,
        "max_stream_count" 1,
    },
)
```

### More Details

In `google-cloud-bigquery-storage<2.0.0`, parameters required by the API were positional
parameters and optional parameters were keyword parameters.

**Before:**
```py
def create_read_session(
    self,
    parent,
    read_session,
    max_stream_count=None,
    retry=google.api_core.gapic_v1.method.DEFAULT,
    timeout=google.api_core.gapic_v1.method.DEFAULT,
    metadata=None,
):
```

In the `2.0.0` release, methods that interact with the backend have a single
positional parameter `request`. Method docstrings indicate whether a parameter is
required or optional.

Some methods have additional keyword only parameters. The available parameters depend
on the [`google.api.method_signature` annotation](https://github.com/googleapis/python-bigquery-storage/blob/9e1bf910e6f5010f479cf4592e25c3b3eebb456d/google/cloud/bigquery_storage_v1/proto/storage.proto#L73)
specified by the API producer.


**After:**
```py
def create_read_session(
    self,
    request: storage.CreateReadSessionRequest = None,
    *,
    parent: str = None,
    read_session: stream.ReadSession = None,
    max_stream_count: int = None,
    retry: retries.Retry = gapic_v1.method.DEFAULT,
    timeout: float = None,
    metadata: Sequence[Tuple[str, str]] = (),
) -> stream.ReadSession:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are
> mutually exclusive. Passing both will result in an error.

Both of these calls are valid:

```py
session = client.create_read_session(
    request={
        "parent": "projects/parent_project",
        "read_session": requested_session,
        "max_stream_count" 1,
    },
)
```

```py
response = client.create_read_session(
    parent="projects/parent_project",
    read_session=requested_session,
    max_stream_count=1,
)
```

This call is _invalid_ because it mixes `request` with a keyword argument
`max_stream_count`. Executing this code will result in an error:

```py
session = client.create_read_session(
    request={
        "parent": "projects/parent_project",
        "read_session": requested_session,
    },
    max_stream_count=1,
)
```

> **NOTE:** The `request` parameter of some methods can also contain a more rich set of
> options that are otherwise not available as explicit keyword only parameters, thus
> these _must_ be passed through `request`.


## Removed Utility Methods

> **WARNING**: Breaking change

Several utility methods such as `project_path()` and `table_path()` have been removed.
These paths must now be constructed manually:

```py
project_path = f"project/{PROJECT_ID}"
table_path = f"projects/{PROJECT_ID}/datasets/{DATASET_ID}/tables/{TABLE_ID}"
```

The two that remained are `read_session_path()` and `read_stream_path()`.


## Removed `client_config` and `channel` Parameter

The client cannot be constructed with `channel` or `client_config` arguments anymore,
these deprecated parameters have been removed.

If you used `client_config` to customize retry and timeout settings for a particular
method, you now need to do it upon method invocation by passing the custom `timeout` and
`retry` arguments, respectively.
