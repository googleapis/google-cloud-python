API Client Generator for Python
===============================

|release level| |pypi| |versions|

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

See the `documentation`_.

.. _documentation: https://googleapis.dev/python/gapic-generator-python/latest

.. |release level| image:: https://img.shields.io/badge/support-stable-gold.svg
  :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/gapic-generator.svg
  :target: https://pypi.org/project/gapic-generator/
.. |versions| image:: https://img.shields.io/pypi/pyversions/gapic-generator.svg
  :target: https://pypi.org/project/gapic-generator/
