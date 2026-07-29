# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""BigQuery DataFrames ML provides a SKLearn-like API on the BigQuery engine.

.. code:: python

    from bigframes.ml.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(feature_columns, label_columns)
    model.predict(feature_columns_from_test_data)

You can also save your fit parameters to BigQuery for later use.

.. code:: python

    import bigframes.pandas as bpd
    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.penguins_model"
        replace=True,
    )
    saved_model = bpd.read_gbq_model(your_model_id)
    saved_model.predict(feature_columns_from_test_data)

See the `BigQuery ML linear regression tutorial
<https://docs.cloud.google.com/bigquery/docs/linear-regression-tutorial>`_ for a
detailed example.

See also the references for ``bigframes.ml`` sub-modules:

* :mod:`bigframes.ml.cluster`
* :mod:`bigframes.ml.compose`
* :mod:`bigframes.ml.decomposition`
* :mod:`bigframes.ml.ensemble`
* :mod:`bigframes.ml.forecasting`
* :mod:`bigframes.ml.imported`
* :mod:`bigframes.ml.impute`
* :mod:`bigframes.ml.linear_model`
* :mod:`bigframes.ml.llm`
* :mod:`bigframes.ml.metrics`
* :mod:`bigframes.ml.model_selection`
* :mod:`bigframes.ml.pipeline`
* :mod:`bigframes.ml.preprocessing`
* :mod:`bigframes.ml.remote`

Alternatively, check out mod:`bigframes.bigquery.ml` for an interface that is
more similar to the BigQuery ML SQL syntax.
"""

from bigframes.ml import (
    cluster,
    compose,
    decomposition,
    ensemble,
    forecasting,
    imported,
    impute,
    linear_model,
    llm,
    metrics,
    model_selection,
    pipeline,
    preprocessing,
    remote,
)

__all__ = [
    "cluster",
    "compose",
    "decomposition",
    "ensemble",
    "forecasting",
    "imported",
    "impute",
    "linear_model",
    "llm",
    "metrics",
    "model_selection",
    "pipeline",
    "preprocessing",
    "remote",
]
