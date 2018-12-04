API Client Generator for Python
===============================

    A generator for protocol buffer described APIs for and in Python 3.

This program accepts an API specified in `protocol buffers`_ and generates
a client library, which can be used to interact with that API. It is
implemented as a plugin to ``protoc``, the protocol buffer compiler.

.. warning::

  This tool is a proof of concept and is being iterated on rapidly.
  Feedback is welcome, but please do not try to use this in some kind of
  system where stability is an expectation.

.. _protocol buffers: https://developers.google.com/protocol-buffers/

.. toctree::
  :maxdepth: 2

  getting-started/index
  api-configuration
  process
  templates
  status
  reference/index
