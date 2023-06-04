# 1.0.0 Migration Guide

The 1.0 release of the `google-cloud-billing-budgets` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-billingbudgets/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 1.0.0 release requires Python 3.6+.


## Namespace Change

> **WARNING**: Breaking change

The 1.0.0 release changes namespace from `google.cloud.billing_budgets` to `google.cloud.billing.budgets`.

**Before:**
```py
from google.cloud import billing_budgets

client = billing_budgets.BudgetServiceClient()
```


**After:**
```py
from google.cloud.billing import budgets

client = budgets.BudgetServiceClient()
```


## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library with `libcst`.

```py
python3 -m pip install google-cloud-billing-budgets[libcst]
```

* The script `fixup_budgets_v1beta1_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_budgets_v1beta1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
budget = client.get_budget(name="billingAccounts/account/budgets/budget")
```


**After:**
```py
budget = client.get_budget(request = {'name': "billingAccounts/account/budgets/budget"})
```

### More Details

In `google-cloud-billing-budgets<1.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def create_budget(
        self,
        parent,
        budget,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 1.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.


**After:**
```py
    def create_budget(
          self,
          request: budget_service.CreateBudgetRequest = None,
          *,
          retry: retries.Retry = gapic_v1.method.DEFAULT,
          timeout: float = None,
          metadata: Sequence[Tuple[str, str]] = (),
      ) -> budget_model.Budget:
```


## Enums and Types


> **WARNING**: Breaking change

The submodules `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import billing_budgets

filter = billing_budgets.enums.Filter.CreditTypesTreatment.INCLUDE_ALL_CREDITS
budget = billing_budgets.types.Budget()
```


**After:**
```py
from google.cloud.billing import budgets

filter = budgets.Filter.CreditTypesTreatment.INCLUDE_ALL_CREDITS
budget = budgets.Budget()
```
