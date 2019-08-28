.. include:: README.rst

Api Reference
-------------

This package includes clients for multiple versions of the Cloud Asset API. By default, you will get ``v1``
the latest stable version.

.. toctree::
    :maxdepth: 2

    gapic/v1/api
    gapic/v1/types

A new beta release with additional features over the current stable version, spelled ``v1p2beta1``, is provided
to allow you to use these new features. These are expected to move into the stable release soon; until
then, the usual beta admonishment (changes are possible, etc.) applies.

An API and type reference is provided for this beta:

.. toctree::
    :maxdepth: 2

    gapic/v1p2beta1/api
    gapic/v1p2beta1/types

The previous beta release, spelled ``v1p2beta1`` is also provided to continue to support code
previously written against it. In order to use it, you will want to import from 
``google.cloud.asset_v1beta1`` in lieu of ``google.cloud.asset_v1``.

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
