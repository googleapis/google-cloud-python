# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.cloud.notebooks_v1.types import event as gcn_event
from google.cloud.notebooks_v1.types import runtime as gcn_runtime


__protobuf__ = proto.module(
    package="google.cloud.notebooks.v1",
    manifest={
        "ListRuntimesRequest",
        "ListRuntimesResponse",
        "GetRuntimeRequest",
        "CreateRuntimeRequest",
        "DeleteRuntimeRequest",
        "StartRuntimeRequest",
        "StopRuntimeRequest",
        "SwitchRuntimeRequest",
        "ResetRuntimeRequest",
        "ReportRuntimeEventRequest",
    },
)


class ListRuntimesRequest(proto.Message):
    r"""Request for listing Managed Notebook Runtimes.

    Attributes:
        parent (str):
            Required. Format:
            ``parent=projects/{project_id}/locations/{location}``
        page_size (int):
            Maximum return size of the list call.
        page_token (str):
            A previous returned page token that can be
            used to continue listing from the last result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListRuntimesResponse(proto.Message):
    r"""Response for listing Managed Notebook Runtimes.

    Attributes:
        runtimes (Sequence[google.cloud.notebooks_v1.types.Runtime]):
            A list of returned Runtimes.
        next_page_token (str):
            Page token that can be used to continue
            listing from the last result in the next list
            call.
        unreachable (Sequence[str]):
            Locations that could not be reached. For example,
            ['us-west1', 'us-central1']. A ListRuntimesResponse will
            only contain either runtimes or unreachables,
    """

    @property
    def raw_page(self):
        return self

    runtimes = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gcn_runtime.Runtime,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetRuntimeRequest(proto.Message):
    r"""Request for getting a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateRuntimeRequest(proto.Message):
    r"""Request for creating a Managed Notebook Runtime.

    Attributes:
        parent (str):
            Required. Format:
            ``parent=projects/{project_id}/locations/{location}``
        runtime_id (str):
            Required. User-defined unique ID of this
            Runtime.
        runtime (google.cloud.notebooks_v1.types.Runtime):
            Required. The Runtime to be created.
    """

    parent = proto.Field(proto.STRING, number=1,)
    runtime_id = proto.Field(proto.STRING, number=2,)
    runtime = proto.Field(proto.MESSAGE, number=3, message=gcn_runtime.Runtime,)


class DeleteRuntimeRequest(proto.Message):
    r"""Request for deleting a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class StartRuntimeRequest(proto.Message):
    r"""Request for starting a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class StopRuntimeRequest(proto.Message):
    r"""Request for stopping a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class SwitchRuntimeRequest(proto.Message):
    r"""Request for switching a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
        machine_type (str):
            machine type.
        accelerator_config (google.cloud.notebooks_v1.types.RuntimeAcceleratorConfig):
            accelerator config.
    """

    name = proto.Field(proto.STRING, number=1,)
    machine_type = proto.Field(proto.STRING, number=2,)
    accelerator_config = proto.Field(
        proto.MESSAGE, number=3, message=gcn_runtime.RuntimeAcceleratorConfig,
    )


class ResetRuntimeRequest(proto.Message):
    r"""Request for reseting a Managed Notebook Runtime.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class ReportRuntimeEventRequest(proto.Message):
    r"""Request for reporting a Managed Notebook Event.

    Attributes:
        name (str):
            Required. Format:
            ``projects/{project_id}/locations/{location}/runtimes/{runtime_id}``
        vm_id (str):
            Required. The VM hardware token for
            authenticating the VM.
            https://cloud.google.com/compute/docs/instances/verifying-instance-identity
        event (google.cloud.notebooks_v1.types.Event):
            Required. The Event to be reported.
    """

    name = proto.Field(proto.STRING, number=1,)
    vm_id = proto.Field(proto.STRING, number=2,)
    event = proto.Field(proto.MESSAGE, number=3, message=gcn_event.Event,)


__all__ = tuple(sorted(__protobuf__.manifest))
