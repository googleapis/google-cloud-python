.. include:: README.rst

.. include:: multiprocessing.rst

This package includes clients for multiple versions of the Text-to-Speech
API. By default, you will get ``v1``, the latest GA version.

v1 API Reference
----------------
.. toctree::
    :maxdepth: 2

    Client (v1) <texttospeech_v1/services>
    Types (v1) <texttospeech_v1/types>


If you are interested in beta features ahead of the latest GA, you may
opt-in to the v1.1 beta, which is spelled ``v1beta1``. In order to do this,
you will want to import from ``google.cloud.texttospeech_v1beta1`` in lieu of
``google.cloud.texttospeech``.

v1beta1 API Reference
---------------------
.. toctree::
    :maxdepth: 2
    
    Client (v1beta1) <texttospeech_v1beta1/services>
    Types (v1beta1) <texttospeech_v1beta1/types>


Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING


Changelog
---------

For a list of all ``google-cloud-texttospeech`` releases.

.. toctree::
    :maxdepth: 2

    changelog
