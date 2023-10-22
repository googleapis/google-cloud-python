# 3.0.0 Migration Guide

The 3.0 release of the `google-cloud-translate` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-translate/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 3.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library and `libcst`.

```py
python3 -m pip install google-cloud-translate libcst
```

* The script `fixup_translation_{version}_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_translation_v3_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import translate

client = translate.TranslationServiceClient()
parent = client.location_path("<PROJECT_ID>", "<LOCATION>")
text = "Good morning!"

response = client.translate_text(
    parent=parent,
    contents=[text],
    mime_type="text/plain",
    source_language_code="en-US",
    target_language_code="fr",
)
```


**After:**
```py
from google.cloud import translate

client = translate.TranslationServiceClient()
parent = "projects/<PROJECT_ID>/locations/<LOCATION>"
text = "Good morning!"

response = client.translate_text(
    request={
        "parent": parent,
        "contents": [text],
        "mime_type": "text/plain",
        "source_language_code": "en-US",
        "target_language_code": "fr"
    }
)
```

### More Details

In `google-cloud-translate<3.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def translate_text(
        self,
        contents,
        target_language_code,
        parent,
        mime_type=None,
        source_language_code=None,
        model=None,
        glossary_config=None,
        labels=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 3.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/translate/v3/translation_service.proto#L55) specified by the API producer.


**After:**
```py
    def translate_text(
        self,
        request: translation_service.TranslateTextRequest = None,
        *,
        parent: str = None,
        target_language_code: str = None,
        contents: Sequence[str] = None,
        model: str = None,
        mime_type: str = None,
        source_language_code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> translation_service.TranslateTextResponse:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.translate_text(
    request={
        "parent": parent,
        "target_language_code": target_language_code,
        "contents": contents
    }
)
```

```py
response = client.translate_text(
    parent=parent,
    target_language_code=target_language_code,
    contents=contents
)
```

This call is invalid because it mixes `request` with a keyword argument `target_language_code`. Executing this code
will result in an error.

```py
response = client.translate_text(
    request={
        "parent": parent,
        "contents": contents,
    },
    target_language_code=target_language_code
)
```



## Enums and types


> **WARNING**: Breaking change

The submodule `enums` (containing enum classes for long running operation State) has been removed.

The submodule `types` is still present. When using the primary version module alias (`translate`)
it is possible to access the types classes directly.

```py
from google.cloud import translate  # the primary version is imported by default

client = translate.TranslationServiceClient()

glossary_config = client.TranslateTextGlossaryConfig(
    glossary=glossary_path
)
```

When a specific version is imported, the full module name must be specified to access types classes.

```py
from google.cloud import translate_v3beta1 as translate

client = translate.TranslationServiceClient()

glossary_config = client.types.TranslateTextGlossaryConfig(
    glossary=glossary_path
)
```
