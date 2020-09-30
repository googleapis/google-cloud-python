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

The 2.0 release of the `google-cloud-bigquery` client drops support for Python
versions below 3.6. The client surface itself has not changed, but the 1.x series
will not be receiving any more feature updates or bug fixes. You are thus
encouraged to upgrade to the 2.x series.

If you experience issues or have questions, please file an
[issue](https://github.com/googleapis/python-bigquery/issues).


## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Supported BigQuery Storage Clients

The 2.0.0 release requires BigQuery Storage `>= 2.0.0`, which dropped support
for `v1beta1` and `v1beta2` versions of the BigQuery Storage API. If you want to
use a BigQuery Storage client, it must be the one supporting the `v1` API version.


## Changed GAPIC Enums Path

> **WARNING**: Breaking change

Generated GAPIC enum types have been moved under `types`. Import paths need to be
adjusted.

**Before:**
```py
from google.cloud.bigquery_v2.gapic import enums

distance_type = enums.Model.DistanceType.COSINE
```

**After:**
```py
from google.cloud.bigquery_v2 import types

distance_type = types.Model.DistanceType.COSINE
```