# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-dataproc` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-dataproc/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-dataproc[libcst]
```

* The script `fixup_dataproc_v1_keywords.py` is shipped with the library. It expects an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_dataproc_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import dataproc

client = dataproc.ClusterControllerClient()

clusters = client.list_clusters(project_id="project_id", region="region")
```


**After:**
```py
from google.cloud import dataproc

client = dataproc.ClusterControllerClient()

clusters = client.list_clusters(request={
    'project_id' : "project_id", 'region' : "region"
})
```

### More Details

In `google-cloud-dataproc<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def get_cluster(
        self,
        project_id,
        region,
        cluster_name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/dataproc/v1/clusters.proto#L88) specified by the API producer.


**After:**
```py
    def get_cluster(
        self,
        request: clusters.GetClusterRequest = None,
        *,
        project_id: str = None,
        region: str = None,
        cluster_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clusters.Cluster:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.get_cluster(
    request={
        "project_id": project_id,
        "region": region,
        "cluster_name": cluster_name
    }
)
```

```py
response = client.get_cluster(
    project_id=project_id,
    region=region,
    cluster_name=cluster_name
)
```

This call is invalid because it mixes `request` with a keyword argument `cluster_name`. Executing this code
will result in an error.

```py
response = client.get_cluster(
    request={
        "project_id": project_id,
        "region": region
    },
    cluster_name=cluster_name
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import dataproc

status = dataproc.enums.ClusterStatus.State.CREATING
cluster = dataproc.types.Cluster(cluster_name="name")
```


**After:**
```py
from google.cloud import dataproc

status = dataproc.ClusterStatus.State.CREATING
cluster = dataproc.Cluster(cluster_name="name")
```

## Path Helper Methods
The following path helper methods have been removed. Please construct the paths manually.

```py
project = 'my-project'
location = 'project-location'
region = 'project-region'
workflow_template = 'template'
autoscaling_policy = 'policy'

location_path = f'projects/{project}/locations/{location}'
region_path = f'projects/{project}/regions/{region}'
workflow_template_path = f'projects/{project}/regions/{region}/workflowTemplates/{workflow_template}'
autoscaling_policy_path = f'projects/{project}/locations/{location}/autoscalingPolicies/{autoscaling_policy}'
```
