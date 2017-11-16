Python Client for Cloud Spanner
===============================

    Python idiomatic client for `Cloud Spanner`_.

.. _Cloud Spanner: https://cloud.google.com/spanner/

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/spanner/usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-spanner

For more information on setting up your Python development environment,
such as installing ``pip`` and ``virtualenv`` on your system, please refer
to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup


Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication


Using the API
-------------

Cloud Spanner is the world’s first fully managed relational database service
to offer both strong consistency and horizontal scalability for
mission-critical online transaction processing (OLTP) applications. With Cloud
Spanner you enjoy all the traditional benefits of a relational database; but
unlike any other relational database service, Cloud Spanner scales
horizontally to hundreds or thousands of servers to handle the biggest
transactional workloads. (`About Cloud Spanner`_)

.. _About Cloud Spanner: https://cloud.google.com/spanner/


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


Insert records using a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Update records using a Transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Learn More
----------

See the ``google-cloud-python`` API `Cloud Spanner documentation`_ to learn how
to connect to Cloud Spanner using this Client Library.

.. _Cloud Spanner documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/spanner/usage.html

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-spanner.svg
   :target: https://pypi.org/project/google-cloud-spanner/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-spanner.svg
   :target: https://pypi.org/project/google-cloud-spanner/
