# Copyright 2019. PyData Development Team
# Distributed under BSD 3-Clause License.
# See LICENSE.txt for details.

import os

import pytest


@pytest.fixture(autouse=True)
def default_credentials(private_key_path):
    """Setup application default credentials for use in code samples."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private_key_path
