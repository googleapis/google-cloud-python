######
Vision
######

.. toctree::
  :maxdepth: 2
  :hidden:

  annotations
  batch
  client
  color
  crop-hint
  entity
  feature
  face
  image
  safe-search
  text
  web

********************************
Authentication and Configuration
********************************

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`/core/auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd
  like to interact with. If the GOOGLE_CLOUD_PROJECT environment variable is
  not present, the project ID from JSON file credentials is used.

  If you are using Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`~google.cloud.vision.client.Client`.

.. code-block:: python

     >>> from google.cloud import vision
     >>> client = vision.ImageAnnotatorClient()

or pass in ``credentials`` and ``project`` explicitly.

.. code-block:: python

     >>> from google.cloud import vision
     >>> client = vision.Client(project='my-project', credentials=creds)


*****************
Annotate an Image
*****************



****************
Manual Detection
****************

You can call the detection method manually.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.ImageAnnotatorClient()
    >>> response = client.annotate_image({
    ...   'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
    ...   'features': [{'type': vision.enums.Feature.Type.FACE_DETECTOIN}],
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


************************
Single-feature Shortcuts
************************

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
    >>> for face in resposne.annotations[0].faces:
    ...     print(face.joy)
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY
    Likelihood.VERY_LIKELY


****************
No results found
****************

If no results for the detection performed can be extracted from the image, then
an empty list is returned. This behavior is similiar with all detection types.


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
