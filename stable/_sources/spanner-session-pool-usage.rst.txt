Session Pools
#############

In order to minimize the latency of session creation, you can set up a
session pool on your database.  For instance, to use a pool which does *not*
block when exhausted, and which pings each session at checkout:

Configuring a session pool for a database
-----------------------------------------

.. code-block:: python

   from google.cloud.spanner import Client
   from google.cloud.spanner import FixedSizePool
   client = Client()
   instance = client.instance(INSTANCE_NAME)
   database = instance.database(DATABASE_NAME)
   pool = FixedSizePool(database, size=10, default_timeout=5)

Note that creating the pool presumes that its database already exists, as
it may need to pre-create sessions (rather than creating them on demand).

You can supply your own pool implementation, which must satisfy the
contract laid out in
:class:`~google.cloud.spanner.session.AbstractSessionPool`:

.. code-block:: python

   from google.cloud.spanner import AbstractSessionPool

   class MyCustomPool(AbstractSessionPool):

        def __init__(self, database, custom_param):
            super(MyCustomPool, self).__init__(database)
            self.custom_param = custom_param

        def get(self, read_only=False):
            ...

        def put(self, session, discard_if_full=True):
            ...

   database = instance.database(DATABASE_NAME, pool=pool)
   pool = MyCustomPool(database, custom_param=42)


Checking out sessions from the pool
-----------------------------------

No matter what kind of pool you create for the database, you can check out
a session from the pool, rather than creating it manually.  The
:meth:`~google.cloud.spanner.session.AbstractSessionPool.session` method
returns an object designed to be used as a context manager, checking the
session out from the pool and returning it automatically:

.. code-block:: python

    with pool.session() as session:

        snapshot = session.snapshot()

        result = snapshot.read(
            table='table-name', columns=['first_name', 'last_name', 'age'],
            key_set=['phred@example.com', 'bharney@example.com'])

        for row in result.rows:
            print(row)

Some pool implementations may allow additional keyword arguments when checked
out:

.. code-block:: python

    with pool.session(read_only=True) as session:

        snapshot = session.snapshot()

        result = snapshot.read(
            table='table-name', columns=['first_name', 'last_name', 'age'],
            key_set=['phred@example.com', 'bharney@example.com'])

        for row in result.rows:
            print(row)


Lowering latency for read / query operations
--------------------------------------------

Some applications may need to minimize latency for read operations, including
particularly the overhead of making an API request to create or refresh a
session.  :class:`~google.cloud.spanner.pool.PingingPool` is designed for such
applications, which need to configure a background thread to do the work of
keeping the sessions fresh.

Create an instance of :class:`~google.cloud.spanner.pool.PingingPool`:

.. code-block:: python

   from google.cloud.spanner import Client
   from google.cloud.spanner import PingingPool

   client = Client()
   instance = client.instance(INSTANCE_NAME)
   pool = PingingPool(size=10, default_timeout=5, ping_interval=300)
   database = instance.database(DATABASE_NAME, pool=pool)

Set up a background thread to ping the pool's session, keeping them
from becoming stale:

.. code-block:: python

   import threading

   background = threading.Thread(target=pool.ping, name='ping-pool')
   background.daemon = True
   background.start()

``database.execute_sql()`` is a shortcut, which checks out a session, creates a
snapshot, and uses the snapshot to execute a query:

.. code-block:: python

   QUERY = """\
   SELECT first_name, last_name, age FROM table-name
   WHERE email in ["phred@example.com", "bharney@example.com"]
   """
   result = database.execute_sql(QUERY)

   for row in result:
       do_something_with(row)


Lowering latency for mixed read-write operations
------------------------------------------------

Some applications may need to minimize latency for read write operations,
including particularly the overhead of making an API request to create or
refresh a session or to begin a session's transaction.
:class:`~google.cloud.spanner.pool.TransactionPingingPool` is designed for
such applications, which need to configure a background thread to do the work
of keeping the sessions fresh and starting their transactions after use.

Create an instance of
:class:`~google.cloud.spanner.pool.TransactionPingingPool`:

.. code-block:: python

   from google.cloud.spanner import Client
   from google.cloud.spanner import TransactionPingingPool

   client = Client()
   instance = client.instance(INSTANCE_NAME)
   pool = TransactionPingingPool(size=10, default_timeout=5, ping_interval=300)
   database = instance.database(DATABASE_NAME, pool=pool)

Set up a background thread to ping the pool's session, keeping them
from becoming stale, and ensuring that each session has a new transaction
started before it is used:

.. code-block:: python

   import threading

   background = threading.Thread(target=pool.ping, name='ping-pool')
   background.daemon = True
   background.start()

``database.run_in_transaction()`` is a shortcut:  it checks out a session
and uses it to perform a set of read and write operations inside the context
of a transaction, retrying if aborted.  The application must supply a callback
function,  which is passed a transaction (plus any additional parameters
passed), and does its work using that transaction.

.. code-block:: python

   import datetime

   QUERY = """\
   SELECT employee_id, sum(hours) FROM daily_hours
   WHERE start_date >= %s AND end_date < %s
   GROUP BY employee_id id ORDER BY employee_id id"""

   def unit_of_work(transaction, month_start, month_end):
       """Compute rolled-up hours for a given month."""
       query = QUERY % (month_start.isoformat(),
              (month_end + datetime.timedelta(1)).isoformat())
       row_iter = transaction.execute_sql(query)

       for emp_id, hours, pay in _compute_pay(row_iter):
           transaction.insert_or_update(
               table='monthly_hours',
               columns=['employee_id', 'month', 'hours', 'pay'],
               values=[emp_id, month_start, hours, pay])

   database.run_in_transaction(
       unit_of_work,
       month_start=datetime.date(2016, 12, 1),
       month_end.date(2016, 12, 31))
