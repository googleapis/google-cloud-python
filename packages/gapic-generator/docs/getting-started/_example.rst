If you want to experiment with an already-existing API, one example is
available. (Reminder that this is still considered experimental, so apologies
for this part being a bit strange.)

You need to clone the `googleapis`_ repository from GitHub, and change to
a special branch:

.. code-block:: shell

  $ git clone git@github.com:googleapis/googleapis.git
  $ cd googleapis
  $ git checkout --track -b input-contract origin/input-contract
  $ cd ..

The API available as an example (thus far) is the `Google Cloud Vision`_ API,
available in the ``google/cloud/vision/v1/`` subdirectory. This will be used
for the remainder of the examples on this page.

.. _googleapis: https://github.com/googleapis/googleapis/tree/input-contract
.. _Google Cloud Vision: https://cloud.google.com/vision/
