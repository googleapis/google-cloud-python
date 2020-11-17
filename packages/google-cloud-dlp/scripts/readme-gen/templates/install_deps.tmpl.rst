Install Dependencies
++++++++++++++++++++

#. Clone python-dlp and change directory to the sample directory you want to use.

    .. code-block:: bash

        $ git clone https://github.com/googleapis/python-dlp.git
        $ cd samples/snippets

#. Install `pip`_ and `virtualenv`_ if you do not already have them. You may want to refer to the `Python Development Environment Setup Guide`_ for Google Cloud Platform for instructions.

   .. _Python Development Environment Setup Guide:
       https://cloud.google.com/python/setup

#. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.

    .. code-block:: bash

        $ virtualenv env
        $ source env/bin/activate

#. Install the dependencies needed to run the samples.

    .. code-block:: bash

        $ pip install -r requirements.txt

.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
