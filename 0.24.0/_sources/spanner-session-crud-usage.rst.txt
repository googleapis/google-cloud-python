Session Creation / Deletion
===========================

Outside of the admin APIs, all work with actual table data in a database
occurs in the context of a session.


Session Factory
---------------

To create a :class:`~google.cloud.spanner.session.Session` object:

.. code:: python

    session = database.session()


Create a new Session
--------------------

After creating the session object, use its
:meth:`~google.cloud.spanner.session.Session.create` method to
trigger its creation on the server:

.. code:: python

    session.create()


Test for the existence of a Session
-----------------------------------

After creating the session object, use its
:meth:`~google.cloud.spanner.session.Session.exists` method to determine
whether the session still exists on the server:

.. code:: python

    assert session.exists()


Delete a Session
----------------

Once done with the session object, use its
:meth:`~google.cloud.spanner.session.Session.delete` method to free up
its resources on the server:

.. code:: python

    session.delete()


Using a Session as a Context Manager
------------------------------------

Rather than calling the Session's
:meth:`~google.cloud.spanner.session.Session.create` and
:meth:`~google.cloud.spanner.session.Session.delete` methods directly,
you can use the session as a Python context manager:

.. code:: python

    with database.session() as session:

        assert session.exists()
        # perform session operations here

.. note::

   At the beginning of the ``with`` block, the session's
   :meth:`~google.cloud.spanner.session.Session.create` method is called.
   At the end of the ``with`` block, the session's
   :meth:`~google.cloud.spanner.session.Session.delete` method is called.


Next Step
---------

Next, learn about :doc:`spanner-session-implicit-txn-usage`.
