# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.dlp_v2.types import dlp
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dlp",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DlpServiceTransport(abc.ABC):
    """Abstract transport class for DlpService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "dlp.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.inspect_content: gapic_v1.method.wrap_method(
                self.inspect_content,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.redact_image: gapic_v1.method.wrap_method(
                self.redact_image,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.deidentify_content: gapic_v1.method.wrap_method(
                self.deidentify_content,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.reidentify_content: gapic_v1.method.wrap_method(
                self.reidentify_content,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_info_types: gapic_v1.method.wrap_method(
                self.list_info_types,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.create_inspect_template: gapic_v1.method.wrap_method(
                self.create_inspect_template,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.update_inspect_template: gapic_v1.method.wrap_method(
                self.update_inspect_template,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.get_inspect_template: gapic_v1.method.wrap_method(
                self.get_inspect_template,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_inspect_templates: gapic_v1.method.wrap_method(
                self.list_inspect_templates,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.delete_inspect_template: gapic_v1.method.wrap_method(
                self.delete_inspect_template,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.create_deidentify_template: gapic_v1.method.wrap_method(
                self.create_deidentify_template,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.update_deidentify_template: gapic_v1.method.wrap_method(
                self.update_deidentify_template,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.get_deidentify_template: gapic_v1.method.wrap_method(
                self.get_deidentify_template,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_deidentify_templates: gapic_v1.method.wrap_method(
                self.list_deidentify_templates,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.delete_deidentify_template: gapic_v1.method.wrap_method(
                self.delete_deidentify_template,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.create_job_trigger: gapic_v1.method.wrap_method(
                self.create_job_trigger, default_timeout=300.0, client_info=client_info,
            ),
            self.update_job_trigger: gapic_v1.method.wrap_method(
                self.update_job_trigger, default_timeout=300.0, client_info=client_info,
            ),
            self.hybrid_inspect_job_trigger: gapic_v1.method.wrap_method(
                self.hybrid_inspect_job_trigger,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.get_job_trigger: gapic_v1.method.wrap_method(
                self.get_job_trigger,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_job_triggers: gapic_v1.method.wrap_method(
                self.list_job_triggers,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.delete_job_trigger: gapic_v1.method.wrap_method(
                self.delete_job_trigger,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.activate_job_trigger: gapic_v1.method.wrap_method(
                self.activate_job_trigger,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.create_dlp_job: gapic_v1.method.wrap_method(
                self.create_dlp_job, default_timeout=300.0, client_info=client_info,
            ),
            self.list_dlp_jobs: gapic_v1.method.wrap_method(
                self.list_dlp_jobs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.get_dlp_job: gapic_v1.method.wrap_method(
                self.get_dlp_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.delete_dlp_job: gapic_v1.method.wrap_method(
                self.delete_dlp_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.cancel_dlp_job: gapic_v1.method.wrap_method(
                self.cancel_dlp_job, default_timeout=300.0, client_info=client_info,
            ),
            self.create_stored_info_type: gapic_v1.method.wrap_method(
                self.create_stored_info_type,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.update_stored_info_type: gapic_v1.method.wrap_method(
                self.update_stored_info_type,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.get_stored_info_type: gapic_v1.method.wrap_method(
                self.get_stored_info_type,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.list_stored_info_types: gapic_v1.method.wrap_method(
                self.list_stored_info_types,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.delete_stored_info_type: gapic_v1.method.wrap_method(
                self.delete_stored_info_type,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.hybrid_inspect_dlp_job: gapic_v1.method.wrap_method(
                self.hybrid_inspect_dlp_job,
                default_timeout=300.0,
                client_info=client_info,
            ),
            self.finish_dlp_job: gapic_v1.method.wrap_method(
                self.finish_dlp_job, default_timeout=300.0, client_info=client_info,
            ),
        }

    @property
    def inspect_content(
        self,
    ) -> typing.Callable[
        [dlp.InspectContentRequest],
        typing.Union[
            dlp.InspectContentResponse, typing.Awaitable[dlp.InspectContentResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def redact_image(
        self,
    ) -> typing.Callable[
        [dlp.RedactImageRequest],
        typing.Union[
            dlp.RedactImageResponse, typing.Awaitable[dlp.RedactImageResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def deidentify_content(
        self,
    ) -> typing.Callable[
        [dlp.DeidentifyContentRequest],
        typing.Union[
            dlp.DeidentifyContentResponse,
            typing.Awaitable[dlp.DeidentifyContentResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def reidentify_content(
        self,
    ) -> typing.Callable[
        [dlp.ReidentifyContentRequest],
        typing.Union[
            dlp.ReidentifyContentResponse,
            typing.Awaitable[dlp.ReidentifyContentResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_info_types(
        self,
    ) -> typing.Callable[
        [dlp.ListInfoTypesRequest],
        typing.Union[
            dlp.ListInfoTypesResponse, typing.Awaitable[dlp.ListInfoTypesResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_inspect_template(
        self,
    ) -> typing.Callable[
        [dlp.CreateInspectTemplateRequest],
        typing.Union[dlp.InspectTemplate, typing.Awaitable[dlp.InspectTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def update_inspect_template(
        self,
    ) -> typing.Callable[
        [dlp.UpdateInspectTemplateRequest],
        typing.Union[dlp.InspectTemplate, typing.Awaitable[dlp.InspectTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def get_inspect_template(
        self,
    ) -> typing.Callable[
        [dlp.GetInspectTemplateRequest],
        typing.Union[dlp.InspectTemplate, typing.Awaitable[dlp.InspectTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def list_inspect_templates(
        self,
    ) -> typing.Callable[
        [dlp.ListInspectTemplatesRequest],
        typing.Union[
            dlp.ListInspectTemplatesResponse,
            typing.Awaitable[dlp.ListInspectTemplatesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_inspect_template(
        self,
    ) -> typing.Callable[
        [dlp.DeleteInspectTemplateRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_deidentify_template(
        self,
    ) -> typing.Callable[
        [dlp.CreateDeidentifyTemplateRequest],
        typing.Union[dlp.DeidentifyTemplate, typing.Awaitable[dlp.DeidentifyTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def update_deidentify_template(
        self,
    ) -> typing.Callable[
        [dlp.UpdateDeidentifyTemplateRequest],
        typing.Union[dlp.DeidentifyTemplate, typing.Awaitable[dlp.DeidentifyTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def get_deidentify_template(
        self,
    ) -> typing.Callable[
        [dlp.GetDeidentifyTemplateRequest],
        typing.Union[dlp.DeidentifyTemplate, typing.Awaitable[dlp.DeidentifyTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def list_deidentify_templates(
        self,
    ) -> typing.Callable[
        [dlp.ListDeidentifyTemplatesRequest],
        typing.Union[
            dlp.ListDeidentifyTemplatesResponse,
            typing.Awaitable[dlp.ListDeidentifyTemplatesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_deidentify_template(
        self,
    ) -> typing.Callable[
        [dlp.DeleteDeidentifyTemplateRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.CreateJobTriggerRequest],
        typing.Union[dlp.JobTrigger, typing.Awaitable[dlp.JobTrigger]],
    ]:
        raise NotImplementedError()

    @property
    def update_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.UpdateJobTriggerRequest],
        typing.Union[dlp.JobTrigger, typing.Awaitable[dlp.JobTrigger]],
    ]:
        raise NotImplementedError()

    @property
    def hybrid_inspect_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.HybridInspectJobTriggerRequest],
        typing.Union[
            dlp.HybridInspectResponse, typing.Awaitable[dlp.HybridInspectResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.GetJobTriggerRequest],
        typing.Union[dlp.JobTrigger, typing.Awaitable[dlp.JobTrigger]],
    ]:
        raise NotImplementedError()

    @property
    def list_job_triggers(
        self,
    ) -> typing.Callable[
        [dlp.ListJobTriggersRequest],
        typing.Union[
            dlp.ListJobTriggersResponse, typing.Awaitable[dlp.ListJobTriggersResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.DeleteJobTriggerRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def activate_job_trigger(
        self,
    ) -> typing.Callable[
        [dlp.ActivateJobTriggerRequest],
        typing.Union[dlp.DlpJob, typing.Awaitable[dlp.DlpJob]],
    ]:
        raise NotImplementedError()

    @property
    def create_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.CreateDlpJobRequest],
        typing.Union[dlp.DlpJob, typing.Awaitable[dlp.DlpJob]],
    ]:
        raise NotImplementedError()

    @property
    def list_dlp_jobs(
        self,
    ) -> typing.Callable[
        [dlp.ListDlpJobsRequest],
        typing.Union[
            dlp.ListDlpJobsResponse, typing.Awaitable[dlp.ListDlpJobsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.GetDlpJobRequest], typing.Union[dlp.DlpJob, typing.Awaitable[dlp.DlpJob]]
    ]:
        raise NotImplementedError()

    @property
    def delete_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.DeleteDlpJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.CancelDlpJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_stored_info_type(
        self,
    ) -> typing.Callable[
        [dlp.CreateStoredInfoTypeRequest],
        typing.Union[dlp.StoredInfoType, typing.Awaitable[dlp.StoredInfoType]],
    ]:
        raise NotImplementedError()

    @property
    def update_stored_info_type(
        self,
    ) -> typing.Callable[
        [dlp.UpdateStoredInfoTypeRequest],
        typing.Union[dlp.StoredInfoType, typing.Awaitable[dlp.StoredInfoType]],
    ]:
        raise NotImplementedError()

    @property
    def get_stored_info_type(
        self,
    ) -> typing.Callable[
        [dlp.GetStoredInfoTypeRequest],
        typing.Union[dlp.StoredInfoType, typing.Awaitable[dlp.StoredInfoType]],
    ]:
        raise NotImplementedError()

    @property
    def list_stored_info_types(
        self,
    ) -> typing.Callable[
        [dlp.ListStoredInfoTypesRequest],
        typing.Union[
            dlp.ListStoredInfoTypesResponse,
            typing.Awaitable[dlp.ListStoredInfoTypesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_stored_info_type(
        self,
    ) -> typing.Callable[
        [dlp.DeleteStoredInfoTypeRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def hybrid_inspect_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.HybridInspectDlpJobRequest],
        typing.Union[
            dlp.HybridInspectResponse, typing.Awaitable[dlp.HybridInspectResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def finish_dlp_job(
        self,
    ) -> typing.Callable[
        [dlp.FinishDlpJobRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()


__all__ = ("DlpServiceTransport",)
