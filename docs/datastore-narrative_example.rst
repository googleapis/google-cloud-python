Cloud Datastore Narrative / Example Application
===============================================

Overview
--------

In order to give a better feel for how a Python application might use the
:mod:`gcloud.datastore` API, let's look at building an example application
which stores its data using the API.  In order to focus on the API, the
sample application will be built as a set of command-line scripts.

For our example, let's build an employee expense reporting system.  An example
set of interactions might look like the following scenario.

Returning from a trip to the Bay Area, Sally creates a CSV file,
``expenses-20140901.csv``, containing one row for each line item in her
expense report:

.. code-block:: none

   "Date","Vendor","Type","Quantity","Price","Memo"
   "2014-08-26","United Airlines","Travel",1,425.00,"Airfaire, IAD <-> SFO"
   "2014-08-27","Yellow Cab","Travel",32.00,"Taxi to IAD"
   ...

Sally then submits her expense report from the command line using our
:program:`submit_expenses` script:

.. code-block:: bash

   $ submit_expenses create --employee-id=sally --description="Frotz project kickoff, San Jose" expenses-20140901.csv
   Processed 15 rows.
   Created report: sally/expenses-2014-09-01

Sally can list all her submitted expense reports using our
:program:`review_expenses` script:

.. code-block:: bash

   $ review_expenses list --employee-id=sally

   "Employee ID", "Report ID","Created","Updated","Description","Status","Memo"
   "sally","expenses-2013-11-19","2013-12-01","2013-12-01","Onsite Training, Mountain View","Paid","Check #3715"
   "sally","expenses-2014-04-19","2014-04-21","2014-04-22","PyCon 2014, Montreal","Paid","Check #3992"
   "sally","expenses-2014-09-01","2014-09-04","2014-09-04","Frotz project kickoff, San Jose","pending",""

Sally can review a submitted expense report using the its ID:

.. code-block:: bash

   $ review_expenses show expenses-2014-09-01
   Report-ID: sally/expenses-2014-09-01
   Report-Status: pending
   Employee-ID: sally
   Description: Frotz project kickoff, San Jose

   "Date","Vendor","Type","Quantity","Price","Memo"
   "2014-08-26","United Airlines","Travel",1,425.00,"Airfaire, IAD <-> SFO"
   "2014-08-27","Yellow Cab","Travel",32.00,"Taxi to IAD"
   ...

While in "pending" status, Sally can edit the CSV and resubmit it:

.. code-block:: bash

   $ submit_expenses update expenses-20140901-amended.csv
   Updated report: sally/expenses-2014-09-01
   Processed 15 rows.

While it remains in "pending" status, Sally can also delete the report:

.. code-block:: bash

   $ submit_expenses delete expenses-20140901-amended
   Deleted report: sally/expenses-2014-09-01
   Removed 15 items.

Sally's boss, Pat, can review all open expense reports:

.. code-block:: bash

   $ review_expenses list --status=pending

   "Employee ID","Report ID","Created","Updated","Description","Status","Memo"
   "sally","expenses-2014-09-01","2014-09-04","2014-09-04","Frotz project kickoff, San Jose","pending",""


Pat can download Sally's report by supplying ``--employee-id=sally``:

.. code-block:: bash

   $ review_expenses show --employee-id=sally expenses-2014-09-01
   Report-ID: sally/expenses-2014-09-01
   Report-Status: pending
   Employee-ID: sally
   Description: Frotz project kickoff, San Jose

   "Date","Vendor","Type","Quantity","Price","Memo"
   "2014-08-26","United Airlines","Travel",1,425.00,"Airfaire, IAD <-> SFO"
   "2014-08-27","Yellow Cab","Travel",32.00,"Taxi to IAD"

Pat can approve Sally's expense report:

.. code-block:: bash

   $ review_expenses approve --check-number=4093 sally expenses-2014-09-01
   Approved, report: sally/expenses-2014-09-01, check #4093

or reject it:

.. code-block:: bash

   $ review_expenses reject --reason="Travel not authorized by client" sally expenses-2014-09-01
   Rejected, report: sally/expenses-2014-09-01, reason: Travel not authorized by client

Connecting to the API Dataset
-----------------------------

The sample application uses a utility function, :func:`expenses._get_dataset`,
to set up the connection.

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _get_dataset

Thie function expects three environment variables to be set up, using
your project's
`OAuth2 API credentials <https://developers.google.com/console/help/new/#generatingoauth2>`_:

- :envvar:`GCLOUD_TESTS_DATASET_ID` is your Google API Project ID
- :envvar:`GCLOUD_TESTS_CLIENT_EMAIL` is your Google API email-address
- :envvar:`GCLOUD_TESTS_TESTS_KEY_FILE` is the filesystem path to your
  Google API private key.

Creating a New Expense Report
-----------------------------

In the sample application, the ``create`` subcommand of the
:program:`submit_expenses` script drives a function,
:func:`expenses.create_report`:

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: create_report
   :linenos:

After connecting to the dataset via :func:`expenses._get_dataset` (line 2),
:func:`expenses.create_report` starts a transaction (line 3) to ensure that
all changes are performed atomically.  It then checks that no report exists
already for the given employee ID and report ID, raising an exception if so
(lines 4-5).  It then  delegates most of the work to the
:func:`expenses._upsert_report` utility function (line 6), finally setting
metadata on the report itself (lines 7-11).


.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _upsert_report
   :linenos:

The :func:`expenses._upsert_report` function: in turn delegates to
:func:`expenses._get_employee`, :func:`expenses._get_report`, and
:func:`expenses._purge_report_items` to ensure that the employee and report
exist, and that the report contains no items (lines 2-4).  It then
iterates over the rows from the CSV file, creating an item for each row
(lines 5-13), finally returning the populated report object (line 14).

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _get_employee
   :linenos:

The :func:`expenses._get_employee` function: looks up an employee (lines 2-3).

.. note:: Employee entities have no "parent" object: they exist at the "top"
          level.

If the employee entity does not exist, and the caller requests it, the
function creates a new employee entity and saves it.

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _get_report
   :linenos:

The :func:`expenses._get_employee` function: looks up an expense report
using an "ancestor" query (lines 2-3).

.. note:: Each expense report entities es expected to have an employee entity
          as its "parent".

If the expense report entity does not exist, and the caller requests it, the
function creates a new expense report entity and saves it.

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _purge_report_items
   :linenos:

The :func:`expenses._purge_report_items` function: delegates to
:func:`expenses._fetch_report_items` to find expense item entities contained
within the given report (line 4), and deletes them (line 5).  It returns
a count of the deleted items.

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: _fetch_report_items
   :linenos:

The :func:`expenses._purge_report_items` function: performs an "ancestor"
query (lines 2-3) to find expense item entities contained within a given
expense report.

Updating an Existing Expense Report
-----------------------------------

In the sample application, the ``update`` subcommand of the
:program:`submit_expenses` script drives a function,
:func:`expenses.update_report`:

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: update_report
   :linenos:

After connecting to the dataset via :func:`expenses._get_dataset` (line 2),
:func:`expenses.update_report` starts a transaction (line 3) to ensure that
all changes are performed atomically.  It then checks that a report *does*
exist already for the given employee ID and report ID, and that it is in
``pending`` staus, raising an exception if not (lines 3-4).  It then
delegates most of the work to the :func:`expenses._upsert_report` utility
function (line 6), finally updating metadata on the report itself (lines 7-11).

Listing Expense Reports
-----------------------

In the sample application, the ``list`` subcommand of the
:program:`review_expenses` script drives a function,
:func:`expenses.list_reports`:

.. literalinclude:: examples/expenses/expenses/__init__.py
   :pyobject: list_reports
   :linenos:

After connecting to the dataset via :func:`expenses._get_dataset` (line 2),
:func:`expenses.list_reports` creates a :class:`~gcloud.dataset.query.Query`
instance, limited to entities of kind, ``Expense Report`` (line 3), and
applies filtering based on the passed criteria:

- If ``employee_id`` is passed, it adds an "ancestor" filter to
  restrict the reslts to expense reports contained in the given employee
  (lines 4-6).

- If ``status`` is passed, it adds an "attribute" filter to
  restrict the reslts to expense reports which have that status (lines 7-8).

.. note::

   The function does *not* set up a transaction, as it uses only
   "read" operations on the API.

Finally, the function fetches the expense report entities returned by
the query and iterates over them, returning a mapping describing the
report (lines 9-30).
