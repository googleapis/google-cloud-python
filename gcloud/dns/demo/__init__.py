import os
from gcloud import dns


__all__ = ['get_connection', 'get_zone' 'CLIENT_EMAIL', 'PRIVATE_KEY_PATH',
           'PROJECT']


CLIENT_EMAIL = '524635209885-rda26ks46309o10e0nc8rb7d33rn0hlm@developer.gserviceaccount.com'
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.p12')
PROJECT = 'gceremote'


def get_connection():
  return dns.get_connection(PROJECT, CLIENT_EMAIL, PRIVATE_KEY_PATH)


def get_zone(zone):
  return dns.get_zone(zone, PROJECT, CLIENT_EMAIL, PRIVATE_KEY_PATH)
