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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={"ValidationError", "ValidationResult",},
)


class ValidationError(proto.Message):
    r"""Represents a single validation error.
    Attributes:
        severity (google.cloud.dialogflow_v2beta1.types.ValidationError.Severity):
            The severity of the error.
        entries (Sequence[str]):
            The names of the entries that the error is
            associated with. Format:

            - "projects/<Project ID>/agent", if the error is
            associated with the entire agent.
            - "projects/<Project ID>/agent/intents/<Intent
            ID>", if the error is associated with certain
            intents.
            - "projects/<Project
            ID>/agent/intents/<Intent
            Id>/trainingPhrases/<Training Phrase ID>", if
            the error is associated with certain intent
            training phrases. - "projects/<Project
            ID>/agent/intents/<Intent
            Id>/parameters/<Parameter ID>", if the error is
            associated with certain intent parameters. -
            "projects/<Project ID>/agent/entities/<Entity
            ID>", if the error is associated with certain
            entities.
        error_message (str):
            The detailed error message.
    """

    class Severity(proto.Enum):
        r"""Represents a level of severity."""
        SEVERITY_UNSPECIFIED = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        CRITICAL = 4

    severity = proto.Field(proto.ENUM, number=1, enum=Severity,)
    entries = proto.RepeatedField(proto.STRING, number=3,)
    error_message = proto.Field(proto.STRING, number=4,)


class ValidationResult(proto.Message):
    r"""Represents the output of agent validation.
    Attributes:
        validation_errors (Sequence[google.cloud.dialogflow_v2beta1.types.ValidationError]):
            Contains all validation errors.
    """

    validation_errors = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ValidationError",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
