.. include:: README.rst

.. include:: multiprocessing.rst

Api Reference
-------------

This package includes clients for multiple versions of the Cloud Asset API. By default, you will get ``v1``
the latest stable version.

v1
~~~~~~~~~
.. toctree::
    :maxdepth: 2

    gapic/v1/api
    gapic/v1/types

Beta releases with additional features over the current stable version. These are expected to move into the stable release soon;
until then, the usual beta admonishment (changes are possible, etc.) applies.

In order to use it, you will want to import from 
``google.cloud.asset_v1p4beta1`` in lieu of ``google.cloud.asset_v1``.

v1p1beta1
~~~~~~~~~
.. toctree::
    :maxdepth: 2

    gapic/v1p1beta1/api
    gapic/v1p1beta1/types


v1p2beta1
~~~~~~~~~
.. toctree::
    :maxdepth: 2

    gapic/v1p2beta1/api
    gapic/v1p2beta1/types


v1p4beta1
~~~~~~~~~
.. toctree::
    :maxdepth: 2

    gapic/v1p4beta1/api
    gapic/v1p4beta1/types



v1beta1
~~~~~~~~~
.. toctree::
    :maxdepth: 2

    gapic/v1beta1/api
    gapic/v1beta1/types


Changelog
---------

For a list of all ``google-cloud-asset`` releases:

.. toctree::
  :maxdepth: 2

  changelog
