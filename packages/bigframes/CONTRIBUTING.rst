############
Contributing
############

This package is part of the ``google-cloud-python`` monorepo.

Please refer to the centralized `Contributing Guide`_ at the repository root for general guidelines on how to contribute, set up your development environment, and submit pull requests.

.. _Contributing Guide: https://github.com/googleapis/google-cloud-python/blob/main/CONTRIBUTING.rst

Package-specific test sessions, dependencies, and supported Python versions are defined in this directory's ``noxfile.py``.

********************
Running System Tests
********************

- System tests will be run against an actual project. A project can be set in
  the environment variable ``$GOOGLE_CLOUD_PROJECT``. If not, the project property
  set in the `Google Cloud CLI <https://cloud.google.com/sdk/gcloud/reference/config/get>`__
  will be effective, which can be peeked into via ``gcloud config get project``,
  or set via ``gcloud config set project <project-name>``. The following roles
  carry the permissions to run the system tests in the project:

  - `BigQuery User <https://cloud.google.com/bigquery/docs/access-control#bigquery.user>`__
    to be able to create test datasets and run BigQuery jobs in the project.

  - `BigQuery Connection Admin <https://cloud.google.com/bigquery/docs/access-control#bigquery.connectionAdmin>`__
    to be able to use BigQuery connections in the project.

  - `BigQuery Data Editor <https://cloud.google.com/bigquery/docs/access-control#bigquery.dataEditor>`__
    to be able to create BigQuery remote functions in the project.

  - `Browser <https://cloud.google.com/resource-manager/docs/access-control-proj#browser>`__
    to be able to get current IAM policy for the service accounts of the BigQuery connections in the project.

  - `Cloud Functions Developer <https://cloud.google.com/functions/docs/reference/iam/roles#cloudfunctions.developer>`__
    to be able to create cloud functions to support BigQuery DataFrames remote functions.

  - `Service Account User <https://cloud.google.com/iam/docs/service-account-permissions#user-role>`__
    to be able to use the project's service accounts.

  - `Vertex AI User <https://cloud.google.com/vertex-ai/docs/general/access-control#aiplatform.user>`__
    to be able to use the BigQuery DataFrames' ML integration with Vertex AI.

- You can run the script ``scripts/setup-project-for-testing.sh <project-id> [<principal>]``
  to set up a project for running system tests and optionally set up necessary
  IAM roles for a principal (user/group/service-account). You need to have the following
  IAM permission to be able to run the set up script successfully:

  - ``serviceusage.services.enable``
  - ``bigquery.connections.create``
  - ``resourcemanager.projects.setIamPolicy``
