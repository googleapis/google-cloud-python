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
    package="google.cloud.securitycenter.v1", manifest={"Indicator",},
)


class Indicator(proto.Message):
    r"""Represents what's commonly known as an Indicator of compromise (IoC)
    in computer forensics. This is an artifact observed on a network or
    in an operating system that, with high confidence, indicates a
    computer intrusion. Reference:
    https://en.wikipedia.org/wiki/Indicator_of_compromise

    Attributes:
        ip_addresses (Sequence[str]):
            List of ip addresses associated to the
            Finding.
        domains (Sequence[str]):
            List of domains associated to the Finding.
    """

    ip_addresses = proto.RepeatedField(proto.STRING, number=1,)
    domains = proto.RepeatedField(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
