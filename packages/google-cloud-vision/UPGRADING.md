# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-vision` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-vision/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-vision[libcst]
```

* The script `fixup_vision_v1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_vision_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import vision_v1

client = vision_v1.ProductSearchClient()

product_set = client.get_product_set("name")
```


**After:**
```py
from google.cloud import vision_v1

client = vision_v1.ProductSearchClient()

product_set = client.get_product_set(request={"name": "name"})
```

### More Details

In `google-cloud-vision<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_product_set(
        self,
        parent,
        product_set,
        product_set_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the `google.api.method_signature` annotation specified by the API producer.


**After:**
```py
    def create_product_set(
        self,
        request: product_search_service.CreateProductSetRequest = None,
        *,
        parent: str = None,
        product_set: product_search_service.ProductSet = None,
        product_set_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> product_search_service.ProductSet:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_product_set(
    request={
        "parent": parent,
        "product_set_id": product_set_id,
        "product_set": product_set
    }
)
```

```py
response = client.create_product_set(
    parent=parent,
    product_set_id=product_set_id,
    product_set=product_set
)
```

This call is invalid because it mixes `request` with a keyword argument `product_set`. Executing this code
will result in an error.

```py
response = client.create_product_set(
    request={
        "parent": parent,
        "product_set_id": product_set_id
    },
    product_set=product_set
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import vision_v1

likelihood = vision_v1.enums.Likelihood.UNKNOWN
request = vision_v1.types.GetProductSetRequest(name="name")
```


**After:**
```py
from google.cloud import vision_v1

likelihood = vision_v1.Likelihood.UNKNOWN
request = vision_v1.GetProductSetRequest(name="name")
```

## Location Path Helper Method

Loation path helper method has been removed. Please construct
the path manually.

```py
project = "my-project"
location = "location"

location_path = f"projects/{project}/locations/{location}"
```
