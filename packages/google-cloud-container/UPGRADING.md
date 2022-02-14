# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-container` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-container/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with the `libcst` extra.

```py
python3 -m pip install google-cloud-container[libcst]
```

* The script `fixup_container_v1_keywords.py` and `fixup_container_v1beta1_keywords.py`
are shipped with the library. It expects an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_container_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

clusters = client.list_clusters(
  project_id="project_id", zone="us-central1-a", parent="parent"
)
```


**After:**
```py
from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

clusters = client.list_clusters(
  request = {'project_id': "project_id", 'zone': "us-central1-a", 'parent': "parent"}
)
```

### More Details

In `google-cloud-container<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def list_clusters(
        self,
        project_id=None,
        zone=None,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/container/v1/cluster_service.proto#L48) specified by the API producer.


**After:**
```py
    def list_clusters(
        self,
        request: cluster_service.ListClustersRequest = None,
        *,
        project_id: str = None,
        zone: str = None,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cluster_service.ListClustersResponse:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.list_clusters(
    request={
        "project_id": project_id,
        "zone": zone,
        "parent": parent,
    }
)
```

```py
response = client.list_clusters(
    project_id=project_id,
    zone=zone,
    parent=parent,
)
```

This call is invalid because it mixes `request` with a keyword argument `parent`. Executing this code will result in an error.

```py
response = client.list_clusters(
    request={
        "project_id": project_id,
        "zone": zone,
    },
    parent=parent
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import container

status = container.enums.Cluster.Status.RUNNING
cluster = container.types.Cluster(name="name")
```


**After:**
```py
from google.cloud import container

status = container.Cluster.Status.RUNNING
cluster = container.Cluster(name="name")
```
