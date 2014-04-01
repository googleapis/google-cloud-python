__version__ = '0.1'

# TODO: Allow specific scopes and authorization levels.
SCOPE = ('https://www.googleapis.com/auth/cloud-platform',
         'https://www.googleapis.com/auth/ndev.clouddns.readonly',
         'https://www.googleapis.com/auth/ndev.clouddns.readwrite')
"""The scope required for authenticating as a Cloud DNS consumer."""


def get_connection(project_id, client_email, private_key_path):
  from gcloud.credentials import Credentials
  from gcloud.dns.connection import Connection

  credentials = Credentials.get_for_service_account(
      client_email, private_key_path, scope=SCOPE)
  return Connection(project_id=project_id, credentials=credentials)
