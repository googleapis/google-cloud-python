Using the Vision API
====================

Authentication and Configuration
--------------------------------

- For an overview of authentication in ``gcloud-python``,
  see :doc:`gcloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GCLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If the GCLOUD_PROJECT environment variable is not present,
  the project ID from JSON file credentials is used.

  If you are using Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`Client <gcloud.vision.client.Client>`

.. code-block:: python

     >>> from gcloud import vision
     >>> client = vision.Client()

or pass in ``credentials`` and ``project`` explicitly

.. code-block:: python

     >>> from gcloud import vision
     >>> client = vision.Client(project='my-project', credentials=creds)

Annotating an Image
-------------------

Annotate a single image
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.png')
    >>> faces = image.detect_faces(limit=10)

Annotate multiple images
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

     >>> first_image = client.image('./image.jpg')
     >>> second_image = client.image('gs://my-storage-bucket/image2.jpg')
     >>> with client.batch():
     ...     labels = first_image.detect_labels()
     ...     faces = second_image.detect_faces(limit=10)

or

.. code-block:: python

     >>> images = []
     >>> images.append(client.image('./image.jpg'))
     >>> images.append(client.image('gs://my-storage-bucket/image2.jpg'))
     >>> faces = client.detect_faces_multi(images, limit=10)

No results returned
~~~~~~~~~~~~~~~~~~~

Failing annotations return no results for the feature type requested.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> logos = image.detect_logos(limit=10)
    >>> logos
    []


Manual Detection
~~~~~~~~~~~~~~~~

You can call the detection method manually.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('gs://my-test-bucket/image.jpg')
    >>> faces = image.detect(type=vision.FACE_DETECTION, limit=10)

Face Detection
~~~~~~~~~~~~~~

Detecting a face or faces in an image.
For a list of the possible facial landmarks
see: https://cloud.google.com/vision/reference/rest/v1/images/annotate#type_1


.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> faces = image.detect_faces(limit=10)
    >>> faces[0].landmarks[0].type
    'LEFT_EYE'
    >>> faces[0].landmarks[0].position.x
    1301.2404
    >>> faces[0].detection_confidence
    0.9863683
    >>> faces[0].joy_likelihood
    0.54453093
    >>> faces[0].anger_likelihood
    0.02545464



Label Detection
~~~~~~~~~~~~~~~

Image labels are a way to help categorize the contents of an image.
If you have an image with a car, person and a dog it, label detection will
attempt to identify those objects.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> labels = image.detect_labels(limit=3)
    >>> labels[0].description
    'automobile'
    >>> labels[0].score
    0.9863683


Landmark Detection
~~~~~~~~~~~~~~~~~~

The API will attemtp to detect landmarks such as Mount Rushmore and
the Sydney Opera House. The API will also provide their known geographical
locations if available.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> landmarks = image.detect_landmarks()
    >>> landmarks[0].description
    'Sydney Opera House'
    >>> landmarks[0].locations[0].latitude
    -33.857123
    >>> landmarks[0].locations[0].longitude
    151.213921
    >>> landmarks[0].bounding_poly.vertices[0].x
    78
    >>> landmarks[0].bounding_poly.vertices[0].y
    162

Logo Detection
~~~~~~~~~~~~~~

Google Vision can also attempt to detect company and brand logos in images.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> logos = image.detect_logos(limit=1)
    >>> results.logos[0].description
    'Google'
    >>> logos[0].score
    0.9795432
    >>> logos[0].bounding_poly.vertices[0].x
    78
    >>> logos[0].bounding_poly.vertices[0].y
    62

Safe Search Detection
~~~~~~~~~~~~~~~~~~~~~

Detecting safe search properties of an image.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> safe_search = image.detect_safe_search()
    >>> safe_search.adult
    'VERY_UNLIKELY'
    >>> safe_search.medical
    'UNLIKELY'

Text Detection
~~~~~~~~~~~~~~

Detecting text with ORC from an image.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> text = image.detect_text()
    >>> text.locale
    'en'
    >>> text.description
    'the full text of the image.'

Image Properties
~~~~~~~~~~~~~~~~

Detecting image color properties.

.. code-block:: python

    >>> from gcloud import vision
    >>> client = vision.Client()
    >>> image = client.image('./image.jpg')
    >>> colors = image.detect_properties()
    >>> colors[0].red
    244
    >>> colors[0].blue
    134
    >>> colors[0].score
    0.65519291
    >>> colors[0].pixel_fraction
    0.758658
