Python Client for Google Cloud Vision
=====================================

|GA| |pypi| |versions| 

The `Google Cloud Vision`_  API enables developers to
understand the content of an image by encapsulating powerful machine
learning models in an easy to use REST API. It quickly classifies images
into thousands of categories (e.g., "sailboat", "lion", "Eiffel Tower"),
detects individual objects and faces within images, and finds and reads
printed words contained within images. You can build metadata on your
image catalog, moderate offensive content, or enable new marketing
scenarios through image sentiment analysis. Analyze images uploaded
in the request or integrate with your image storage on Google Cloud
Storage.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-vision.svg
   :target: https://pypi.org/project/google-cloud-vision/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-vision.svg
   :target: https://pypi.org/project/google-cloud-vision/
.. _Vision: https://cloud.google.com/vision/

.. _Google Cloud Vision: https://cloud.google.com/vision/
.. _Client Library Documentation: https://googleapis.dev/python/vision/latest
.. _Product Documentation: https://cloud.google.com/vision/reference/rest/


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Vision API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Vision API.:  https://cloud.google.com/vision
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-vision==1.0.0.

RaspberryPi ARM devices 
^^^^^^^^^^^^^^^^^^^^^^^
Note: Raspberry Pi ARMv6 is not supported because there is an internal binary google that does not comply with armv6 processors.

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-vision


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-vision


Example Usage
~~~~~~~~~~~~~

.. code-block:: python

   from google.cloud import vision

   client = vision.ImageAnnotatorClient()
   response = client.annotate_image({
     'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
     'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
   })

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Vision API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
