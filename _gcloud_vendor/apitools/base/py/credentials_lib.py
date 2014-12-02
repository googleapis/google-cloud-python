#!/usr/bin/env python
"""Common credentials classes and constructors."""

import httplib
import json
import os
import urllib2


import httplib2
import oauth2client
import oauth2client.client
import oauth2client.gce
import oauth2client.multistore_file
import oauth2client.tools

try:
    from gflags import FLAGS
except ImportError:
    FLAGS = None

import logging

from apitools.base.py import exceptions
from apitools.base.py import util

__all__ = [
    'CredentialsFromFile',
    'GaeAssertionCredentials',
    'GceAssertionCredentials',
    'GetCredentials',
    'ServiceAccountCredentials',
    'ServiceAccountCredentialsFromFile',
]



# TODO(craigcitro): Expose the extra args here somewhere higher up,
# possibly as flags in the generated CLI.
def GetCredentials(package_name, scopes, client_id, client_secret, user_agent,
                   credentials_filename=None,
                   service_account_name=None, service_account_keyfile=None,
                   api_key=None, client=None):
  """Attempt to get credentials, using an oauth dance as the last resort."""
  scopes = util.NormalizeScopes(scopes)
  # TODO(craigcitro): Error checking.
  client_info = {
      'client_id': client_id,
      'client_secret': client_secret,
      'scope': ' '.join(sorted(util.NormalizeScopes(scopes))),
      'user_agent': user_agent or '%s-generated/0.1' % package_name,
  }
  if service_account_name is not None:
    credentials = ServiceAccountCredentialsFromFile(
        service_account_name, service_account_keyfile, scopes)
    if credentials is not None:
      return credentials
  credentials = GaeAssertionCredentials.Get(scopes)
  if credentials is not None:
    return credentials
  credentials = GceAssertionCredentials.Get(scopes)
  if credentials is not None:
    return credentials
  credentials_filename = credentials_filename or os.path.expanduser(
      '~/.apitools.token')
  credentials = CredentialsFromFile(credentials_filename, client_info)
  if credentials is not None:
    return credentials
  raise exceptions.CredentialsError('Could not create valid credentials')


def ServiceAccountCredentialsFromFile(
    service_account_name, private_key_filename, scopes):
  with open(private_key_filename) as key_file:
    return ServiceAccountCredentials(
        service_account_name, key_file.read(), scopes)


def ServiceAccountCredentials(service_account_name, private_key, scopes):
  scopes = util.NormalizeScopes(scopes)
  return oauth2client.client.SignedJwtAssertionCredentials(
      service_account_name, private_key, scopes)


# TODO(craigcitro): We override to add some utility code, and to
# update the old refresh implementation. Either push this code into
# oauth2client or drop oauth2client.
class GceAssertionCredentials(oauth2client.gce.AppAssertionCredentials):
  """Assertion credentials for GCE instances."""

  def __init__(self, scopes=None, service_account_name='default', **kwds):
    if not util.DetectGce():
      raise exceptions.ResourceUnavailableError(
          'GCE credentials requested outside a GCE instance')
    self.__service_account_name = service_account_name
    if scopes:
      scope_ls = util.NormalizeScopes(scopes)
      instance_scopes = self.GetInstanceScopes()
      if scope_ls > instance_scopes:
        raise exceptions.CredentialsError(
            'Instance did not have access to scopes %s' % (
                sorted(list(scope_ls - instance_scopes)),))
    else:
      scopes = self.GetInstanceScopes()
    super(GceAssertionCredentials, self).__init__(scopes, **kwds)

  @classmethod
  def Get(cls, *args, **kwds):
    try:
      return cls(*args, **kwds)
    except exceptions.Error:
      return None

  def GetInstanceScopes(self):
    # Extra header requirement can be found here:
    # https://developers.google.com/compute/docs/metadata
    scopes_uri = (
        'http://metadata.google.internal/computeMetadata/v1/instance/'
        'service-accounts/%s/scopes') % self.__service_account_name
    additional_headers = {'X-Google-Metadata-Request': 'True'}
    request = urllib2.Request(scopes_uri, headers=additional_headers)
    try:
      response = urllib2.urlopen(request)
    except urllib2.URLError as e:
      raise exceptions.CommunicationError(
          'Could not reach metadata service: %s' % e.reason)
    return util.NormalizeScopes(scope.strip() for scope in response.readlines())

  def _refresh(self, do_request):
    """Refresh self.access_token.

    Args:
      do_request: A function matching httplib2.Http.request's signature.
    """
    token_uri = (
        'http://metadata.google.internal/computeMetadata/v1beta1/instance/'
        'service-accounts/%s/token') % self.__service_account_name
    extra_headers = {'X-Google-Metadata-Request': 'True'}
    response, content = do_request(token_uri, headers=extra_headers)
    if response.status != httplib.OK:
      raise exceptions.CredentialsError(
          'Error refreshing credentials: %s' % content)
    try:
      credential_info = json.loads(content)
    except ValueError:
      raise exceptions.CredentialsError(
          'Invalid credentials response: %s' % content)
    self.access_token = credential_info['access_token']


# TODO(craigcitro): Currently, we can't even *load*
# `oauth2client.appengine` without being on appengine, because of how
# it handles imports. Fix that by splitting that module into
# GAE-specific and GAE-independent bits, and guarding imports.
class GaeAssertionCredentials(oauth2client.client.AssertionCredentials):
  """Assertion credentials for Google App Engine apps."""

  def __init__(self, scopes, **kwds):
    if not util.DetectGae():
      raise exceptions.ResourceUnavailableError(
          'GCE credentials requested outside a GCE instance')
    self._scopes = list(util.NormalizeScopes(scopes))
    super(GaeAssertionCredentials, self).__init__(None, **kwds)

  @classmethod
  def Get(cls, *args, **kwds):
    try:
      return cls(*args, **kwds)
    except exceptions.Error:
      return None

  @classmethod
  def from_json(cls, json_data):
    data = json.loads(json_data)
    return GaeAssertionCredentials(data['_scopes'])

  def _refresh(self, _):
    """Refresh self.access_token.

    Args:
      _: (ignored) A function matching httplib2.Http.request's signature.
    """
    from google.appengine.api import app_identity
    try:
      token, _ = app_identity.get_access_token(self._scopes)
    except app_identity.Error as e:
      raise exceptions.CredentialsError(str(e))
    self.access_token = token


# TODO(craigcitro): Switch this from taking a path to taking a stream.
def CredentialsFromFile(path, client_info):
  """Read credentials from a file."""
  credential_store = oauth2client.multistore_file.get_credential_storage(
      path,
      client_info['client_id'],
      client_info['user_agent'],
      client_info['scope'])
  if hasattr(FLAGS, 'auth_local_webserver'):
    FLAGS.auth_local_webserver = False
  credentials = credential_store.get()
  if credentials is None or credentials.invalid:
    print 'Generating new OAuth credentials ...'
    while True:
      # If authorization fails, we want to retry, rather than let this
      # cascade up and get caught elsewhere. If users want out of the
      # retry loop, they can ^C.
      try:
        flow = oauth2client.client.OAuth2WebServerFlow(**client_info)
        credentials = oauth2client.tools.run(flow, credential_store)
        break
      except (oauth2client.client.FlowExchangeError, SystemExit) as e:
        # Here SystemExit is "no credential at all", and the
        # FlowExchangeError is "invalid" -- usually because you reused
        # a token.
        print 'Invalid authorization: %s' % (e,)
      except httplib2.HttpLib2Error as e:
        print 'Communication error: %s' % (e,)
        raise exceptions.CredentialsError(
            'Communication error creating credentials: %s' % e)
  return credentials
