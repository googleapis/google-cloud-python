# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-webrisk` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-webrisk/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library and `libcst >= 0.2.5`.

```py
python3 -m pip install google-cloud-webrisk libcst >= 0.2.5
```

* The scripts `fixup_webrisk_v1_keywords.py` and  `fixup_webrisk_v1beta1_keywords.py` shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_webrisk_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import webrisk_v1

client = webrisk_v1.WebRiskServiceClient()
# TODO: Initialize `threat_types`:
threat_types = []

response = client.search_hashes(threat_types)
```


**After:**
```py
from google.cloud import webrisk_v1

client = webrisk_v1.WebRiskServiceClient()

response = client.search_hashes(request={"threat_types": "[]"})

```

### More Details

In `google-cloud-webrisk<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def search_hashes(
        self,
        threat_types,
        hash_prefix=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/webrisk/v1/webrisk.proto#L74) specified by the API producer.


**After:**
```py
    def search_hashes(
        self,
        request: webrisk.SearchHashesRequest = None,
        *,
        hash_prefix: bytes = None,
        threat_types: Sequence[webrisk.ThreatType] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> webrisk.SearchHashesResponse:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.search_hashes(
    request={
        "hash_prefix": hash_prefix,
        "threat_types": threat_types,
    }
)
```

```py
response = client.search_hashes(
    hash_prefix=hash_prefix,
    threat_types=threat_types,
)
```

This call is invalid because it mixes `request` with a keyword argument `threat_types`. Executing this code
will result in an error.

```py
response = client.synthesize_speech(
    request={
        "hash_prefix": hash_prefix,
    },
    threat_types=threat_types
)
```
