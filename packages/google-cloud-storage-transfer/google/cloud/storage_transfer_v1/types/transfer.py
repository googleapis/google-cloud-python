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

from google.cloud.storage_transfer_v1.types import transfer_types
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.storagetransfer.v1",
    manifest={
        "GetGoogleServiceAccountRequest",
        "CreateTransferJobRequest",
        "UpdateTransferJobRequest",
        "GetTransferJobRequest",
        "ListTransferJobsRequest",
        "ListTransferJobsResponse",
        "PauseTransferOperationRequest",
        "ResumeTransferOperationRequest",
        "RunTransferJobRequest",
    },
)


class GetGoogleServiceAccountRequest(proto.Message):
    r"""Request passed to GetGoogleServiceAccount.

    Attributes:
        project_id (str):
            Required. The ID of the Google Cloud Platform
            Console project that the Google service account
            is associated with.
    """

    project_id = proto.Field(proto.STRING, number=1,)


class CreateTransferJobRequest(proto.Message):
    r"""Request passed to CreateTransferJob.

    Attributes:
        transfer_job (google.cloud.storage_transfer_v1.types.TransferJob):
            Required. The job to create.
    """

    transfer_job = proto.Field(
        proto.MESSAGE, number=1, message=transfer_types.TransferJob,
    )


class UpdateTransferJobRequest(proto.Message):
    r"""Request passed to UpdateTransferJob.

    Attributes:
        job_name (str):
            Required. The name of job to update.
        project_id (str):
            Required. The ID of the Google Cloud Platform
            Console project that owns the job.
        transfer_job (google.cloud.storage_transfer_v1.types.TransferJob):
            Required. The job to update. ``transferJob`` is expected to
            specify only four fields:
            [description][google.storagetransfer.v1.TransferJob.description],
            [transfer_spec][google.storagetransfer.v1.TransferJob.transfer_spec],
            [notification_config][google.storagetransfer.v1.TransferJob.notification_config],
            and [status][google.storagetransfer.v1.TransferJob.status].
            An ``UpdateTransferJobRequest`` that specifies other fields
            are rejected with the error
            [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
            Updating a job status to
            [DELETED][google.storagetransfer.v1.TransferJob.Status.DELETED]
            requires ``storagetransfer.jobs.delete`` permissions.
        update_transfer_job_field_mask (google.protobuf.field_mask_pb2.FieldMask):
            The field mask of the fields in ``transferJob`` that are to
            be updated in this request. Fields in ``transferJob`` that
            can be updated are:
            [description][google.storagetransfer.v1.TransferJob.description],
            [transfer_spec][google.storagetransfer.v1.TransferJob.transfer_spec],
            [notification_config][google.storagetransfer.v1.TransferJob.notification_config],
            and [status][google.storagetransfer.v1.TransferJob.status].
            To update the ``transfer_spec`` of the job, a complete
            transfer specification must be provided. An incomplete
            specification missing any required fields is rejected with
            the error
            [INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
    """

    job_name = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)
    transfer_job = proto.Field(
        proto.MESSAGE, number=3, message=transfer_types.TransferJob,
    )
    update_transfer_job_field_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
    )


class GetTransferJobRequest(proto.Message):
    r"""Request passed to GetTransferJob.

    Attributes:
        job_name (str):
            Required.
            The job to get.
        project_id (str):
            Required. The ID of the Google Cloud Platform
            Console project that owns the job.
    """

    job_name = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)


class ListTransferJobsRequest(proto.Message):
    r"""``projectId``, ``jobNames``, and ``jobStatuses`` are query
    parameters that can be specified when listing transfer jobs.

    Attributes:
        filter (str):
            Required. A list of query parameters specified as JSON text
            in the form of:
            ``{"projectId":"my_project_id", "jobNames":["jobid1","jobid2",...], "jobStatuses":["status1","status2",...]}``

            Since ``jobNames`` and ``jobStatuses`` support multiple
            values, their values must be specified with array notation.
            ``projectId`` is required. ``jobNames`` and ``jobStatuses``
            are optional. The valid values for ``jobStatuses`` are
            case-insensitive:
            [ENABLED][google.storagetransfer.v1.TransferJob.Status.ENABLED],
            [DISABLED][google.storagetransfer.v1.TransferJob.Status.DISABLED],
            and
            [DELETED][google.storagetransfer.v1.TransferJob.Status.DELETED].
        page_size (int):
            The list page size. The max allowed value is
            256.
        page_token (str):
            The list page token.
    """

    filter = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=4,)
    page_token = proto.Field(proto.STRING, number=5,)


class ListTransferJobsResponse(proto.Message):
    r"""Response from ListTransferJobs.

    Attributes:
        transfer_jobs (Sequence[google.cloud.storage_transfer_v1.types.TransferJob]):
            A list of transfer jobs.
        next_page_token (str):
            The list next page token.
    """

    @property
    def raw_page(self):
        return self

    transfer_jobs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=transfer_types.TransferJob,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class PauseTransferOperationRequest(proto.Message):
    r"""Request passed to PauseTransferOperation.

    Attributes:
        name (str):
            Required. The name of the transfer operation.
    """

    name = proto.Field(proto.STRING, number=1,)


class ResumeTransferOperationRequest(proto.Message):
    r"""Request passed to ResumeTransferOperation.

    Attributes:
        name (str):
            Required. The name of the transfer operation.
    """

    name = proto.Field(proto.STRING, number=1,)


class RunTransferJobRequest(proto.Message):
    r"""Request passed to RunTransferJob.

    Attributes:
        job_name (str):
            Required. The name of the transfer job.
        project_id (str):
            Required. The ID of the Google Cloud Platform
            Console project that owns the transfer job.
    """

    job_name = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
