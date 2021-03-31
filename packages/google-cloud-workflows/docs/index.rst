.. include:: README.rst

.. include:: multiprocessing.rst

This package includes clients for multiple versions of the Workflows API By default, you will get ``v1``, the latest version.

v1
---
.. toctree::
    :maxdepth: 2

    workflows_v1/services
    executions_v1/services
    workflows_v1/types
    executions_v1/types

The previous beta release, spelled ``v1beta`` is provided to continue to support code previously written against it. In order to use it, you will want to import from it e.g., ``google.cloud.workflows_v1`` in lieu of ``google.cloud.workflows`` (or the equivalent ``google.cloud.workflows_v1``).

v1beta
-------------
.. toctree::
    :maxdepth: 2

    workflows_v1beta/services
    executions_v1beta/services
    workflows_v1beta/types
    executions_v1beta/types

Changelog
---------

For a list of all ``google-cloud-workflows`` releases:

.. toctree::
   :maxdepth: 2

   changelog
