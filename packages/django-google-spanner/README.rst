Cloud Spanner support for Django
================================

`Cloud Spanner`_ is the world's first fully managed relational database service
to offer both strong consistency and horizontal scalability for
mission-critical online transaction processing (OLTP) applications. With Cloud
Spanner you enjoy all the traditional benefits of a relational database; but
unlike any other relational database service, Cloud Spanner scales horizontally
to hundreds or thousands of servers to handle the biggest transactional
workloads.


- `Client Library Documentation`_
- `Product Documentation`_

.. _Cloud Spanner: https://cloud.google.com/spanner/
.. _Client Library Documentation: https://googleapis.dev/python/django-google-spanner/latest/index.html
.. _Product Documentation:  https://cloud.google.com/spanner/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Spanner API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Spanner API.:  https://cloud.google.com/spanner
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

This package provides a `3rd-party database backend
<https://docs.djangoproject.com/en/2.2/ref/databases/#using-a-3rd-party-database-backend>`__
for using `Cloud Spanner <https://cloud.google.com/spanner>`__ with the `Django
ORM <https://docs.djangoproject.com/en/2.2/topics/db/>`__. It uses the `Cloud
Spanner Python client library <https://github.com/googleapis/python-spanner>`__
under the hood.

Installation
------------

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python and Django environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Mac/Linux
~~~~~~~~~

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install python-spanner-django
    <your-env>/bin/pip install google-cloud-spanner


Windows
~~~~~~~

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install python-spanner-django
    <your-env>\Scripts\pip.exe install google-cloud-spanner


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


Set credentials and project environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You'll need to download a service account JSON key file and point to it using an environment variable:

.. code:: shell

    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/keyfile.json
    export GOOGLE_CLOUD_PROJECT=gcloud_project


Apply the migrations
~~~~~~~~~~~~~~~~~~~~

Please run:

.. code:: shell

    $ python3 manage.py migrate

and that'll take a while to run. After this you should be able to see the tables and indices created in your Cloud Spanner console.

Now run your server
~~~~~~~~~~~~~~~~~~~
After those migrations are completed, that will be all. Please continue on with the guides.

Create an Django admin user
~~~~~~~~~~~~~~~~~~~~~~~~~~~
First you’ll need to create a user who can login to the admin site. Run the following command:

.. code:: shell

    $ python3 manage.py createsuperuser

which will then produce a prompt which will allow you to create your super user

.. code:: shell

    Username: admin
    Email address: admin@example.com
    Password: **********
    Password (again): **********
    Superuser created successfully.


Login as admin
~~~~~~~~~~~~~~
Let’s run the server

.. code:: shell

    python3 manage.py runserver

Then visit http://127.0.0.1:8000/admin/

Create and register your first model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please follow the guides in https://docs.djangoproject.com/en/2.2/intro/tutorial02/#creating-models
to create and register the model to the Django’s automatically-generated admin site.

How it works
------------

Overall design
~~~~~~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/googleapis/python-spanner-django/master/assets/overview.png
   :alt: "Overall Design"

Internals
~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/googleapis/python-spanner-django/master/assets/internals.png
   :alt: "Internals"


Executing a query
~~~~~~~~~~~~~~~~~

Here is an example of how to add a row for Model Author, save it and later query it using Django

.. code:: shell

    >>> author_kent = Author( first_name="Arthur", last_name="Kent", rating=Decimal("4.1"),)
    >>> author_kent.save()
    >>> qs1 = Author.objects.all().values("first_name", "last_name")


HOW TO CONTRIBUTE
-----------------

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING <https://github.com/googleapis/python-spanner-django/blob/master/CONTRIBUTING.md>`_ for more information on how to get started.

Please note that this project is released with a Contributor Code of Conduct.
By participating in this project you agree to abide by its terms. See the `Code 
of Conduct <https://github.com/googleapis/python-spanner-django/blob/master/CODE_OF_CONDUCT.md>`_ for more information.

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

``Unsigned`` datatypes are not supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spanner does not support ``Unsigned`` datatypes so `PositiveIntegerField
<https://docs.djangoproject.com/en/stable/ref/models/fields/#positiveintegerfield>`__
and `PositiveSmallIntegerField
<https://docs.djangoproject.com/en/3.2/ref/models/fields/#positivesmallintegerfield>`__
are both stored as `Integer type
<https://cloud.google.com/spanner/docs/data-types#integer_type>`__
.

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
