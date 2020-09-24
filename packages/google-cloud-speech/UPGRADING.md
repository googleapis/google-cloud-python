# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-speech` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-speech/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-speech
```

* The scripts `fixup_speech_v1_keywords.py` and `fixup_speech_v1p1beta1_keywords.py` are shipped with the library. It expects an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_speech_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import speech

client = speech.SpeechClient()

response = client.recognize(config, audio)
```


**After:**
```py
from google.cloud import speech

client = speech.SpeechClient()

request = speech.RecognizeRequest(request={"config": config, "audio": audio})
response = client.list_voices(request=request)
```

### More Details

In `google-cloud-speech<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def recognize(
        self,
        config,
        audio,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/3dbeac0d54125b123c8dfd39c774b37473c36944/google/cloud/speech/v1/cloud_speech.proto#L48) specified by the API producer.


**After:**
```py
    def recognize(
        self,
        request: cloud_speech.RecognizeRequest = None,
        *,
        config: cloud_speech.RecognitionConfig = None,
        audio: cloud_speech.RecognitionAudio = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_speech.RecognizeResponse:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.recognize(
    request={
        "config": config,
        "audio": audio,
    }
)
```

```py
response = client.recognize(
    config=config,
    audio=audio,
)
```

This call is invalid because it mixes `request` with a keyword argument `audio_config`. Executing this code
will result in an error.

```py
response = client.recognize(
    request={
        "config": config,
    },
    audio=audio,
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import speech

encoding = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16
audio = speech.types.RecognitionAudio(content=content)
```


**After:**
```py
from google.cloud import speech

encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
audio = speech.RecognitionAudio(content=content)
```