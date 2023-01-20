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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.run_v2.types import task_template

__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "ExecutionTemplate",
    },
)


class ExecutionTemplate(proto.Message):
    r"""ExecutionTemplate describes the data an execution should have
    when created from a template.

    Attributes:
        labels (MutableMapping[str, str]):
            KRM-style labels for the resource.

            .. raw:: html

                <p>Cloud Run API v2 does not support labels with `run.googleapis.com`,
                `cloud.googleapis.com`, `serving.knative.dev`, or `autoscaling.knative.dev`
                namespaces, and they will be rejected. All system labels in v1 now have a
                corresponding field in v2 ExecutionTemplate.
        annotations (MutableMapping[str, str]):
            KRM-style annotations for the resource.

            .. raw:: html

                <p>Cloud Run API v2 does not support annotations with `run.googleapis.com`,
                `cloud.googleapis.com`, `serving.knative.dev`, or `autoscaling.knative.dev`
                namespaces, and they will be rejected. All system annotations in v1 now
                have a corresponding field in v2 ExecutionTemplate.
        parallelism (int):
            Specifies the maximum desired number of tasks the execution
            should run at given time. Must be <= task_count. When the
            job is run, if this field is 0 or unset, the maximum
            possible value will be used for that execution. The actual
            number of tasks running in steady state will be less than
            this number when there are fewer tasks waiting to be
            completed remaining, i.e. when the work left to do is less
            than max parallelism.
        task_count (int):
            Specifies the desired number of tasks the
            execution should run. Setting to 1 means that
            parallelism is limited to 1 and the success of
            that task signals the success of the execution.
            More info:
            https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/
        template (google.cloud.run_v2.types.TaskTemplate):
            Required. Describes the task(s) that will be
            created when executing an execution.
    """

    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    parallelism: int = proto.Field(
        proto.INT32,
        number=3,
    )
    task_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    template: task_template.TaskTemplate = proto.Field(
        proto.MESSAGE,
        number=5,
        message=task_template.TaskTemplate,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
