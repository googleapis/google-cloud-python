Now that you have a project,
we need to make sure we are able to access our data.
There are many ways to authenticate,
but we're going to use a Service Account for today.

A *Service Account* is sort of like a username and password
(like when you're connecting to your MySQL database),
except the username is automatically generated
(and is an e-mail address)
and the password is actually a private key file.

To create a Service Account:

* **Click on Credentials**
  under the "APIs & Auth" section.

* **Click the big red button**
  that says "Create New Client ID"
  under the OAuth section
  (the first one).

* **Choose "Service Account"**
  and click the blue button
  that says "Create Client ID".

* **This will automatically**
  download a private key file.
  **Do not lose this.**

* **Rename your key** something shorter.
  I like to name the key ``<project name>.p12``.

  This is like your password for the account.

* **Copy the long weird e-mail address**
  labeled "E-mail address"
  in the information section
  for the Service Account
  you just created.

  This is like your username for the account.
