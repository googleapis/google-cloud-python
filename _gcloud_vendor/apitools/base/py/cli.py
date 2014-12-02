#!/usr/bin/env python
"""Top-level import for all CLI-related functionality in apitools.

Note that importing this file will ultimately have side-effects, and
may require imports not available in all environments (such as App
Engine). In particular, picking up some readline-related imports can
cause pain.
"""

# pylint:disable=wildcard-import

from apitools.base.py.app2 import *
from apitools.base.py.base_cli import *
