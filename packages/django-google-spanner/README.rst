Cloud Spanner support for Django
================================

This package provides a `3rd-party database backend
<https://docs.djangoproject.com/en/2.2/ref/databases/#using-a-3rd-party-database-backend>`__
for using `Cloud Spanner <https://cloud.google.com/spanner>`__ with the `Django
ORM <https://docs.djangoproject.com/en/2.2/topics/db/>`__. It uses the `Cloud
Spanner Python client library <https://github.com/googleapis/python-spanner>`__
under the hood.

Installation
------------

To use this library, you'll need a Google Cloud Platform project with the Cloud
Spanner API enabled. For details on enabling the API and authenticating with
GCP, see the `Cloud Spanner Python client library quickstart guide
<https://github.com/googleapis/python-spanner/#quick-start>`__.

Supported versions
~~~~~~~~~~~~~~~~~~

At the moment, this library only supports `Django 2.2
<https://docs.djangoproject.com/en/2.2/>`__. It also requires Python version
3.6 or later.

This package follows a common versioning convention for Django plugins: the
major and minor version components of this package should match the installed
version of Django. That is, ``django-google-spanner~=2.2`` works with
``Django~=2.2``.

Installing the package
~~~~~~~~~~~~~~~~~~~~~~

To install from PyPI:

.. code:: shell

    pip3 install django-google-spanner


To install from source:

.. code:: shell

    git clone git@github.com:googleapis/python-spanner-django.git
    cd python-spanner-django
    pip3 install -e .


Creating a Cloud Spanner instance and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't already have a Cloud Spanner database, or want to start from
scratch for a new Django application, you can `create a new instance
<https://cloud.google.com/spanner/docs/getting-started/python#create_an_instance>`__
and `database
<https://cloud.google.com/spanner/docs/getting-started/python#create_a_database>`__
using the Google Cloud SDK:

.. code:: shell

    gcloud spanner instances create $INSTANCE --config=regional-us-central1 --description="New Django Instance" --nodes=1
    gcloud spanner databases create $DB --instance $INSTANCE


Configuring ``settings.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package provides a Django application named ``django_spanner``. To use the
Cloud Spanner database backend, the application needs to installed and
configured:

-  Add ``django_spanner`` as the first entry in ``INSTALLED_APPS``:

   .. code:: python

       INSTALLED_APPS = [
           'django_spanner',
           ...
       ]

-  Edit the ``DATABASES`` setting to point to an existing Cloud Spanner database:

   .. code:: python

       DATABASES = {
           'default': {
               'ENGINE': 'django_spanner',
               'PROJECT': '$PROJECT',
               'INSTANCE': '$INSTANCE',
               'NAME': '$DATABASE',
           }
       }


How it works
------------

Overall design
~~~~~~~~~~~~~~

.. figure:: ./assets/overview.png
   :alt:

Internals
~~~~~~~~~

.. figure:: ./assets/internals.png
   :alt:



Executing a query
~~~~~~~~~~~~~~~~~

.. code:: python

    from google.cloud.spanner_dbapi import connect

    connection = connect('<instance_id>', '<database_id>')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT *"
        "FROM Singers"
        "WHERE SingerId = 15"
    )

    results = cursor.fetchall()


Contributing
------------

Contributions to this library are always welcome and highly encouraged.

See [CONTRIBUTING][contributing] for more information on how to get started.

Please note that this project is released with a Contributor Code of Conduct.
By participating in this project you agree to abide by its terms. See the `Code
of Conduct <code-of-conduct.md>`_ for more information.

Current limitations
-------------------

``AutoField`` generates random IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner doesn't have support for auto-generating primary key values.
Therefore, ``django-google-spanner`` monkey-patches ``AutoField`` to generate a
random UUID4. It generates a default using ``Field``'s ``default`` option which
means ``AutoField``\ s will have a value when a model instance is created. For
example:

::

    >>> ExampleModel()
    >>> ExampleModel.pk
    4229421414948291880

To avoid
`hotspotting <https://cloud.google.com/spanner/docs/schema-design#uuid_primary_key>`__,
these IDs are not monotonically increasing. This means that sorting
models by ID isn't guaranteed to return them in the order in which they
were created.

``ForeignKey`` constraints aren't created (`#313 <https://github.com/googleapis/python-spanner-django/issues/313>`__)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner does not support ``ON DELETE CASCADE`` when creating foreign-key
constraints, so this is not supported in ``django-google-spanner``.

Check constraints aren't supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner does not support ``CHECK`` constraints so one isn't created for
`PositiveIntegerField
<https://docs.djangoproject.com/en/stable/ref/models/fields/#positiveintegerfield>`__
and `CheckConstraint
<https://docs.djangoproject.com/en/stable/ref/models/constraints/#checkconstraint>`__
can't be used.

No native support for ``DecimalField``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner's support for `Decimal <https://www.python.org/dev/peps/pep-0327/>`__
types is limited to
`NUMERIC <https://cloud.google.com/spanner/docs/data-types#numeric_types>`__
precision. Higher-precision values can be stored as strings instead.

``Meta.order_with_respect_to`` model option isn't supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This feature uses a column name that starts with an underscore
(``_order``) which Spanner doesn't allow.

Random ``QuerySet`` ordering isn't supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner does not support it and will throw an exception. For example:

::

    >>> ExampleModel.objects.order_by('?')
    ...
    django.db.utils.ProgrammingError: 400 Function not found: RANDOM ... FROM
    example_model ORDER BY RANDOM() ASC

Schema migrations
~~~~~~~~~~~~~~~~~

There are some limitations on schema changes to consider:

-  No support for renaming tables and columns;
-  A column's type can't be changed;
-  A table's primary key can't be altered.

``DurationField`` arithmetic doesn't work with ``DateField`` values (`#253 <https://github.com/googleapis/python-spanner-django/issues/253>`__)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner requires using different functions for arithmetic depending on
the column type:

-  ``TIMESTAMP`` columns (``DateTimeField``) require ``TIMESTAMP_ADD``
   or ``TIMESTAMP_SUB``
-  ``DATE`` columns (``DateField``) require ``DATE_ADD`` or ``DATE_SUB``

Django does not provide ways to determine which database function to
use. ``DatabaseOperations.combine_duration_expression()`` arbitrarily uses
``TIMESTAMP_ADD`` and ``TIMESTAMP_SUB``. Therefore, if you use a
``DateField`` in a ``DurationField`` expression, you'll likely see an error
such as:

::

    "No matching signature for function TIMESTAMP\_ADD for argument types:
    DATE, INTERVAL INT64 DATE\_TIME\_PART."

Computations that yield FLOAT64 values cannot be assigned to INT64 columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner does not support this (`#331
<https://github.com/googleapis/python-spanner-django/issues/331>`__) and will
throw an error:

::

    >>> ExampleModel.objects.update(integer=F('integer') / 2)
    ...
    django.db.utils.ProgrammingError: 400 Value of type FLOAT64 cannot be
    assigned to integer, which has type INT64 [at 1:46]\nUPDATE
    example_model SET integer = (example_model.integer /...

Addition with null values crash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Additions cannot include ``None`` values. For example:

::

    >>> Book.objects.annotate(adjusted_rating=F('rating') + None)
    ...
    google.api_core.exceptions.InvalidArgument: 400 Operands of + cannot be literal
    NULL ...
