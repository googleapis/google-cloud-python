__version__ = '0.1'

# TODO: Allow specific scopes and authorization levels.
SCOPE = ('https://www.googleapis.com/auth/compute')
"""The scope required for authenticating as a Compute Engine consumer."""


def get_connection(project_name, client_email, private_key_path):
  from gcloud.credentials import Credentials
  from gcloud.compute.connection import Connection

  credentials = Credentials.get_for_service_account(
      client_email, private_key_path, scope=SCOPE)
  return Connection(project_name=project_name, credentials=credentials)
