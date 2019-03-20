import pytest

from google.cloud import datastore
from google.cloud import ndb

from . import KIND


@pytest.fixture(scope="module", autouse=True)
def initial_clean():
    # Make sure database is in clean state at beginning of test run
    client = datastore.Client()
    query = client.query(kind=KIND)
    for entity in query.fetch():
        client.delete(entity.key)


@pytest.fixture(scope="session")
def deleted_keys():
    return set()


@pytest.fixture
def to_delete():
    return []


@pytest.fixture
def ds_client(to_delete, deleted_keys):
    client = datastore.Client()

    # Make sure we're leaving database as clean as we found it after each test
    query = client.query(kind=KIND)
    results = [
        entity for entity in query.fetch() if entity.key not in deleted_keys
    ]
    assert not results

    yield client

    if to_delete:
        client.delete_multi(to_delete)
        deleted_keys.update(to_delete)

    results = [
        entity for entity in query.fetch() if entity.key not in deleted_keys
    ]
    assert not results


@pytest.fixture
def ds_entity(ds_client, dispose_of):
    def make_entity(*key_args, **entity_kwargs):
        key = ds_client.key(*key_args)
        assert ds_client.get(key) is None
        entity = datastore.Entity(key=key)
        entity.update(entity_kwargs)
        ds_client.put(entity)
        dispose_of(key)

        return entity

    yield make_entity


@pytest.fixture
def dispose_of(ds_client, to_delete):
    def delete_entity(ds_key):
        to_delete.append(ds_key)

    return delete_entity


@pytest.fixture
def client_context():
    client = ndb.Client()
    with client.context():
        yield
