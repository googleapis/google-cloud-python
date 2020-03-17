# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Wrappers for protocol buffer enum types."""

import enum


class Code(enum.IntEnum):
    """
    Specifies a service that was configured for Cloud Audit Logging. For
    example, ``storage.googleapis.com``, ``cloudsql.googleapis.com``.
    ``allServices`` is a special value that covers all services. Required

    Attributes:
      OK (int): Not an error; returned on success

      HTTP Mapping: 200 OK
      CANCELLED (int): The operation was cancelled, typically by the caller.

      HTTP Mapping: 499 Client Closed Request
      UNKNOWN (int): The service account impersonation analysis if
      ``AnalyzeIamPolicyRequest.analyze_service_account_impersonation`` is
      enabled.
      INVALID_ARGUMENT (int): A URL/resource name that uniquely identifies the type of the
      serialized protocol buffer message. This string must contain at least
      one "/" character. The last segment of the URL's path must represent the
      fully qualified name of the type (as in
      ``path/google.protobuf.Duration``). The name should be in a canonical
      form (e.g., leading "." is not accepted).

      In practice, teams usually precompile into the binary all types that
      they expect it to use in the context of Any. However, for URLs which use
      the scheme ``http``, ``https``, or no scheme, one can optionally set up
      a type server that maps type URLs to message definitions as follows:

      -  If no scheme is provided, ``https`` is assumed.
      -  An HTTP GET on the URL must yield a ``google.protobuf.Type`` value in
         binary format, or produce an error.
      -  Applications are allowed to cache lookup results based on the URL, or
         have them precompiled into a binary to avoid any lookup. Therefore,
         binary compatibility needs to be preserved on changes to types. (Use
         versioned type names to manage breaking changes.)

      Note: this functionality is not currently available in the official
      protobuf release, and it is not used for type URLs beginning with
      type.googleapis.com.

      Schemes other than ``http``, ``https`` (or the empty scheme) might be
      used with implementation specific semantics.
      DEADLINE_EXCEEDED (int): The deadline expired before the operation could complete. For operations
      that change the state of the system, this error may be returned
      even if the operation has completed successfully.  For example, a
      successful response from a server could have been delayed long
      enough for the deadline to expire.

      HTTP Mapping: 504 Gateway Timeout
      NOT_FOUND (int): A response message for ``AssetService.AnalyzeIamPolicy``.
      ALREADY_EXISTS (int): The entity that a client attempted to create (e.g., file or directory)
      already exists.

      HTTP Mapping: 409 Conflict
      PERMISSION_DENIED (int): Required. The message name of the primary return type for this
      long-running operation. This type will be used to deserialize the LRO's
      response.

      If the response is in a different package from the rpc, a
      fully-qualified message name must be used (e.g.
      ``google.protobuf.Struct``).

      Note: Altering this value constitutes a breaking change.
      UNAUTHENTICATED (int): The request does not have valid authentication credentials for the
      operation.

      HTTP Mapping: 401 Unauthorized
      RESOURCE_EXHAUSTED (int): Some resource has been exhausted, perhaps a per-user quota, or
      perhaps the entire file system is out of space.

      HTTP Mapping: 429 Too Many Requests
      FAILED_PRECONDITION (int): A single identity that is exempted from "data access" audit logging
      for the ``service`` specified above. Follows the same format of
      Binding.members.
      ABORTED (int): The export IAM policy analysis response. This message is returned by
      the ``google.longrunning.Operations.GetOperation`` method in the
      returned ``google.longrunning.Operation.response`` field.
      OUT_OF_RANGE (int): The custom pattern is used for specifying an HTTP method that is not
      included in the ``pattern`` field, such as HEAD, or "*" to leave the
      HTTP method unspecified for this rule. The wild-card rule is useful for
      services that provide content to Web (HTML) clients.
      UNIMPLEMENTED (int): The operation is not implemented or is not supported/enabled in this
      service.

      HTTP Mapping: 501 Not Implemented
      INTERNAL (int): Internal errors.  This means that some invariants expected by the
      underlying system have been broken.  This error code is reserved
      for serious errors.

      HTTP Mapping: 500 Internal Server Error
      UNAVAILABLE (int): Optional. If true, the resource section of the result will expand
      any resource attached to an IAM policy to include resources lower in the
      resource hierarchy.

      For example, if the request analyzes for which resources user A has
      permission P, and the results include an IAM policy with P on a GCP
      folder, the results will also include resources in that folder with
      permission P.

      If ``resource_selector`` is specified, the resource section of the
      result will be determined by the selector, and this flag will have no
      effect. Default is false.
      DATA_LOSS (int): Unrecoverable data loss or corruption.

      HTTP Mapping: 500 Internal Server Error
    """

    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    UNAUTHENTICATED = 16
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
