Dialogflow: Python Client
=========================

|release level| |circleci| |codecov|

    Python idiomatic client for `Dialogflow`_

`Dialogflow`_ is an enterprise-grade NLU platform that makes it easy for
developers to design and integrate conversational user interfaces into
mobile apps, web applications, devices, and bots.

* `Dialogflow Python Client API Reference <http://dialogflow-python-client-v2.readthedocs.io/en/latest/>`_
* `Dialogflow Standard Edition Documentation <https://www.dialogflow.com>`_
* `Dialogflow Enterprise Edition Documentation <https://cloud.google.com/dialogflow-enterprise/docs>`_

Read more about the client libraries for Cloud APIs, including the older
Google APIs Client Libraries, in
`Client Libraries Explained <https://cloud.google.com/apis/docs/client-libraries-explained>`_.

.. _Dialogflow: https://dialogflow.com/


Before you begin
----------------

#. Select or create a Cloud Platform `project`_.
#. `Enable billing`_ for your project.
#.  `Enable the Google Cloud Dialogflow API`_.
#.  `Set up authentication`_ with a service account so you can access the
    API from your local workstation.

.. _project: https://console.cloud.google.com/project
.. _Enable billing: https://support.google.com/cloud/answer/6293499#enable-billing
.. _Enable the Google Cloud Dialogflow API: https://console.cloud.google.com/flows/enableapi?apiid=dialogflow.googleapis.com
.. _Set up authentication: https://cloud.google.com/docs/authentication/getting-started


Installation
------------

.. code-block:: shell

    pip install dialogflow

.. note::

    We highly recommend that you install this library in a
    `virtualenv <https://virtualenv.pypa.io/en/latest/>`_.


Usage
-----

View `usage documentation <http://dialogflow-python-client-v2.readthedocs.io/en/latest/?#using-dialogflow>`_ on Read the Docs.


Versioning
----------

This library follows `Semantic Versioning <http://semver.org/>`_.

This library is considered to be in **beta**. This means it is expected to be
mostly stable while we work toward a general availability release; however,
complete stability is not guaranteed. We will address issues and requests
against beta libraries with a high priority.

More Information: `Google Cloud Platform Launch Stages <https://cloud.google.com/terms/launch-stages>`_

Contributing
------------

Contributions welcome! See the `Contributing Guide <https://github.com/googleapis/python-dialogflow/blob/master/.github/CONTRIBUTING.rst>`_.

License
-------

Apache Version 2.0

See `the LICENSE file <https://github.com/googleapis/python-dialogflow/blob/master/LICENSE>`_ for more information.


.. |release level| image:: https://img.shields.io/badge/release%20level-beta-yellow.svg?style&#x3D;flat
    :target: https://cloud.google.com/terms/launch-stages
.. |circleci| image:: https://img.shields.io/circleci/project/github/dialogflow/dialogflow-python-client-v2.svg?style=flat)
    :target: https://circleci.com/gh/dialogflow/dialogflow-python-client-v2
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/dialogflow/dialogflow-python-client-v2?branch=master&svg=true)
    :target: https://ci.appveyor.com/project/dialogflow/dialogflow-python-client-v2
.. |codecov| image:: https://img.shields.io/codecov/c/github/dialogflow/dialogflow-python-client-v2/master.svg?style=flat)
    :target: https://codecov.io/gh/dialogflow/dialogflow-python-client-v2
