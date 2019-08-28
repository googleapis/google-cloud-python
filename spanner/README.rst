Python Client for Cloud Spanner
===============================

|GA| |pypi| |versions| 

`Cloud Spanner`_ is the world's first fully managed relational database service
to offer both strong consistency and horizontal scalability for
mission-critical online transaction processing (OLTP) applications. With Cloud
Spanner you enjoy all the traditional benefits of a relational database; but
unlike any other relational database service, Cloud Spanner scales horizontally
to hundreds or thousands of servers to handle the biggest transactional
workloads.


- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
   :target: https://pypi.org/project/google-cloud-spanner/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-spanner.svg
   :target: https://pypi.org/project/google-cloud-spanner/
.. _Cloud Spanner: https://cloud.google.com/spanner/
.. _Client Library Documentation: https://googleapis.dev/python/spanner/latest
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
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-spanner


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-spanner


Example Usage
-------------


Executing Arbitrary SQL in a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generally, to work with Cloud Spanner, you will want a transaction. The
preferred mechanism for this is to create a single function, which executes
as a callback to ``database.run_in_transaction``:

.. code:: python

    # First, define the function that represents a single "unit of work"
    # that should be run within the transaction.
    def update_anniversary(transaction, person_id, unix_timestamp):
        # The query itself is just a string.
        #
        # The use of @parameters is recommended rather than doing your
        # own string interpolation; this provides protections against
        # SQL injection attacks.
        query = """SELECT anniversary FROM people
            WHERE id = @person_id"""

        # When executing the SQL statement, the query and parameters are sent
        # as separate arguments. When using parameters, you must specify
        # both the parameters themselves and their types.
        row = transaction.execute_sql(
            query=query,
            params={'person_id': person_id},
            param_types={
                'person_id': types.INT64_PARAM_TYPE,
            },
        ).one()

        # Now perform an update on the data.
        old_anniversary = row[0]
        new_anniversary = _compute_anniversary(old_anniversary, years)
        transaction.update(
            'people',
            ['person_id', 'anniversary'],
            [person_id, new_anniversary],
        )

    # Actually run the `update_anniversary` function in a transaction.
    database.run_in_transaction(update_anniversary,
        person_id=42,
        unix_timestamp=1335020400,
    )


Select records using a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have a transaction object (such as the first argument sent to
``run_in_transaction``), reading data is easy:

.. code:: python

    # Define a SELECT query.
    query = """SELECT e.first_name, e.last_name, p.telephone
        FROM employees as e, phones as p
        WHERE p.employee_id == e.employee_id"""

    # Execute the query and return results.
    result = transaction.execute_sql(query)
    for row in result.rows:
        print(row)


Insert records using Data Manipulation Language (DML) with a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``execute_update()`` method to execute a DML statement:

.. code:: python

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    def insert_singers(transaction):
        row_ct = transaction.execute_update(
            "INSERT Singers (SingerId, FirstName, LastName) "
            " VALUES (10, 'Virginia', 'Watson')"
        )

        print("{} record(s) inserted.".format(row_ct))

    database.run_in_transaction(insert_singers)


Insert records using Mutations with a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add one or more records to a table, use ``insert``:

.. code:: python

    transaction.insert(
        'citizens',
        columns=['email', 'first_name', 'last_name', 'age'],
        values=[
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ],
    )


Update records using Data Manipulation Language (DML) with a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    def update_albums(transaction):
        row_ct = transaction.execute_update(
            "UPDATE Albums "
            "SET MarketingBudget = MarketingBudget * 2 "
            "WHERE SingerId = 1 and AlbumId = 1"
        )

        print("{} record(s) updated.".format(row_ct))

    database.run_in_transaction(update_albums)


Update records using Mutations with a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Transaction.update`` updates one or more existing records in a table.  Fails
if any of the records does not already exist.

.. code:: python

    transaction.update(
        'citizens',
        columns=['email', 'age'],
        values=[
            ['phred@exammple.com', 33],
            ['bharney@example.com', 32],
        ],
    )


Next Steps
~~~~~~~~~~

- See the `Client Library Documentation`_ to learn how to connect to Cloud
  Spanner using this Client Library.
- Read the `Product documentation`_ to learn
  more about the product and see How-to Guides.
