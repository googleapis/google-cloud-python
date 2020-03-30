# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import sys

from google.api_core.gapic_v1.client_info import ClientInfo

VERSION = '0.0.1'
DEFAULT_USER_AGENT = 'django_spanner/' + VERSION

vers = sys.version_info


def google_client_info(user_agent=None):
    """
    Return a google.api_core.gapic_v1.client_info.ClientInfo
    containg the user_agent and python_version for this library
    """

    return ClientInfo(
        user_agent=user_agent or DEFAULT_USER_AGENT,
        python_version='%d.%d.%d' % (vers.major, vers.minor, vers.micro or 0),
    )
