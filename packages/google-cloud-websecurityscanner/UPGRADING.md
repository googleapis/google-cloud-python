# 1.0.0 Migration Guide

The 1.0 release of the `google-cloud-websecurityscanner` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-websecurityscanner/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-websecurityscanner
```

* The script `fixup_websecurityscanner_v1alpha_keywords.py` and `fixup_websecurityscanner_v1beta_keywords.py` are shipped with the library. It expects an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_websecurityscanner_v1beta_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import websecurityscanner_v1beta

client = websecurityscanner_v1beta.WebSecurityScannerClient()

scan_configs = client.list_scan_configs(parent=parent)
```


**After:**
```py
from google.cloud import websecurityscanner_v1beta

client = websecurityscanner_v1beta.WebSecurityScannerClient()

scan_configs = client.list_scan_configs(request = {'parent': parent})
```

### More Details

In `google-cloud-websecurityscanner<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def update_scan_config(
        self,
        scan_config,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/websecurityscanner/v1beta/web_security_scanner.proto#L84) specified by the API producer.


**After:**
```py
    def update_scan_config(
        self,
        request: web_security_scanner.UpdateScanConfigRequest = None,
        *,
        scan_config: gcw_scan_config.ScanConfig = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcw_scan_config.ScanConfig:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.update_scan_config(
    request={
        "scan_config": scan_config,
        "update_mask": update_mask
    }
)
```

```py
response = client.update_scan_config(
    scan_config=scan_config,
    update_mask=update_mask
)
```

This call is invalid because it mixes `request` with a keyword argument `update_mask`. Executing this code
will result in an error.

```py
response = client.update_scan_config(
    request={ "scan_config": scan_config },
    update_mask=update_mask
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import websecurityscanner_v1beta

risk_level = websecurityscanner_v1beta.enums.ScanConfig.RiskLevel.LOW
finding = websecurityscanner_v1beta.types.Finding(name="name")
```


**After:**
```py
from google.cloud import websecurityscanner_v1beta

risk_level = websecurityscanner_v1beta.ScanConfig.RiskLevel.LOW
finding = websecurityscanner_v1beta.Finding(name="name")
```
