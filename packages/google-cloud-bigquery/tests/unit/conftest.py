import pytest

from .helpers import make_client


@pytest.fixture
def client():
    yield make_client()


@pytest.fixture
def PROJECT():
    yield "PROJECT"


@pytest.fixture
def DS_ID():
    yield "DATASET_ID"


@pytest.fixture
def LOCATION():
    yield "us-central"
