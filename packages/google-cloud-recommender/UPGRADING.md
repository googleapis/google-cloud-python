# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-recommender` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-recommender/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-recommender
```

* The script `fixup_recommender_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_recommender_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import recommender

client = recommender.RecommenderClient()
name = client.insight_path('[PROJECT]', '[LOCATION]', '[INSIGHT_TYPE]', '[INSIGHT]')
etag = "my_etag"
response = client.mark_insight_accepted(name=name, etag=etag)
```


**After:**
```py
from google.cloud import recommender

client = recommender.RecommenderClient()
name = client.insight_path('[PROJECT]', '[LOCATION]', '[INSIGHT_TYPE]', '[INSIGHT]')
etag = "my_etag"
response = client.mark_insight_accepted(request={"name": name, "etag": etag})
```

### More Details

In `google-cloud-recommender<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def mark_insight_accepted(
        self,
        name,
        etag,
        state_metadata=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/recommender/v1/recommender_service.proto#L70) specified by the API producer.


**After:**
```py
    def mark_insight_accepted(
        self,
        request: recommender_service.MarkInsightAcceptedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkInsightAcceptedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> insight.Insight:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.mark_insight_accepted(
    request={
        "name": name,
        "etag": my_etag
    }
)
```

```py
response = client.mark_insight_accepted(
    name=name,
    etag=my_etag
)
```

This call is invalid because it mixes `request` with a keyword argument `etag`. Executing this code
will result in an error.

```py
response = client.mark_insight_accepted(
    request={
        "name": name
    },
    etag=my_etag
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import recommender

insight = recommender.enums.Insight.Category.PERFORMANCE]
cost_projection = recommender.types.CostProjection()
```


**After:**
```py
from google.cloud import recommender

features = recommender.Insight.Category.PERFORMANCE
cost_projection = recommender.CostProjection()
```