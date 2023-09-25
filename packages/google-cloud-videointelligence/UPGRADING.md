# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-videointelligence` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-videointelligence/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-videointelligence
```

* The script `fixup_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()
input_uri = "gs://cloud-samples-data/video/cat.mp4"
features = [videointelligence.enums.Feature.LABEL_DETECTION]
operation = client.annotate_video(
    input_uri=input_uri, features=features
)
```


**After:**
```py
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()
input_uri = "gs://cloud-samples-data/video/cat.mp4"
features = [videointelligence.Feature.LABEL_DETECTION]
operation = client.annotate_video(request={"input_uri": input_uri, "features": features})
```

### More Details

In `google-cloud-videointelligence<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def annotate_video(
        self,
        input_uri=None,
        input_content=None,
        features=None,
        video_context=None,
        output_uri=None,
        location_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/videointelligence/v1/video_intelligence.proto#L51) specified by the API producer.


**After:**
```py
    def annotate_video(
        self,
        request: video_intelligence.AnnotateVideoRequest = None,
        *,
        input_uri: str = None,
        features: Sequence[video_intelligence.Feature] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.annotate_video(
    request={
        "input_uri": input_uri,
        "features": features
    }
)
```

```py
response = client.annotate_video(
    input_uri=input_uri
    features=features
)
```

This call is invalid because it mixes `request` with a keyword argument `features`. Executing this code
will result in an error.

```py
response = client.annotate_video(
    request={
        "input_uri": input_uri
    },
    features=features
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import videointelligence

features = [videointelligence.enums.Feature.TEXT_DETECTION]
video_context = videointelligence.types.VideoContext()
```


**After:**
```py
from google.cloud import videointelligence

features = [videointelligence.Feature.TEXT_DETECTION]
video_context = videointelligence.VideoContext()
```
