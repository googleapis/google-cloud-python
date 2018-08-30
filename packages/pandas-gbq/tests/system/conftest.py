"""Shared pytest fixtures for system tests."""

import os
import os.path

import pytest


@pytest.fixture(scope="session")
def project_id():
    return os.environ.get("GBQ_PROJECT_ID") or os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # noqa


@pytest.fixture(scope="session")
def private_key_path():
    path = None
    if "TRAVIS_BUILD_DIR" in os.environ:
        path = os.path.join(
            os.environ["TRAVIS_BUILD_DIR"], "ci", "travis_gbq.json"
        )
    elif "GBQ_GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        path = os.environ["GBQ_GOOGLE_APPLICATION_CREDENTIALS"]
    elif "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    if path is None:
        pytest.skip(
            "Cannot run integration tests without a "
            "private key json file path"
        )
        return None
    if not os.path.isfile(path):
        pytest.skip(
            "Cannot run integration tests when there is "
            "no file at the private key json file path"
        )
        return None

    return path


@pytest.fixture(scope="session")
def private_key_contents(private_key_path):
    if private_key_path is None:
        return None

    with open(private_key_path) as f:
        return f.read()
