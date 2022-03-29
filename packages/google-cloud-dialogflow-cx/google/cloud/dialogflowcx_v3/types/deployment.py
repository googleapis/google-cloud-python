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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={
        "Deployment",
        "ListDeploymentsRequest",
        "ListDeploymentsResponse",
        "GetDeploymentRequest",
    },
)


class Deployment(proto.Message):
    r"""Represents an deployment in an environment. A deployment
    happens when a flow version configured to be active in the
    environment. You can configure running pre-deployment steps,
    e.g. running validation test cases, experiment auto-rollout,
    etc.

    Attributes:
        name (str):
            The name of the deployment.
            Format: projects/<Project
            ID>/locations/<Location ID>/agents/<Agent
            ID>/environments/<Environment
            ID>/deployments/<Deployment ID>.
        flow_version (str):
            The name of the flow version for this
            deployment. Format: projects/<Project
            ID>/locations/<Location ID>/agents/<Agent
            ID>/flows/<Flow ID>/versions/<Verion ID>.
        state (google.cloud.dialogflowcx_v3.types.Deployment.State):
            The current state of the deployment.
        result (google.cloud.dialogflowcx_v3.types.Deployment.Result):
            Result of the deployment.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Start time of this deployment.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End time of this deployment.
    """

    class State(proto.Enum):
        r"""The state of the deployment."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3

    class Result(proto.Message):
        r"""Result of the deployment.

        Attributes:
            deployment_test_results (Sequence[str]):
                Results of test cases running before the deployment. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/testCases/<TestCase ID>/results/<TestCaseResult ID>``.
            experiment (str):
                The name of the experiment triggered by this
                deployment. Format: projects/<Project
                ID>/locations/<Location ID>/agents/<Agent
                ID>/environments/<Environment
                ID>/experiments/<Experiment ID>.
        """

        deployment_test_results = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        experiment = proto.Field(
            proto.STRING,
            number=2,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    flow_version = proto.Field(
        proto.STRING,
        number=2,
    )
    state = proto.Field(
        proto.ENUM,
        number=3,
        enum=State,
    )
    result = proto.Field(
        proto.MESSAGE,
        number=4,
        message=Result,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class ListDeploymentsRequest(proto.Message):
    r"""The request message for
    [Deployments.ListDeployments][google.cloud.dialogflow.cx.v3.Deployments.ListDeployments].

    Attributes:
        parent (str):
            Required. The
            [Environment][google.cloud.dialogflow.cx.v3.Environment] to
            list all environments for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 20 and at most 100.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListDeploymentsResponse(proto.Message):
    r"""The response message for
    [Deployments.ListDeployments][google.cloud.dialogflow.cx.v3.Deployments.ListDeployments].

    Attributes:
        deployments (Sequence[google.cloud.dialogflowcx_v3.types.Deployment]):
            The list of deployments. There will be a maximum number of
            items returned based on the page_size field in the request.
            The list may in some cases be empty or contain fewer entries
            than page_size even if this isn't the last page.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    deployments = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Deployment",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDeploymentRequest(proto.Message):
    r"""The request message for
    [Deployments.GetDeployment][google.cloud.dialogflow.cx.v3.Deployments.GetDeployment].

    Attributes:
        name (str):
            Required. The name of the
            [Deployment][google.cloud.dialogflow.cx.v3.Deployment].
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/deployments/<Deployment ID>``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
