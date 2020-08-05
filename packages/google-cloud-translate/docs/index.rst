.. include:: README.rst

.. include:: multiprocessing.rst

API Reference
-------------

An API and type reference is provided for ``v3``, ``v3beta1``, and ``v2``.

By default, you will get ``v3``. A beta release, spelled ``v3beta1`` is
provided for preview of upcoming features. In order to use this, you will
want to import from ``google.cloud.translate_v3beta1`` in lieu of
``google.cloud.translate``. The previous release ``v2`` is also available.
Import from ``google.cloud.translate_v2`` to use this release.

v3 API Reference
----------------
.. toctree::
   :maxdepth: 2
   
   Client (v3) <translate_v3/services>
   Types (v3) <translate_v3/types>

v3beta1 API Reference
---------------------
.. toctree::
   :maxdepth: 2

   Client (v3beta1) <translate_v3beta1/services>
   Types (v3beta1) <translate_v3beta1/types>

v2 API Reference
----------------
.. toctree::
   :maxdepth: 2

   v2


Migration Guide
---------------

See the guide below for instructions on migrating to the 3.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING


Changelog
---------

For a list of all ``google-cloud-translate`` releases:

.. toctree::
  :maxdepth: 2

  changelog

