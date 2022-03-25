.. include:: README.rst

.. include:: multiprocessing.rst


Using the Library
-----------------

Annotate an Image
~~~~~~~~~~~~~~~~~

You can call the :meth:`annotate_image` method directly:

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.ImageAnnotatorClient()
    >>> response = client.annotate_image({
    ...   'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
    ...   'features': [{'type_': vision.Feature.Type.FACE_DETECTION}],
    ... })
    >>> len(response.annotations)
    2
    >>> for face in response.annotations[0].faces:
    ...     print(face.joy)
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY
    >>> for logo in response.annotations[0].logos:
    ...     print(logo.description)
    'google'
    'github'


Single-feature Shortcuts
~~~~~~~~~~~~~~~~~~~~~~~~

If you are only requesting a single feature, you may find it easier to ask
for it using our direct methods:

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.ImageAnnotatorClient()
    >>> response = client.face_detection({
    ...   'source': {'image_uri': 'gs://my-test-bucket/image.jpg'},
    ... })
    >>> len(response.annotations)
    1
    >>> for face in response.annotations[0].faces:
    ...     print(face.joy)
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY


No results found
~~~~~~~~~~~~~~~~

If no results for the detection performed can be extracted from the image, then
an empty list is returned. This behavior is similar with all detection types.


Example with :meth:`~google.cloud.vision.ImageAnnotatorClient.logo_detection`:

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.ImageAnnotatorClient()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     content = image_file.read()
    >>> response = client.logo_detection({
    ...     'content': content,
    ... })
    >>> len(response.annotations)
    0

API Reference
-------------

This package includes clients for multiple versions of the Vision
API. By default, you will get ``v1``, the latest stable version.

.. toctree::
    :maxdepth: 2

    vision_v1/services
    vision_v1/types


A new beta release with additional features over the current stable version,
spelled ``v1p4beta1``, is provided to allow you to use these new features.
These are expected to move into the stable release soon; until then, the
usual beta admonishment (changes are possible, etc.) applies.

.. toctree::
    :maxdepth: 2

    vision_v1p4beta1/services
    vision_v1p4beta1/types

Previous beta releases ``v1p3beta1`` and ``v1p2beta1`` are provided as well.

An API and type reference is provided for ``v1p3beta1``:

.. toctree::
    :maxdepth: 2

    vision_v1p3beta1/services
    vision_v1p3beta1/types


An API and type reference is provided for ``v1p2beta1``:

.. toctree::
    :maxdepth: 2

    vision_v1p2beta1/services
    vision_v1p2beta1/types

Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING

Changelog
---------

For a list of all ``google-cloud-vision`` releases:

.. toctree::
  :maxdepth: 2

  changelog
