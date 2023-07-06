# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-language` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-language/issues).

## Supported Python Versions

> **WARNING**: Breaking change
The 2.0.0 release requires Python 3.6+.

## Method Calls

> **WARNING**: Breaking change
Methods expect request objects. We provide a script that will convert most common use cases.
* Install the library and `libcst`.

```py
python3 -m pip install google-cloud-language[libcst]
```

* The script `fixup_language_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_language_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import language_v1
language = language_v1.LanguageClient()
return language.analyze_sentiment(document=document).document_sentiment
```


**After:**
```py
from google.cloud import language_v1
language = language_v1.LanguageServiceClient()
return language.analyze_sentiment(request={'document': document}).document_sentiment
```

### More Details

In `google-cloud-language<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def analyze_sentiment(
        self,
        document,
        encoding_type=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def analyze_sentiment(
        self,
        request: language_service.AnalyzeSentimentRequest = None,
        *,
        document: language_service.Document = None,
        encoding_type: language_service.EncodingType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> language_service.AnalyzeSentimentResponse:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.
Both of these calls are valid:

```py
response = client.analyze_sentiment(
    request={
        "document": document,
        "encoding_type": encoding_type
    }
)
```

```py
response = client.analyze_sentiment(
    document=document,
    encoding_type=encoding_type
    )  # Make an API request.
```

This call is invalid because it mixes `request` with a keyword argument `entry_group`. Executing this code
will result in an error.

```py
response = client.analyze_sentiment(
    request={
        "document": document
    },
    encoding_type=encoding_type
)
```



## Enums and Types


> **WARNING**: Breaking change
The submodules `enums` and `types` have been removed.
**Before:**
```py
from google.cloud import language_v1
document = language_v1.types.Document(content=text, type=language_v1.enums.Document.Type.PLAIN_TEXT)
encoding_type = language_v1.enums.EncodingType.UTF8
```


**After:**
```py
from google.cloud import language_v1
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
encoding_type = language_v1.EncodingType.UTF8
```

## Project Path Helper Methods

The project path helper method `project_path` has been removed. Please construct
this path manually.

```py
project = 'my-project'
project_path = f'projects/{project}'
