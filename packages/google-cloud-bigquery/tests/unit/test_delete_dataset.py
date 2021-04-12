from .helpers import make_connection, make_client, dataset_polymorphic
import google.api_core.exceptions
import pytest


@dataset_polymorphic
def test_delete_dataset(make_dataset, get_reference, client, PROJECT, DS_ID):
    dataset = make_dataset(PROJECT, DS_ID)
    PATH = "projects/%s/datasets/%s" % (PROJECT, DS_ID)
    conn = client._connection = make_connection({})
    client.delete_dataset(dataset, timeout=7.5)
    conn.api_request.assert_called_with(
        method="DELETE", path="/%s" % PATH, query_params={}, timeout=7.5
    )


@dataset_polymorphic
def test_delete_dataset_delete_contents(
    make_dataset, get_reference, client, PROJECT, DS_ID
):
    PATH = "projects/%s/datasets/%s" % (PROJECT, DS_ID)
    conn = client._connection = make_connection({})
    dataset = make_dataset(PROJECT, DS_ID)
    client.delete_dataset(dataset, delete_contents=True)
    conn.api_request.assert_called_with(
        method="DELETE",
        path="/%s" % PATH,
        query_params={"deleteContents": "true"},
        timeout=None,
    )


def test_delete_dataset_wrong_type(client):
    with pytest.raises(TypeError):
        client.delete_dataset(42)


def test_delete_dataset_w_not_found_ok_false(PROJECT, DS_ID):
    path = "/projects/{}/datasets/{}".format(PROJECT, DS_ID)
    http = object()
    client = make_client(_http=http)
    conn = client._connection = make_connection(
        google.api_core.exceptions.NotFound("dataset not found")
    )

    with pytest.raises(google.api_core.exceptions.NotFound):
        client.delete_dataset(DS_ID)

    conn.api_request.assert_called_with(
        method="DELETE", path=path, query_params={}, timeout=None
    )


def test_delete_dataset_w_not_found_ok_true(PROJECT, DS_ID):
    path = "/projects/{}/datasets/{}".format(PROJECT, DS_ID)
    http = object()
    client = make_client(_http=http)
    conn = client._connection = make_connection(
        google.api_core.exceptions.NotFound("dataset not found")
    )
    client.delete_dataset(DS_ID, not_found_ok=True)
    conn.api_request.assert_called_with(
        method="DELETE", path=path, query_params={}, timeout=None
    )
