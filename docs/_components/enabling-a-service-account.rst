A `Service Account`_ handles authentication for a backend service that
needs to talk to other services (e.g. Google APIs).

To create a Service Account:

#. Visit the `Google Developers Console`_.

#. Create a new project or click on an existing project.

#. Navigate to  **APIs & auth** > **APIs section** and turn on the following
   APIs (you may need to enable billing in order to use these services):

   * Google Cloud Datastore API
   * Google Cloud Storage
   * Google Cloud Storage JSON API
   * Google Pub/Sub API

#. Navigate to **APIs & auth** >  **Credentials** and then:

   * If you want to use a new service account, click on **Create new Client ID**
     and select **Service account**. After the account is created, you will be
     prompted to download the JSON key file that the library uses to authorize
     your requests.
   * If you want to generate a new key for an existing service account, click
     on **Generate new JSON key** and download the JSON key file.

.. _Google Developers Console: https://console.developers.google.com/project
.. _Service Account: https://developers.google.com/accounts/docs/OAuth2ServiceAccount
