# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

import os
import pytest

from google.cloud import dlp_v2
from google.api_core import exceptions

from test_utils.vpcsc_config import vpcsc_config


_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy"


@pytest.fixture(scope="module")
def client():
    return dlp_v2.DlpServiceClient()


@pytest.fixture(scope="module")
def name_inside(client):
    return f"projects/{vpcsc_config.project_inside}"


@pytest.fixture(scope="module")
def name_outside(client):
    return f"projects/{vpcsc_config.project_outside}"


@pytest.fixture(scope="module")
def content_item():
    return dlp_v2.ContentItem(value="testing")


@pytest.fixture(scope="module")
def bytes_content_item():
    return dlp_v2.ByteContentItem(data=b"DEADBEEF")


@vpcsc_config.skip_unless_inside_vpcsc
def test_inspect_content_inside(client, name_inside, content_item):
    client.inspect_content(
        request={"parent": name_inside, "item": content_item}
    )  # no perms issue


@vpcsc_config.skip_unless_inside_vpcsc
def test_inspect_content_outside(client, name_outside, content_item):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.inspect_content(request={"parent": name_outside, "item": content_item})

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_redact_image_inside(client, name_inside, bytes_content_item):
    with pytest.raises(exceptions.InvalidArgument):  # no perms issue
        client.redact_image(
            request={"parent": name_inside, "byte_item": bytes_content_item}
        )


@vpcsc_config.skip_unless_inside_vpcsc
def test_redact_image_outside(client, name_outside, bytes_content_item):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.redact_image(
            request={"parent": name_outside, "byte_item": bytes_content_item}
        )

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_deidentify_content_inside(client, name_inside, content_item):
    with pytest.raises(exceptions.InvalidArgument):  # no perms issue
        client.deidentify_content(request={"parent": name_inside, "item": content_item})


@vpcsc_config.skip_unless_inside_vpcsc
def test_deidentify_content_outside(client, name_outside, content_item):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.deidentify_content(
            request={"parent": name_outside, "item": content_item}
        )

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_reidentify_content_inside(client, name_inside, content_item):
    with pytest.raises(exceptions.InvalidArgument):  # no perms issue
        client.reidentify_content(request={"parent": name_inside, "item": content_item})


@vpcsc_config.skip_unless_inside_vpcsc
def test_reidentify_content_outside(client, name_outside, content_item):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.reidentify_content(
            request={"parent": name_outside, "item": content_item}
        )

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def inspect_template_path_inside(client):
    inspect_template_id = 1234567
    return (
        f"projects/{vpcsc_config.project_inside}/inspectTemplates/{inspect_template_id}"
    )


@pytest.fixture(scope="module")
def inspect_template_path_outside(client):
    inspect_template_id = 1234567
    return f"projects/{vpcsc_config.project_outside}/inspectTemplates/{inspect_template_id}"


@pytest.fixture(scope="module")
def inspect_template():
    return dlp_v2.InspectTemplate()


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDInspectTemplate(object):
    @staticmethod
    def test_create_inspect_template_inside(client, name_inside, inspect_template):
        client.create_inspect_template(
            request={"parent": name_inside, "inspect_template": inspect_template}
        )  # no perms issue

    @staticmethod
    def test_create_inspect_template_outside(client, name_outside, inspect_template):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.create_inspect_template(
                request={"parent": name_outside, "inspect_template": inspect_template}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_inspect_templates_inside(client, name_inside):
        list(client.list_inspect_templates(request={"parent": name_inside}))

    @staticmethod
    def test_list_inspect_templates_outside(client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(client.list_inspect_templates(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_inspect_template_inside(client, inspect_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.update_inspect_template(
                request={"name": inspect_template_path_inside}
            )

    @staticmethod
    def test_update_inspect_template_outside(client, inspect_template_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.update_inspect_template(
                request={"name": inspect_template_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_inspect_template_inside(client, inspect_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.get_inspect_template(request={"name": inspect_template_path_inside})

    @staticmethod
    def test_get_inspect_template_outside(client, inspect_template_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.get_inspect_template(request={"name": inspect_template_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_inspect_template_inside(client, inspect_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.delete_inspect_template(
                request={"name": inspect_template_path_inside}
            )

    @staticmethod
    def test_delete_inspect_template_outside(client, inspect_template_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.delete_inspect_template(
                request={"name": inspect_template_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def deidentify_template_path_inside(client):
    deidentify_template_id = 1234567
    return f"projects/{vpcsc_config.project_inside}/deidentifyTemplates/{deidentify_template_id}"


@pytest.fixture(scope="module")
def deidentify_template_path_outside(client):
    deidentify_template_id = 1234567
    return f"projects/{vpcsc_config.project_outside}/deidentifyTemplates/{deidentify_template_id}"


@pytest.fixture(scope="module")
def deidentify_template():
    return dlp_v2.DeidentifyTemplate()


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDDeidentifyTemplate(object):
    @staticmethod
    def test_create_deidentify_template_inside(
        client, name_inside, deidentify_template
    ):
        client.create_deidentify_template(
            request={"parent": name_inside, "deidentify_template": deidentify_template}
        )

    @staticmethod
    def test_create_deidentify_template_outside(
        client, name_outside, deidentify_template
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.create_deidentify_template(
                request={
                    "parent": name_outside,
                    "deidentify_template": deidentify_template,
                }
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_deidentify_templates_inside(client, name_inside):
        list(client.list_deidentify_templates(request={"parent": name_inside}))

    @staticmethod
    def test_list_deidentify_templates_outside(client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(client.list_deidentify_templates(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_deidentify_template_inside(client, deidentify_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.update_deidentify_template(
                request={"name": deidentify_template_path_inside}
            )

    @staticmethod
    def test_update_deidentify_template_outside(
        client, deidentify_template_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.update_deidentify_template(
                request={"name": deidentify_template_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_deidentify_template_inside(client, deidentify_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.get_deidentify_template(
                request={"name": deidentify_template_path_inside}
            )

    @staticmethod
    def test_get_deidentify_template_outside(client, deidentify_template_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.get_deidentify_template(
                request={"name": deidentify_template_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_deidentify_template_inside(client, deidentify_template_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.delete_deidentify_template(
                request={"name": deidentify_template_path_inside}
            )

    @staticmethod
    def test_delete_deidentify_template_outside(
        client, deidentify_template_path_outside
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.delete_deidentify_template(
                request={"name": deidentify_template_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def job_path_inside(name_inside):
    job_id = 1234567
    return "{}/jobs/{}".format(name_inside, job_id)


@pytest.fixture(scope="module")
def job_path_outside(name_outside):
    job_id = 1234567
    return "{}/jobs/{}".format(name_outside, job_id)


@pytest.fixture(scope="module")
def inspect_job():
    return dlp_v2.InspectJobConfig()


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDDlpJob(object):
    @staticmethod
    def test_create_dlp_job_inside(client, name_inside, inspect_job):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.create_dlp_job(
                request={"parent": name_inside, "inspect_job": inspect_job}
            )

    @staticmethod
    def test_create_dlp_job_outside(client, name_outside, inspect_job):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.create_dlp_job(
                request={"parent": name_outside, "inspect_job": inspect_job}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_dlp_jobs_inside(client, name_inside):
        list(client.list_dlp_jobs(request={"parent": name_inside}))

    @staticmethod
    def test_list_dlp_jobs_outside(client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(client.list_dlp_jobs(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_dlp_job_inside(client, job_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.get_dlp_job(request={"name": job_path_inside})

    @staticmethod
    def test_get_dlp_job_outside(client, job_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.get_dlp_job(request={"name": job_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_dlp_job_inside(client, job_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.delete_dlp_job(request={"name": job_path_inside})

    @staticmethod
    def test_delete_dlp_job_outside(client, job_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.delete_dlp_job(request={"name": job_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_cancel_dlp_job_inside(client, job_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.cancel_dlp_job(request={"name": job_path_inside})

    @staticmethod
    def test_cancel_dlp_job_outside(client, job_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.cancel_dlp_job(request={"name": job_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def job_trigger_path_inside(client):
    job_trigger_id = 1234567
    return client.job_trigger_path(vpcsc_config.project_inside, job_trigger_id)


@pytest.fixture(scope="module")
def job_trigger_path_outside(client):
    job_trigger_id = 1234567
    return client.job_trigger_path(vpcsc_config.project_outside, job_trigger_id)


@pytest.fixture(scope="module")
def job_trigger():
    return dlp_v2.JobTrigger()


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDJobTrigger(object):
    @staticmethod
    def test_create_job_trigger_inside(client, name_inside, job_trigger):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.create_job_trigger(
                request={"parent": name_inside, "job_trigger": job_trigger}
            )

    @staticmethod
    def test_create_job_trigger_outside(client, name_outside, job_trigger):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.create_job_trigger(
                request={"parent": name_outside, "job_trigger": job_trigger}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_job_triggers_inside(client, name_inside):
        list(client.list_job_triggers(request={"parent": name_inside}))

    @staticmethod
    def test_list_job_triggers_outside(client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(client.list_job_triggers(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_job_trigger_inside(client, job_trigger_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.get_job_trigger(request={"name": job_trigger_path_inside})

    @staticmethod
    def test_get_job_trigger_outside(client, job_trigger_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.get_job_trigger(request={"name": job_trigger_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_job_trigger_inside(client, job_trigger_path_inside):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.update_job_trigger(request={"name": job_trigger_path_inside})

    @staticmethod
    def test_update_job_trigger_outside(client, job_trigger_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.update_job_trigger(request={"name": job_trigger_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_job_trigger_inside(client, job_trigger_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.delete_job_trigger(request={"name": job_trigger_path_inside})

    @staticmethod
    def test_delete_job_trigger_outside(client, job_trigger_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.delete_job_trigger(request={"name": job_trigger_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@pytest.fixture(scope="module")
def stored_info_type_path_inside(client):
    stored_info_type_id = 1234567
    return (
        f"projects/{vpcsc_config.project_inside}/storedInfoTypes/{stored_info_type_id}"
    )


@pytest.fixture(scope="module")
def stored_info_type_path_outside(client):
    stored_info_type_id = 1234567
    return (
        f"projects/{vpcsc_config.project_outside}/storedInfoTypes/{stored_info_type_id}"
    )


@pytest.fixture(scope="module")
def stored_info_type_config(client):
    return dlp_v2.StoredInfoTypeConfig()


@vpcsc_config.skip_unless_inside_vpcsc
class TestCRUDStoredInfoType(object):
    @staticmethod
    def test_create_stored_info_type_inside(
        client, name_inside, stored_info_type_config
    ):
        with pytest.raises(exceptions.InvalidArgument):  # no perms issue
            client.create_stored_info_type(
                request={"parent": name_inside, "config": stored_info_type_config}
            )

    @staticmethod
    def test_create_stored_info_type_outside(
        client, name_outside, stored_info_type_config
    ):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.create_stored_info_type(
                request={"parent": name_outside, "config": stored_info_type_config}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_list_stored_info_types_inside(client, name_inside):
        list(client.list_stored_info_types(request={"parent": name_inside}))

    @staticmethod
    def test_list_stored_info_types_outside(client, name_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(client.list_stored_info_types(request={"parent": name_outside}))

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_get_stored_info_type_inside(client, stored_info_type_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.get_stored_info_type(request={"name": stored_info_type_path_inside})

    @staticmethod
    def test_get_stored_info_type_outside(client, stored_info_type_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.get_stored_info_type(request={"name": stored_info_type_path_outside})

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_update_stored_info_type_inside(client, stored_info_type_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.update_stored_info_type(
                request={"name": stored_info_type_path_inside}
            )

    @staticmethod
    def test_update_stored_info_type_outside(client, stored_info_type_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.update_stored_info_type(
                request={"name": stored_info_type_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message

    @staticmethod
    def test_delete_stored_info_type_inside(client, stored_info_type_path_inside):
        with pytest.raises(exceptions.NotFound):  # no perms issue
            client.delete_stored_info_type(
                request={"name": stored_info_type_path_inside}
            )

    @staticmethod
    def test_delete_stored_info_type_outside(client, stored_info_type_path_outside):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            client.delete_stored_info_type(
                request={"name": stored_info_type_path_outside}
            )

        assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message
