# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import pytest

from google.api_core import exceptions
from . import _helpers


def test_bucket_create_w_alt_storage_class(storage_client, buckets_to_delete):
    from google.cloud.storage import constants

    bucket_name = _helpers.unique_name("bucket-w-archive")

    with pytest.raises(exceptions.NotFound):
        storage_client.get_bucket(bucket_name)

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = constants.ARCHIVE_STORAGE_CLASS

    _helpers.retry_429_503(bucket.create)()
    buckets_to_delete.append(bucket)

    created = storage_client.get_bucket(bucket_name)
    assert created.storage_class == constants.ARCHIVE_STORAGE_CLASS


def test_bucket_lifecycle_rules(storage_client, buckets_to_delete):
    from google.cloud.storage import constants
    from google.cloud.storage.bucket import LifecycleRuleDelete
    from google.cloud.storage.bucket import LifecycleRuleSetStorageClass

    bucket_name = _helpers.unique_name("w-lifcycle-rules")
    custom_time_before = datetime.date(2018, 8, 1)
    noncurrent_before = datetime.date(2018, 8, 1)

    with pytest.raises(exceptions.NotFound):
        storage_client.get_bucket(bucket_name)

    bucket = storage_client.bucket(bucket_name)
    bucket.add_lifecycle_delete_rule(
        age=42,
        number_of_newer_versions=3,
        days_since_custom_time=2,
        custom_time_before=custom_time_before,
        days_since_noncurrent_time=2,
        noncurrent_time_before=noncurrent_before,
    )
    bucket.add_lifecycle_set_storage_class_rule(
        constants.COLDLINE_STORAGE_CLASS,
        is_live=False,
        matches_storage_class=[constants.NEARLINE_STORAGE_CLASS],
    )

    expected_rules = [
        LifecycleRuleDelete(
            age=42,
            number_of_newer_versions=3,
            days_since_custom_time=2,
            custom_time_before=custom_time_before,
            days_since_noncurrent_time=2,
            noncurrent_time_before=noncurrent_before,
        ),
        LifecycleRuleSetStorageClass(
            constants.COLDLINE_STORAGE_CLASS,
            is_live=False,
            matches_storage_class=[constants.NEARLINE_STORAGE_CLASS],
        ),
    ]

    _helpers.retry_429_503(bucket.create)(location="us")
    buckets_to_delete.append(bucket)

    assert bucket.name == bucket_name
    assert list(bucket.lifecycle_rules) == expected_rules

    bucket.clear_lifecyle_rules()
    bucket.patch()

    assert list(bucket.lifecycle_rules) == []


def test_bucket_update_labels(storage_client, buckets_to_delete):
    bucket_name = _helpers.unique_name("update-labels")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)
    assert bucket.exists()

    updated_labels = {"test-label": "label-value"}
    bucket.labels = updated_labels
    bucket.update()
    assert bucket.labels == updated_labels

    new_labels = {"another-label": "another-value"}
    bucket.labels = new_labels
    bucket.patch()
    assert bucket.labels == new_labels

    bucket.labels = {}
    # See https://github.com/googleapis/python-storage/issues/541
    retry_400 = _helpers.RetryErrors(exceptions.BadRequest)
    retry_400(bucket.update)()
    assert bucket.labels == {}


def test_bucket_get_set_iam_policy(
    storage_client, buckets_to_delete, service_account,
):
    from google.cloud.storage.iam import STORAGE_OBJECT_VIEWER_ROLE
    from google.api_core.exceptions import BadRequest
    from google.api_core.exceptions import PreconditionFailed

    bucket_name = _helpers.unique_name("iam-policy")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)
    assert bucket.exists()

    policy_no_version = bucket.get_iam_policy()
    assert policy_no_version.version == 1

    policy = bucket.get_iam_policy(requested_policy_version=3)
    assert policy == policy_no_version

    member = "serviceAccount:{}".format(storage_client.get_service_account_email())

    binding_w_condition = {
        "role": STORAGE_OBJECT_VIEWER_ROLE,
        "members": {member},
        "condition": {
            "title": "always-true",
            "description": "test condition always-true",
            "expression": "true",
        },
    }
    policy.bindings.append(binding_w_condition)

    with pytest.raises(PreconditionFailed, match="enable uniform bucket-level access"):
        bucket.set_iam_policy(policy)

    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(binding_w_condition)

    with pytest.raises(BadRequest, match="at least 3"):
        bucket.set_iam_policy(policy)

    policy.version = 3
    returned_policy = bucket.set_iam_policy(policy)
    assert returned_policy.version == 3
    assert returned_policy.bindings == policy.bindings

    fetched_policy = bucket.get_iam_policy(requested_policy_version=3)
    assert fetched_policy.bindings == returned_policy.bindings


def test_bucket_crud_w_requester_pays(storage_client, buckets_to_delete, user_project):
    bucket_name = _helpers.unique_name("w-requester-pays")
    created = _helpers.retry_429_503(storage_client.create_bucket)(
        bucket_name, requester_pays=True
    )
    buckets_to_delete.append(created)
    assert created.name == bucket_name
    assert created.requester_pays

    with_user_project = storage_client.bucket(bucket_name, user_project=user_project,)

    try:
        # Exercise 'buckets.get' w/ userProject.
        assert with_user_project.exists()
        with_user_project.reload()
        assert with_user_project.requester_pays

        # Exercise 'buckets.patch' w/ userProject.
        with_user_project.configure_website(
            main_page_suffix="index.html", not_found_page="404.html"
        )
        with_user_project.patch()
        expected_website = {"mainPageSuffix": "index.html", "notFoundPage": "404.html"}
        assert with_user_project._properties["website"] == expected_website

        # Exercise 'buckets.update' w/ userProject.
        new_labels = {"another-label": "another-value"}
        with_user_project.labels = new_labels
        with_user_project.update()
        assert with_user_project.labels == new_labels

    finally:
        # Exercise 'buckets.delete' w/ userProject.
        with_user_project.delete()
        buckets_to_delete.remove(created)


def test_bucket_acls_iam_w_user_project(
    storage_client, buckets_to_delete, user_project
):
    bucket_name = _helpers.unique_name("acl-w-user-project")
    created = _helpers.retry_429_503(storage_client.create_bucket)(
        bucket_name, requester_pays=True,
    )
    buckets_to_delete.append(created)

    with_user_project = storage_client.bucket(bucket_name, user_project=user_project)

    # Exercise bucket ACL w/ userProject
    acl = with_user_project.acl
    acl.reload()
    acl.all().grant_read()
    acl.save()
    assert "READER" in acl.all().get_roles()

    del acl.entities["allUsers"]
    acl.save()
    assert not acl.has_entity("allUsers")

    # Exercise default object ACL w/ userProject
    doa = with_user_project.default_object_acl
    doa.reload()
    doa.all().grant_read()
    doa.save()
    assert "READER" in doa.all().get_roles()

    # Exercise IAM w/ userProject
    test_permissions = ["storage.buckets.get"]
    found = with_user_project.test_iam_permissions(test_permissions)
    assert found == test_permissions

    policy = with_user_project.get_iam_policy()
    viewers = policy.setdefault("roles/storage.objectViewer", set())
    viewers.add(policy.all_users())
    with_user_project.set_iam_policy(policy)


def test_bucket_acls_w_metageneration_match(storage_client, buckets_to_delete):
    wrong_metageneration_number = 9
    bucket_name = _helpers.unique_name("acl-w-metageneration-match")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    # Exercise bucket ACL with metageneration match
    acl = bucket.acl
    acl.group("cloud-developer-relations@google.com").grant_read()
    bucket.reload()

    with pytest.raises(exceptions.PreconditionFailed):
        acl.save(if_metageneration_match=wrong_metageneration_number)
        assert (
            "READER"
            not in acl.group("cloud-developer-relations@google.com").get_roles()
        )

    acl.save(if_metageneration_match=bucket.metageneration)
    assert "READER" in acl.group("cloud-developer-relations@google.com").get_roles()

    # Exercise default object ACL w/ metageneration match
    doa = bucket.default_object_acl
    doa.group("cloud-developer-relations@google.com").grant_owner()
    bucket.reload()

    with pytest.raises(exceptions.PreconditionFailed):
        doa.save(if_metageneration_match=wrong_metageneration_number)
        assert (
            "OWNER" not in doa.group("cloud-developer-relations@google.com").get_roles()
        )

    doa.save(if_metageneration_match=bucket.metageneration)
    assert "OWNER" in doa.group("cloud-developer-relations@google.com").get_roles()


def test_bucket_copy_blob(
    storage_client, buckets_to_delete, blobs_to_delete, user_project,
):
    payload = b"DEADBEEF"
    bucket_name = _helpers.unique_name("copy-blob")
    created = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(created)
    assert created.name == bucket_name

    blob = created.blob("CloudLogo")
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    new_blob = _helpers.retry_bad_copy(created.copy_blob)(
        blob, created, "CloudLogoCopy"
    )
    blobs_to_delete.append(new_blob)

    copied_contents = new_blob.download_as_bytes()
    assert copied_contents == payload


def test_bucket_copy_blob_w_user_project(
    storage_client, buckets_to_delete, blobs_to_delete, user_project,
):
    payload = b"DEADBEEF"
    bucket_name = _helpers.unique_name("copy-w-requester-pays")
    created = _helpers.retry_429_503(storage_client.create_bucket)(
        bucket_name, requester_pays=True
    )
    buckets_to_delete.append(created)
    assert created.name == bucket_name
    assert created.requester_pays

    blob = created.blob("simple")
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    with_user_project = storage_client.bucket(bucket_name, user_project=user_project)

    new_blob = _helpers.retry_bad_copy(with_user_project.copy_blob)(
        blob, with_user_project, "simple-copy"
    )
    blobs_to_delete.append(new_blob)

    assert new_blob.download_as_bytes() == payload


def test_bucket_copy_blob_w_generation_match(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    payload = b"DEADBEEF"
    bucket_name = _helpers.unique_name("generation-match")
    created = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(created)
    assert created.name == bucket_name

    blob = created.blob("simple")
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    dest_bucket = storage_client.bucket(bucket_name)

    new_blob = dest_bucket.copy_blob(
        blob, dest_bucket, "simple-copy", if_source_generation_match=blob.generation,
    )
    blobs_to_delete.append(new_blob)

    assert new_blob.download_as_bytes() == payload


def test_bucket_copy_blob_w_metageneration_match(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    payload = b"DEADBEEF"
    bucket_name = _helpers.unique_name("generation-match")
    created = _helpers.retry_429_503(storage_client.create_bucket)(
        bucket_name, requester_pays=True
    )
    buckets_to_delete.append(created)
    assert created.name == bucket_name

    blob = created.blob("simple")
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    dest_bucket = storage_client.bucket(bucket_name)

    new_blob = dest_bucket.copy_blob(
        blob,
        dest_bucket,
        "simple-copy",
        if_source_metageneration_match=blob.metageneration,
    )
    blobs_to_delete.append(new_blob)

    assert new_blob.download_as_bytes() == payload


def test_bucket_get_blob_with_user_project(
    storage_client, buckets_to_delete, blobs_to_delete, user_project,
):
    blob_name = "blob-name"
    payload = b"DEADBEEF"
    bucket_name = _helpers.unique_name("w-requester-pays")
    created = _helpers.retry_429_503(storage_client.create_bucket)(
        bucket_name, requester_pays=True
    )
    buckets_to_delete.append(created)
    assert created.name == bucket_name
    assert created.requester_pays

    with_user_project = storage_client.bucket(bucket_name, user_project=user_project)

    assert with_user_project.get_blob("nonesuch") is None

    to_add = created.blob(blob_name)
    to_add.upload_from_string(payload)
    blobs_to_delete.append(to_add)

    found = with_user_project.get_blob(blob_name)
    assert found.download_as_bytes() == payload


@_helpers.retry_failures
def test_bucket_list_blobs(listable_bucket, listable_filenames):
    all_blobs = list(listable_bucket.list_blobs())
    assert sorted(blob.name for blob in all_blobs) == sorted(listable_filenames)


@_helpers.retry_failures
def test_bucket_list_blobs_w_user_project(
    storage_client, listable_bucket, listable_filenames, user_project,
):
    with_user_project = storage_client.bucket(
        listable_bucket.name, user_project=user_project
    )
    all_blobs = list(with_user_project.list_blobs())
    assert sorted(blob.name for blob in all_blobs) == sorted(listable_filenames)


@_helpers.retry_failures
def test_bucket_list_blobs_paginated(listable_bucket, listable_filenames):
    truncation_size = 1
    count = len(listable_filenames) - truncation_size
    iterator = listable_bucket.list_blobs(max_results=count)
    page_iter = iterator.pages

    page1 = next(page_iter)
    blobs = list(page1)
    assert len(blobs) == count
    assert iterator.next_page_token is not None
    # Technically the iterator is exhausted.
    assert iterator.num_results == iterator.max_results
    # But we modify the iterator to continue paging after
    # artificially stopping after ``count`` items.
    iterator.max_results = None

    page2 = next(page_iter)
    last_blobs = list(page2)
    assert len(last_blobs) == truncation_size


@_helpers.retry_failures
def test_bucket_list_blobs_paginated_w_offset(listable_bucket, listable_filenames):
    truncation_size = 1
    inclusive_start_offset = listable_filenames[1]
    exclusive_end_offset = listable_filenames[-1]
    desired_files = listable_filenames[1:-1]
    count = len(desired_files) - truncation_size
    iterator = listable_bucket.list_blobs(
        max_results=count,
        start_offset=inclusive_start_offset,
        end_offset=exclusive_end_offset,
    )
    page_iter = iterator.pages

    page1 = next(page_iter)
    blobs = list(page1)
    assert len(blobs) == count
    assert blobs[0].name == desired_files[0]
    assert iterator.next_page_token is not None
    # Technically the iterator is exhausted.
    assert iterator.num_results == iterator.max_results
    # But we modify the iterator to continue paging after
    # artificially stopping after ``count`` items.
    iterator.max_results = None

    page2 = next(page_iter)
    last_blobs = list(page2)
    assert len(last_blobs) == truncation_size
    assert last_blobs[-1].name == desired_files[-1]


@_helpers.retry_failures
def test_blob_exists_hierarchy(hierarchy_bucket, hierarchy_filenames):
    for filename in hierarchy_filenames:
        blob = hierarchy_bucket.blob(filename)
        assert blob.exists()


@_helpers.retry_failures
def test_bucket_list_blobs_hierarchy_root_level(hierarchy_bucket, hierarchy_filenames):
    expected_names = ["file01.txt"]
    expected_prefixes = set(["parent/"])

    iterator = hierarchy_bucket.list_blobs(delimiter="/")
    page = next(iterator.pages)
    blobs = list(page)

    assert [blob.name for blob in blobs] == expected_names
    assert iterator.next_page_token is None
    assert iterator.prefixes == expected_prefixes


@_helpers.retry_failures
def test_bucket_list_blobs_hierarchy_first_level(hierarchy_bucket, hierarchy_filenames):
    expected_names = ["parent/", "parent/file11.txt"]
    expected_prefixes = set(["parent/child/"])

    iterator = hierarchy_bucket.list_blobs(delimiter="/", prefix="parent/")
    page = next(iterator.pages)
    blobs = list(page)

    assert [blob.name for blob in blobs] == expected_names
    assert iterator.next_page_token is None
    assert iterator.prefixes == expected_prefixes


@_helpers.retry_failures
def test_bucket_list_blobs_hierarchy_second_level(
    hierarchy_bucket, hierarchy_filenames
):
    expected_names = ["parent/child/file21.txt", "parent/child/file22.txt"]
    expected_prefixes = set(["parent/child/grand/", "parent/child/other/"])

    iterator = hierarchy_bucket.list_blobs(delimiter="/", prefix="parent/child/")
    page = next(iterator.pages)
    blobs = list(page)
    assert [blob.name for blob in blobs] == expected_names
    assert iterator.next_page_token is None
    assert iterator.prefixes == expected_prefixes


@_helpers.retry_failures
def test_bucket_list_blobs_hierarchy_third_level(hierarchy_bucket, hierarchy_filenames):
    # Pseudo-hierarchy can be arbitrarily deep, subject to the limit
    # of 1024 characters in the UTF-8 encoded name:
    # https://cloud.google.com/storage/docs/bucketnaming#objectnames
    # Exercise a layer deeper to illustrate this.
    expected_names = ["parent/child/grand/file31.txt"]
    expected_prefixes = set()

    iterator = hierarchy_bucket.list_blobs(delimiter="/", prefix="parent/child/grand/")
    page = next(iterator.pages)
    blobs = list(page)

    assert [blob.name for blob in blobs] == expected_names
    assert iterator.next_page_token is None
    assert iterator.prefixes == expected_prefixes


@_helpers.retry_failures
def test_bucket_list_blobs_hierarchy_w_include_trailing_delimiter(
    hierarchy_bucket, hierarchy_filenames,
):
    expected_names = ["file01.txt", "parent/"]
    expected_prefixes = set(["parent/"])

    iterator = hierarchy_bucket.list_blobs(
        delimiter="/", include_trailing_delimiter=True
    )
    page = next(iterator.pages)
    blobs = list(page)

    assert [blob.name for blob in blobs] == expected_names
    assert iterator.next_page_token is None
    assert iterator.prefixes == expected_prefixes


def test_bucket_w_retention_period(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    period_secs = 10
    bucket_name = _helpers.unique_name("w-retention-period")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    bucket.retention_period = period_secs
    bucket.default_event_based_hold = False
    bucket.patch()

    assert bucket.retention_period == period_secs
    assert isinstance(bucket.retention_policy_effective_time, datetime.datetime)
    assert not bucket.default_event_based_hold
    assert not bucket.retention_policy_locked

    blob_name = "test-blob"
    payload = b"DEADBEEF"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload)

    blobs_to_delete.append(blob)

    other = bucket.get_blob(blob_name)

    assert not other.event_based_hold
    assert not other.temporary_hold
    assert isinstance(other.retention_expiration_time, datetime.datetime)

    with pytest.raises(exceptions.Forbidden):
        other.delete()

    bucket.retention_period = None
    bucket.patch()

    assert bucket.retention_period is None
    assert bucket.retention_policy_effective_time is None
    assert not bucket.default_event_based_hold
    assert not bucket.retention_policy_locked

    _helpers.retry_no_event_based_hold(other.reload)()

    assert not other.event_based_hold
    assert not other.temporary_hold
    assert other.retention_expiration_time is None

    other.delete()
    blobs_to_delete.pop()


def test_bucket_w_default_event_based_hold(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    bucket_name = _helpers.unique_name("w-def-ebh")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    bucket.default_event_based_hold = True
    bucket.patch()

    assert bucket.default_event_based_hold
    assert bucket.retention_period is None
    assert bucket.retention_policy_effective_time is None
    assert not bucket.retention_policy_locked

    blob_name = "test-blob"
    payload = b"DEADBEEF"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload)

    blobs_to_delete.append(blob)

    other = bucket.get_blob(blob_name)

    assert other.event_based_hold
    assert not other.temporary_hold
    assert other.retention_expiration_time is None

    with pytest.raises(exceptions.Forbidden):
        other.delete()

    other.event_based_hold = False
    other.patch()
    other.delete()

    bucket.default_event_based_hold = False
    bucket.patch()

    assert not bucket.default_event_based_hold
    assert bucket.retention_period is None
    assert bucket.retention_policy_effective_time is None
    assert not bucket.retention_policy_locked

    blob.upload_from_string(payload)

    # https://github.com/googleapis/python-storage/issues/435
    if blob.event_based_hold:
        _helpers.retry_no_event_based_hold(blob.reload)()

    assert not blob.event_based_hold
    assert not blob.temporary_hold
    assert blob.retention_expiration_time is None

    blob.delete()
    blobs_to_delete.pop()


def test_blob_w_temporary_hold(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    bucket_name = _helpers.unique_name("w-tmp-hold")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    blob_name = "test-blob"
    payload = b"DEADBEEF"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload)

    blobs_to_delete.append(blob)

    other = bucket.get_blob(blob_name)
    other.temporary_hold = True
    other.patch()

    assert other.temporary_hold
    assert not other.event_based_hold
    assert other.retention_expiration_time is None

    with pytest.raises(exceptions.Forbidden):
        other.delete()

    other.temporary_hold = False
    other.patch()

    other.delete()
    blobs_to_delete.pop()


def test_bucket_lock_retention_policy(
    storage_client, buckets_to_delete,
):
    period_secs = 10
    bucket_name = _helpers.unique_name("loc-ret-policy")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    bucket.retention_period = period_secs
    bucket.patch()

    assert bucket.retention_period == period_secs
    assert isinstance(bucket.retention_policy_effective_time, datetime.datetime)
    assert not bucket.default_event_based_hold
    assert not bucket.retention_policy_locked

    bucket.lock_retention_policy()

    bucket.reload()
    assert bucket.retention_policy_locked

    bucket.retention_period = None
    with pytest.raises(exceptions.Forbidden):
        bucket.patch()


def test_new_bucket_w_ubla(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    bucket_name = _helpers.unique_name("new-w-ubla")
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    _helpers.retry_429_503(bucket.create)()
    buckets_to_delete.append(bucket)

    bucket_acl = bucket.acl
    with pytest.raises(exceptions.BadRequest):
        bucket_acl.reload()

    bucket_acl.loaded = True  # Fake that we somehow loaded the ACL
    bucket_acl.group("cloud-developer-relations@google.com").grant_read()
    with pytest.raises(exceptions.BadRequest):
        bucket_acl.save()

    blob_name = "my-blob.txt"
    blob = bucket.blob(blob_name)
    payload = b"DEADBEEF"
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    found = bucket.get_blob(blob_name)
    assert found.download_as_bytes() == payload

    blob_acl = blob.acl
    with pytest.raises(exceptions.BadRequest):
        blob_acl.reload()

    blob_acl.loaded = True  # Fake that we somehow loaded the ACL
    blob_acl.group("cloud-developer-relations@google.com").grant_read()
    with pytest.raises(exceptions.BadRequest):
        blob_acl.save()


def test_ubla_set_unset_preserves_acls(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    bucket_name = _helpers.unique_name("ubla-acls")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    blob_name = "my-blob.txt"
    blob = bucket.blob(blob_name)
    payload = b"DEADBEEF"
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    # Preserve ACLs before setting UBLA
    bucket_acl_before = list(bucket.acl)
    blob_acl_before = list(bucket.acl)

    # Set UBLA
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()

    assert bucket.iam_configuration.uniform_bucket_level_access_enabled

    # While UBLA is set, cannot get / set ACLs
    with pytest.raises(exceptions.BadRequest):
        bucket.acl.reload()

    # Clear UBLA
    bucket.iam_configuration.uniform_bucket_level_access_enabled = False
    bucket.patch()

    # Query ACLs after clearing UBLA
    bucket.acl.reload()
    bucket_acl_after = list(bucket.acl)
    blob.acl.reload()
    blob_acl_after = list(bucket.acl)

    assert bucket_acl_before == bucket_acl_after
    assert blob_acl_before == blob_acl_after


def test_new_bucket_created_w_inherited_pap(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    from google.cloud.storage import constants

    bucket_name = _helpers.unique_name("new-w-pap-inherited")
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.create()
    buckets_to_delete.append(bucket)

    # TODO: Remove unspecified after changeover is complete
    assert bucket.iam_configuration.public_access_prevention in [
        constants.PUBLIC_ACCESS_PREVENTION_UNSPECIFIED,
        constants.PUBLIC_ACCESS_PREVENTION_INHERITED,
    ]

    bucket.iam_configuration.public_access_prevention = (
        constants.PUBLIC_ACCESS_PREVENTION_ENFORCED
    )
    bucket.patch()
    assert (
        bucket.iam_configuration.public_access_prevention
        == constants.PUBLIC_ACCESS_PREVENTION_ENFORCED
    )
    assert bucket.iam_configuration.uniform_bucket_level_access_enabled

    bucket.iam_configuration.uniform_bucket_level_access_enabled = False
    bucket.patch()
    assert (
        bucket.iam_configuration.public_access_prevention
        == constants.PUBLIC_ACCESS_PREVENTION_ENFORCED
    )

    with pytest.raises(exceptions.BadRequest):
        bucket.iam_configuration.public_access_prevention = "unexpected value"
        bucket.patch()

    with pytest.raises(exceptions.PreconditionFailed):
        bucket.make_public()

    blob_name = "my-blob.txt"
    blob = bucket.blob(blob_name)
    payload = b"DEADBEEF"
    blob.upload_from_string(payload)

    with pytest.raises(exceptions.PreconditionFailed):
        blob.make_public()


@pytest.mark.skip(reason="Unspecified PAP is changing to inherited")
def test_new_bucket_created_w_enforced_pap(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    from google.cloud.storage import constants

    bucket_name = _helpers.unique_name("new-w-pap-enforced")
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.public_access_prevention = (
        constants.PUBLIC_ACCESS_PREVENTION_ENFORCED
    )
    bucket.create()
    buckets_to_delete.append(bucket)

    assert (
        bucket.iam_configuration.public_access_prevention
        == constants.PUBLIC_ACCESS_PREVENTION_ENFORCED
    )

    bucket.iam_configuration.public_access_prevention = (
        constants.PUBLIC_ACCESS_PREVENTION_INHERITED
    )
    bucket.patch()

    # TODO: Remove unspecified after changeover is complete
    assert bucket.iam_configuration.public_access_prevention in [
        constants.PUBLIC_ACCESS_PREVENTION_UNSPECIFIED,
        constants.PUBLIC_ACCESS_PREVENTION_INHERITED,
    ]
    assert not bucket.iam_configuration.uniform_bucket_level_access_enabled


def test_new_bucket_with_rpo(
    storage_client, buckets_to_delete, blobs_to_delete,
):
    from google.cloud.storage import constants

    bucket_name = _helpers.unique_name("new-w-turbo-replication")
    bucket = storage_client.create_bucket(bucket_name, location="NAM4")
    buckets_to_delete.append(bucket)

    assert bucket.rpo == constants.RPO_DEFAULT

    bucket.rpo = constants.RPO_ASYNC_TURBO
    bucket.patch()

    bucket_from_server = storage_client.get_bucket(bucket_name)

    assert bucket_from_server.rpo == constants.RPO_ASYNC_TURBO
