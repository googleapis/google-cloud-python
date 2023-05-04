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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ai.generativelanguage.v1beta2",
    manifest={
        "GenerateTextRequest",
        "GenerateTextResponse",
        "TextPrompt",
        "TextCompletion",
        "EmbedTextRequest",
        "EmbedTextResponse",
        "Embedding",
    },
)


class GenerateTextRequest(proto.Message):
    r"""Request to generate a text completion response from the
    model.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        model (str):
            Required. The model name to use with the
            format name=models/{model}.
        prompt (google.ai.generativelanguage_v1beta2.types.TextPrompt):
            Required. The free-form input text given to
            the model as a prompt.
            Given a prompt, the model will generate a
            TextCompletion response it predicts as the
            completion of the input text.
        temperature (float):
            Controls the randomness of the output. Note: The default
            value varies by model, see the ``Model.temperature``
            attribute of the ``Model`` returned the ``getModel``
            function.

            Values can range from [0.0,1.0], inclusive. A value closer
            to 1.0 will produce responses that are more varied and
            creative, while a value closer to 0.0 will typically result
            in more straightforward responses from the model.

            This field is a member of `oneof`_ ``_temperature``.
        candidate_count (int):
            Number of generated responses to return.

            This value must be between [1, 8], inclusive. If unset, this
            will default to 1.

            This field is a member of `oneof`_ ``_candidate_count``.
        max_output_tokens (int):
            The maximum number of tokens to include in a
            candidate.
            If unset, this will default to 64.

            This field is a member of `oneof`_ ``_max_output_tokens``.
        top_p (float):
            The maximum cumulative probability of tokens to consider
            when sampling.

            The model uses combined Top-k and nucleus sampling.

            Tokens are sorted based on their assigned probabilities so
            that only the most liekly tokens are considered. Top-k
            sampling directly limits the maximum number of tokens to
            consider, while Nucleus sampling limits number of tokens
            based on the cumulative probability.

            Note: The default value varies by model, see the
            ``Model.top_p`` attribute of the ``Model`` returned the
            ``getModel`` function.

            This field is a member of `oneof`_ ``_top_p``.
        top_k (int):
            The maximum number of tokens to consider when sampling.

            The model uses combined Top-k and nucleus sampling.

            Top-k sampling considers the set of ``top_k`` most probable
            tokens. Defaults to 40.

            Note: The default value varies by model, see the
            ``Model.top_k`` attribute of the ``Model`` returned the
            ``getModel`` function.

            This field is a member of `oneof`_ ``_top_k``.
        stop_sequences (MutableSequence[str]):
            The set of character sequences (up to 5) that
            will stop output generation. If specified, the
            API will stop at the first appearance of a stop
            sequence. The stop sequence will not be included
            as part of the response.
    """

    model: str = proto.Field(
        proto.STRING,
        number=1,
    )
    prompt: "TextPrompt" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TextPrompt",
    )
    temperature: float = proto.Field(
        proto.FLOAT,
        number=3,
        optional=True,
    )
    candidate_count: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    max_output_tokens: int = proto.Field(
        proto.INT32,
        number=5,
        optional=True,
    )
    top_p: float = proto.Field(
        proto.FLOAT,
        number=6,
        optional=True,
    )
    top_k: int = proto.Field(
        proto.INT32,
        number=7,
        optional=True,
    )
    stop_sequences: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )


class GenerateTextResponse(proto.Message):
    r"""The response from the model, including candidate completions.

    Attributes:
        candidates (MutableSequence[google.ai.generativelanguage_v1beta2.types.TextCompletion]):
            Candidate responses from the model.
    """

    candidates: MutableSequence["TextCompletion"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TextCompletion",
    )


class TextPrompt(proto.Message):
    r"""Text given to the model as a prompt.
    The Model will use this TextPrompt to Generate a text
    completion.

    Attributes:
        text (str):
            Required. The prompt text.
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
    )


class TextCompletion(proto.Message):
    r"""Output text returned from a model.

    Attributes:
        output (str):
            Output only. The generated text returned from
            the model.
    """

    output: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EmbedTextRequest(proto.Message):
    r"""Request to get a text embedding from the model.

    Attributes:
        model (str):
            Required. The model name to use with the
            format model=models/{model}.
        text (str):
            Required. The free-form input text that the
            model will turn into an embedding.
    """

    model: str = proto.Field(
        proto.STRING,
        number=1,
    )
    text: str = proto.Field(
        proto.STRING,
        number=2,
    )


class EmbedTextResponse(proto.Message):
    r"""The response to a EmbedTextRequest.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        embedding (google.ai.generativelanguage_v1beta2.types.Embedding):
            Output only. The embedding generated from the
            input text.

            This field is a member of `oneof`_ ``_embedding``.
    """

    embedding: "Embedding" = proto.Field(
        proto.MESSAGE,
        number=1,
        optional=True,
        message="Embedding",
    )


class Embedding(proto.Message):
    r"""A list of floats representing the embedding.

    Attributes:
        value (MutableSequence[float]):
            The embedding values.
    """

    value: MutableSequence[float] = proto.RepeatedField(
        proto.FLOAT,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
