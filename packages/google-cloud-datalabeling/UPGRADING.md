# 1.0.0 Migration Guide

The 1.0 release of the `google-cloud-datalabeling` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-datalabeling/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library

```py
python3 -m pip install google-cloud-datalabeling[libcst]
```

* The script `fixup_datalabeling_v1_keywords.py` is shipped with the library. It expects an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_datalabeling_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import datalabeling

client = datalabeling.DataLabelingServiceClient()

datasets = client.list_datasets(parent="projects/project")
```


**After:**
```py
from google.cloud import datalabeling

client = datalabeling.DataLabelingServiceClient()

datasets = client.list_datasets(request={"parent": "projects/project"})
```

### More Details

In `google-cloud-datalabeling<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_dataset(
        self,
        parent,
        dataset,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/master/google/cloud/datalabeling/v1beta1/data_labeling_service.proto#L48) specified by the API producer.


**After:**
```py
    def create_dataset(
        self,
        request: data_labeling_service.CreateDatasetRequest = None,
        *,
        parent: str = None,
        dataset: gcd_dataset.Dataset = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_dataset.Dataset:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.create_dataset(
    request={
        "parent": parent,
        "dataset": dataset
    }
)
```

```py
response = client.create_dataset(
    parent=parent,
    dataset=dataset
)
```

This call is invalid because it mixes `request` with a keyword argument `dataset`. Executing this code
will result in an error.

```py
response = client.create_dataset(
    request={
        "parent": parent
    },
    dataset=dataset
)
```



## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py
from google.cloud import datalabeling

data_type = datalabeling.enums.DataType.IMAGE
dataset = datalabeling.types.Dataset(display_name="name")
```


**After:**
```py
from google.cloud import datalabeling

data_type = datalabeling.DataType.IMAGE
dataset = datalabeling.Dataset(display_name="name")
```

## Path Helper Methods
The following path helper methods have been removed. Please construct the paths manually.

```py
project="project"
dataset="dataset"
annotated_dataset="annotated_dataset"
annotation_spec_set="annotation_spec_set"
data_item="data_item"
evaluation="evaluation"
evaluation_job="evaluation_job"
example="example"
instruction="instruction"

annotated_dataset_path = f'projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}'
annotation_spec_set_path = f'projects/{project}/annotationSpecSets/{annotation_spec_set}'
data_item_path=f'projects/{project}/datasets/{dataset}/dataItems/{data_item}'
dataset_path=f'projects/{project}/datasets/{dataset}'
evaluation_path=f'projects/{project}/datasets/{dataset}/evaluations/{evaluation}'
evaluation_job_path=f'projects/{project}/evaluationJobs/{evaluation_job}'
example_path=f'projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}/examples/{example}'
instruction_path=f'projects/{project}/instructions/{instruction}'
project_path=f'projects/{project}'
```
