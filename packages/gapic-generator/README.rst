API Client Generator for Python
===============================

|release level| |ci| |docs| |codecov|

    A generator for protocol buffer described APIs for and in Python 3.

This is a generator for API client libraries for APIs
specified by `protocol buffers`_, such as those inside Google.
It takes a protocol buffer (with particular annotations) and uses it
to generate a client library.

.. _protocol buffers: https://developers.google.com/protocol-buffers/

Purpose
-------

This library primarily exists to facilitate experimentation, particularly
regarding:

- An explicit normalized format for specifying APIs.
- Light weight, in-language code generators.

Documentation
-------------

`Documentation`_ is available on Read the Docs.

.. _documentation: https://gapic-generator-python.readthedocs.io/

.. |release level| image:: https://img.shields.io/badge/release%20level-beta-yellow.svg?style&#x3D;flat
  :target: https://cloud.google.com/terms/launch-stages
.. |docs| image:: https://readthedocs.org/projects/gapic-generator-python/badge/?version=latest
  :target: https://gapic-generator-python.readthedocs.io/
.. |ci| image:: https://circleci.com/gh/googleapis/gapic-generator-python.svg?style=shield
  :target: https://circleci.com/gh/googleapis/gapic-generator-python
.. |codecov| image:: https://codecov.io/gh/googleapis/gapic-generator-python/graph/badge.svg
  :target: https://codecov.io/gh/googleapis/gapic-generator-python
