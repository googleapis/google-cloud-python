Advanced Session Pool Topics
============================

Custom Session Pool Implementations
-----------------------------------

You can supply your own pool implementation, which must satisfy the
contract laid out in
:class:`~google.cloud.spanner.pool.AbstractSessionPool`:

.. code-block:: python

   from google.cloud.spanner.pool import AbstractSessionPool

   class MyCustomPool(AbstractSessionPool):

        def __init__(self, custom_param):
            super(MyCustomPool, self).__init__()
            self.custom_param = custom_param

        def bind(self, database):
            ...

        def get(self, read_only=False):
            ...

        def put(self, session, discard_if_full=True):
            ...

   pool = MyCustomPool(custom_param=42)
   database = instance.database(DATABASE_NAME, pool=pool)

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
   from google.cloud.spanner.pool import PingingPool

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
   from google.cloud.spanner.pool import TransactionPingingPool

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
