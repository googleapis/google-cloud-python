# Copyright 2025 Google LLC
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

"""This module integrates BigQuery built-in 'ObjectRef' functions for use with Series/DataFrame objects,
such as OBJ.FETCH_METADATA:
https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions


.. warning::

    This product or feature is subject to the "Pre-GA Offerings Terms" in the
    General Service Terms section of the `Service Specific Terms
    <https://cloud.google.com/terms/service-terms>`_. Pre-GA products and
    features are available "as is" and might have limited support. For more
    information, see the `launch stage descriptions
    <https://cloud.google.com/products?hl=en#product-launch-stages>`_.

.. note::

    To provide feedback or request support for this feature, send an email to
    bq-objectref-feedback@google.com.
"""

from bigframes.bigquery._operations.obj import fetch_metadata, get_access_url, make_ref

__all__ = [
    "fetch_metadata",
    "get_access_url",
    "make_ref",
]
