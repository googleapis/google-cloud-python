import itertools
import os
import uuid

import pytest
import requests

from google.cloud import datastore
from google.cloud import ndb

from google.cloud.ndb import global_cache as global_cache_module

from . import KIND, OTHER_KIND, OTHER_NAMESPACE


def _make_ds_client(namespace):
    emulator = bool(os.environ.get("DATASTORE_EMULATOR_HOST"))
    if emulator:
        client = datastore.Client(namespace=namespace, _http=requests.Session)
    else:
        client = datastore.Client(namespace=namespace)

    return client


def all_entities(client):
    return itertools.chain(
        client.query(kind=KIND).fetch(),
        client.query(kind=OTHER_KIND).fetch(),
        client.query(namespace=OTHER_NAMESPACE).fetch(),
    )


@pytest.fixture(scope="module", autouse=True)
def initial_clean():
    # Make sure database is in clean state at beginning of test run
    client = _make_ds_client(None)
    for entity in all_entities(client):
        client.delete(entity.key)


@pytest.fixture(scope="session")
def deleted_keys():
    return set()


@pytest.fixture
def to_delete():
    return []


@pytest.fixture
def ds_client(namespace):
    return _make_ds_client(namespace)


@pytest.fixture
def with_ds_client(ds_client, to_delete, deleted_keys):
    # Make sure we're leaving database as clean as we found it after each test
    results = [
        entity
        for entity in all_entities(ds_client)
        if entity.key not in deleted_keys
    ]
    assert not results

    yield ds_client

    if to_delete:
        ds_client.delete_multi(to_delete)
        deleted_keys.update(to_delete)

    not_deleted = [
        entity
        for entity in all_entities(ds_client)
        if entity.key not in deleted_keys
    ]
    assert not not_deleted


@pytest.fixture
def ds_entity(with_ds_client, dispose_of):
    def make_entity(*key_args, **entity_kwargs):
        key = with_ds_client.key(*key_args)
        assert with_ds_client.get(key) is None
        entity = datastore.Entity(key=key)
        entity.update(entity_kwargs)
        with_ds_client.put(entity)
        dispose_of(key)

        return entity

    yield make_entity


@pytest.fixture
def ds_entity_with_meanings(with_ds_client, dispose_of):
    def make_entity(*key_args, **entity_kwargs):
        meanings = key_args[0]
        key = with_ds_client.key(*key_args[1:])
        assert with_ds_client.get(key) is None
        entity = datastore.Entity(key=key, exclude_from_indexes=("blob",))
        entity._meanings = meanings
        entity.update(entity_kwargs)
        with_ds_client.put(entity)
        dispose_of(key)

        return entity

    yield make_entity


@pytest.fixture
def dispose_of(with_ds_client, to_delete):
    def delete_entity(*ds_keys):
        to_delete.extend(ds_keys)

    return delete_entity


@pytest.fixture
def namespace():
    return str(uuid.uuid4())


@pytest.fixture
def client_context(namespace):
    client = ndb.Client(namespace=namespace)
    with client.context(cache_policy=False, legacy_data=False) as the_context:
        yield the_context


@pytest.fixture
def redis_context(client_context):
    global_cache = global_cache_module.RedisCache.from_environment()
    with client_context.new(global_cache=global_cache).use() as context:
        context.set_global_cache_policy(None)  # Use default
        yield context
