import os
from gcloud import dns


__all__ = ['get_connection', 'CLIENT_EMAIL', 'PRIVATE_KEY_PATH',
           'PROJECT_ID']


CLIENT_EMAIL = '524635209885-rda26ks46309o10e0nc8rb7d33rn0hlm@developer.gserviceaccount.com'
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.key')
PROJECT_ID = 'gceremote'


def get_connection():
  return dns.get_connection(PROJECT_ID, CLIENT_EMAIL, PRIVATE_KEY_PATH)
