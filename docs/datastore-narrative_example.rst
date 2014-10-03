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

.. code-block:: csv

   "Date","Vendor","Type","Quantity","Price","Memo"
   "2014-08-26","United Airlines","Travel",1,425.00,"Airfaire, IAD <-> SFO"
   "2014-08-27","Yellow Cab","Travel",32.00,"Taxi to IAD"
   ...

Sally then submits her expense report from the command line using our
``submit_expenses`` script:

.. code-block:: bash

   $ submit_expenses create --employee-id=sally --description="Frotz project kickoff, San Jose" expenses-20140901.csv
   Processed 15 rows.
   Created, report ID: sally/expenses-2014-09-01

Sally can list all her submitted expense reports using our ``review_expenses``
script:

.. code-block:: bash

   $ review_expenses list --employee-id=sally

   "Report ID","Description","Status","Memo"
   "sally/2013-11-19","Onsite Training, Mountain View","Paid","Check #3715"
   "sally/2014-04-19","PyCon 2014, Montreal","Paid","Check #3992"
   "sally/2014-09-01","Frotz project kickoff, San Jose","Pending",""

Sally can review a submitted expense report using the its ID:

.. code-block:: bash

   $ review_expenses show --report-id=sally/expenses-2014-09-01
   Report-ID: sally/expenses-2014-09-01
   Report-Status: Pending
   Employee-ID: sally
   Description: Frotz project kickoff, San Jose

   "Date","Vendor","Type","Quantity","Price","Memo"
   "2014-08-26","United Airlines","Travel",1,425.00,"Airfaire, IAD <-> SFO"
   "2014-08-27","Yellow Cab","Travel",32.00,"Taxi to IAD"
   ...

While in "Pending" status, Sally can edit the CSV and resubmit it:

.. code-block:: bash

   $ submit_expenses update --report-id=sally/expenses-2014-09-01 expenses-20140901-amended.csv
   Processed 15 rows.
   Updated, report ID: sally/expenses-2014-09-01

Sally's boss, Pat, can review all open expense reports:

.. code-block:: bash

   $ review_expenses list --status=Pending

   "Report ID","Description","Status","Memo"
   "sally/2014-09-01","Frotz project kickoff, San Jose","Pending",""

and download the expenses just as above.  Pat can approve Sally's expense
report:

.. code-block:: bash

   $ review_expenses approve --report-id=sally/expenses-2014-09-01 --check-number=4093
   Approved, report ID: sally/expenses-2014-09-01, check #4093

or reject it:

.. code-block:: bash

   $ review_expenses reject --report-id=sally/expenses-2014-09-01 --reason="Travel not authorized by client"
   Rejected, report ID: sally/expenses-2014-09-01, reason: Travel not authorized by client
