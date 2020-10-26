# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import platform

PY_VERSION = platform.python_version()
VERSION = "2.2.0a1"
DEFAULT_USER_AGENT = "django_spanner/" + VERSION
