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

from google.cloud.oslogin_v1 import common  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.oslogin.v1",
    manifest={
        "LoginProfile",
        "DeletePosixAccountRequest",
        "DeleteSshPublicKeyRequest",
        "GetLoginProfileRequest",
        "GetSshPublicKeyRequest",
        "ImportSshPublicKeyRequest",
        "ImportSshPublicKeyResponse",
        "UpdateSshPublicKeyRequest",
    },
)


class LoginProfile(proto.Message):
    r"""The user profile information used for logging in to a virtual
    machine on Google Compute Engine.

    Attributes:
        name (str):
            Required. A unique user ID.
        posix_accounts (Sequence[google.cloud.oslogin.v1.common.PosixAccount]):
            The list of POSIX accounts associated with
            the user.
        ssh_public_keys (Sequence[google.cloud.oslogin_v1.types.LoginProfile.SshPublicKeysEntry]):
            A map from SSH public key fingerprint to the
            associated key object.
    """

    name = proto.Field(proto.STRING, number=1,)
    posix_accounts = proto.RepeatedField(
        proto.MESSAGE, number=2, message=common.PosixAccount,
    )
    ssh_public_keys = proto.MapField(
        proto.STRING, proto.MESSAGE, number=3, message=common.SshPublicKey,
    )


class DeletePosixAccountRequest(proto.Message):
    r"""A request message for deleting a POSIX account entry.

    Attributes:
        name (str):
            Required. A reference to the POSIX account to update. POSIX
            accounts are identified by the project ID they are
            associated with. A reference to the POSIX account is in
            format ``users/{user}/projects/{project}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteSshPublicKeyRequest(proto.Message):
    r"""A request message for deleting an SSH public key.

    Attributes:
        name (str):
            Required. The fingerprint of the public key to update.
            Public keys are identified by their SHA-256 fingerprint. The
            fingerprint of the public key is in format
            ``users/{user}/sshPublicKeys/{fingerprint}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetLoginProfileRequest(proto.Message):
    r"""A request message for retrieving the login profile
    information for a user.

    Attributes:
        name (str):
            Required. The unique ID for the user in format
            ``users/{user}``.
        project_id (str):
            The project ID of the Google Cloud Platform
            project.
        system_id (str):
            A system ID for filtering the results of the
            request.
    """

    name = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)
    system_id = proto.Field(proto.STRING, number=3,)


class GetSshPublicKeyRequest(proto.Message):
    r"""A request message for retrieving an SSH public key.

    Attributes:
        name (str):
            Required. The fingerprint of the public key to retrieve.
            Public keys are identified by their SHA-256 fingerprint. The
            fingerprint of the public key is in format
            ``users/{user}/sshPublicKeys/{fingerprint}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ImportSshPublicKeyRequest(proto.Message):
    r"""A request message for importing an SSH public key.

    Attributes:
        parent (str):
            Required. The unique ID for the user in format
            ``users/{user}``.
        ssh_public_key (google.cloud.oslogin.v1.common.SshPublicKey):
            Optional. The SSH public key and expiration
            time.
        project_id (str):
            The project ID of the Google Cloud Platform
            project.
    """

    parent = proto.Field(proto.STRING, number=1,)
    ssh_public_key = proto.Field(proto.MESSAGE, number=2, message=common.SshPublicKey,)
    project_id = proto.Field(proto.STRING, number=3,)


class ImportSshPublicKeyResponse(proto.Message):
    r"""A response message for importing an SSH public key.

    Attributes:
        login_profile (google.cloud.oslogin_v1.types.LoginProfile):
            The login profile information for the user.
    """

    login_profile = proto.Field(proto.MESSAGE, number=1, message="LoginProfile",)


class UpdateSshPublicKeyRequest(proto.Message):
    r"""A request message for updating an SSH public key.

    Attributes:
        name (str):
            Required. The fingerprint of the public key to update.
            Public keys are identified by their SHA-256 fingerprint. The
            fingerprint of the public key is in format
            ``users/{user}/sshPublicKeys/{fingerprint}``.
        ssh_public_key (google.cloud.oslogin.v1.common.SshPublicKey):
            Required. The SSH public key and expiration
            time.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Mask to control which fields get updated.
            Updates all if not present.
    """

    name = proto.Field(proto.STRING, number=1,)
    ssh_public_key = proto.Field(proto.MESSAGE, number=2, message=common.SshPublicKey,)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
