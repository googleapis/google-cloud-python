import os
from gcloud import dns


__all__ = ['get_connection', 'get_zone' 'CLIENT_EMAIL', 'PRIVATE_KEY_PATH',
           'PROJECT']


CLIENT_EMAIL = ''
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.key')
PROJECT = ''


def get_connection():
  return dns.get_connection(PROJECT, CLIENT_EMAIL, PRIVATE_KEY_PATH)


def get_zone(zone_name):
  return dns.get_zone(zone_name, PROJECT, CLIENT_EMAIL, PRIVATE_KEY_PATH)
