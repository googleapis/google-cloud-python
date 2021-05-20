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
    package="google.cloud.language.v1beta2",
    manifest={
        "EncodingType",
        "Document",
        "Sentence",
        "Entity",
        "Token",
        "Sentiment",
        "PartOfSpeech",
        "DependencyEdge",
        "EntityMention",
        "TextSpan",
        "ClassificationCategory",
        "AnalyzeSentimentRequest",
        "AnalyzeSentimentResponse",
        "AnalyzeEntitySentimentRequest",
        "AnalyzeEntitySentimentResponse",
        "AnalyzeEntitiesRequest",
        "AnalyzeEntitiesResponse",
        "AnalyzeSyntaxRequest",
        "AnalyzeSyntaxResponse",
        "ClassifyTextRequest",
        "ClassifyTextResponse",
        "AnnotateTextRequest",
        "AnnotateTextResponse",
    },
)


class EncodingType(proto.Enum):
    r"""Represents the text encoding that the caller uses to process the
    output. Providing an ``EncodingType`` is recommended because the API
    provides the beginning offsets for various outputs, such as tokens
    and mentions, and languages that natively use different text
    encodings may access offsets differently.
    """
    NONE = 0
    UTF8 = 1
    UTF16 = 2
    UTF32 = 3


class Document(proto.Message):
    r"""Represents the input to API methods.

    Attributes:
        type_ (google.cloud.language_v1beta2.types.Document.Type):
            Required. If the type is not set or is ``TYPE_UNSPECIFIED``,
            returns an ``INVALID_ARGUMENT`` error.
        content (str):
            The content of the input in string format.
            Cloud audit logging exempt since it is based on
            user data.
        gcs_content_uri (str):
            The Google Cloud Storage URI where the file content is
            located. This URI must be of the form:
            gs://bucket_name/object_name. For more details, see
            https://cloud.google.com/storage/docs/reference-uris. NOTE:
            Cloud Storage object versioning is not supported.
        language (str):
            The language of the document (if not specified, the language
            is automatically detected). Both ISO and BCP-47 language
            codes are accepted. `Language
            Support <https://cloud.google.com/natural-language/docs/languages>`__
            lists currently supported languages for each API method. If
            the language (either specified by the caller or
            automatically detected) is not supported by the called API
            method, an ``INVALID_ARGUMENT`` error is returned.
    """

    class Type(proto.Enum):
        r"""The document types enum."""
        TYPE_UNSPECIFIED = 0
        PLAIN_TEXT = 1
        HTML = 2

    type_ = proto.Field(proto.ENUM, number=1, enum=Type,)
    content = proto.Field(proto.STRING, number=2, oneof="source",)
    gcs_content_uri = proto.Field(proto.STRING, number=3, oneof="source",)
    language = proto.Field(proto.STRING, number=4,)


class Sentence(proto.Message):
    r"""Represents a sentence in the input document.
    Attributes:
        text (google.cloud.language_v1beta2.types.TextSpan):
            The sentence text.
        sentiment (google.cloud.language_v1beta2.types.Sentiment):
            For calls to [AnalyzeSentiment][] or if
            [AnnotateTextRequest.Features.extract_document_sentiment][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_document_sentiment]
            is set to true, this field will contain the sentiment for
            the sentence.
    """

    text = proto.Field(proto.MESSAGE, number=1, message="TextSpan",)
    sentiment = proto.Field(proto.MESSAGE, number=2, message="Sentiment",)


class Entity(proto.Message):
    r"""Represents a phrase in the text that is a known entity, such
    as a person, an organization, or location. The API associates
    information, such as salience and mentions, with entities.

    Attributes:
        name (str):
            The representative name for the entity.
        type_ (google.cloud.language_v1beta2.types.Entity.Type):
            The entity type.
        metadata (Sequence[google.cloud.language_v1beta2.types.Entity.MetadataEntry]):
            Metadata associated with the entity.

            For most entity types, the metadata is a Wikipedia URL
            (``wikipedia_url``) and Knowledge Graph MID (``mid``), if
            they are available. For the metadata associated with other
            entity types, see the Type table below.
        salience (float):
            The salience score associated with the entity in the [0,
            1.0] range.

            The salience score for an entity provides information about
            the importance or centrality of that entity to the entire
            document text. Scores closer to 0 are less salient, while
            scores closer to 1.0 are highly salient.
        mentions (Sequence[google.cloud.language_v1beta2.types.EntityMention]):
            The mentions of this entity in the input
            document. The API currently supports proper noun
            mentions.
        sentiment (google.cloud.language_v1beta2.types.Sentiment):
            For calls to [AnalyzeEntitySentiment][] or if
            [AnnotateTextRequest.Features.extract_entity_sentiment][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_entity_sentiment]
            is set to true, this field will contain the aggregate
            sentiment expressed for this entity in the provided
            document.
    """

    class Type(proto.Enum):
        r"""The type of the entity. For most entity types, the associated
        metadata is a Wikipedia URL (``wikipedia_url``) and Knowledge Graph
        MID (``mid``). The table below lists the associated fields for
        entities that have different metadata.
        """
        UNKNOWN = 0
        PERSON = 1
        LOCATION = 2
        ORGANIZATION = 3
        EVENT = 4
        WORK_OF_ART = 5
        CONSUMER_GOOD = 6
        OTHER = 7
        PHONE_NUMBER = 9
        ADDRESS = 10
        DATE = 11
        NUMBER = 12
        PRICE = 13

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=3,)
    salience = proto.Field(proto.FLOAT, number=4,)
    mentions = proto.RepeatedField(proto.MESSAGE, number=5, message="EntityMention",)
    sentiment = proto.Field(proto.MESSAGE, number=6, message="Sentiment",)


class Token(proto.Message):
    r"""Represents the smallest syntactic building block of the text.
    Attributes:
        text (google.cloud.language_v1beta2.types.TextSpan):
            The token text.
        part_of_speech (google.cloud.language_v1beta2.types.PartOfSpeech):
            Parts of speech tag for this token.
        dependency_edge (google.cloud.language_v1beta2.types.DependencyEdge):
            Dependency tree parse for this token.
        lemma (str):
            `Lemma <https://en.wikipedia.org/wiki/Lemma_%28morphology%29>`__
            of the token.
    """

    text = proto.Field(proto.MESSAGE, number=1, message="TextSpan",)
    part_of_speech = proto.Field(proto.MESSAGE, number=2, message="PartOfSpeech",)
    dependency_edge = proto.Field(proto.MESSAGE, number=3, message="DependencyEdge",)
    lemma = proto.Field(proto.STRING, number=4,)


class Sentiment(proto.Message):
    r"""Represents the feeling associated with the entire text or
    entities in the text.
    Next ID: 6

    Attributes:
        magnitude (float):
            A non-negative number in the [0, +inf) range, which
            represents the absolute magnitude of sentiment regardless of
            score (positive or negative).
        score (float):
            Sentiment score between -1.0 (negative
            sentiment) and 1.0 (positive sentiment).
    """

    magnitude = proto.Field(proto.FLOAT, number=2,)
    score = proto.Field(proto.FLOAT, number=3,)


class PartOfSpeech(proto.Message):
    r"""Represents part of speech information for a token.
    Attributes:
        tag (google.cloud.language_v1beta2.types.PartOfSpeech.Tag):
            The part of speech tag.
        aspect (google.cloud.language_v1beta2.types.PartOfSpeech.Aspect):
            The grammatical aspect.
        case (google.cloud.language_v1beta2.types.PartOfSpeech.Case):
            The grammatical case.
        form (google.cloud.language_v1beta2.types.PartOfSpeech.Form):
            The grammatical form.
        gender (google.cloud.language_v1beta2.types.PartOfSpeech.Gender):
            The grammatical gender.
        mood (google.cloud.language_v1beta2.types.PartOfSpeech.Mood):
            The grammatical mood.
        number (google.cloud.language_v1beta2.types.PartOfSpeech.Number):
            The grammatical number.
        person (google.cloud.language_v1beta2.types.PartOfSpeech.Person):
            The grammatical person.
        proper (google.cloud.language_v1beta2.types.PartOfSpeech.Proper):
            The grammatical properness.
        reciprocity (google.cloud.language_v1beta2.types.PartOfSpeech.Reciprocity):
            The grammatical reciprocity.
        tense (google.cloud.language_v1beta2.types.PartOfSpeech.Tense):
            The grammatical tense.
        voice (google.cloud.language_v1beta2.types.PartOfSpeech.Voice):
            The grammatical voice.
    """

    class Tag(proto.Enum):
        r"""The part of speech tags enum."""
        UNKNOWN = 0
        ADJ = 1
        ADP = 2
        ADV = 3
        CONJ = 4
        DET = 5
        NOUN = 6
        NUM = 7
        PRON = 8
        PRT = 9
        PUNCT = 10
        VERB = 11
        X = 12
        AFFIX = 13

    class Aspect(proto.Enum):
        r"""The characteristic of a verb that expresses time flow during
        an event.
        """
        ASPECT_UNKNOWN = 0
        PERFECTIVE = 1
        IMPERFECTIVE = 2
        PROGRESSIVE = 3

    class Case(proto.Enum):
        r"""The grammatical function performed by a noun or pronoun in a
        phrase, clause, or sentence. In some languages, other parts of
        speech, such as adjective and determiner, take case inflection
        in agreement with the noun.
        """
        CASE_UNKNOWN = 0
        ACCUSATIVE = 1
        ADVERBIAL = 2
        COMPLEMENTIVE = 3
        DATIVE = 4
        GENITIVE = 5
        INSTRUMENTAL = 6
        LOCATIVE = 7
        NOMINATIVE = 8
        OBLIQUE = 9
        PARTITIVE = 10
        PREPOSITIONAL = 11
        REFLEXIVE_CASE = 12
        RELATIVE_CASE = 13
        VOCATIVE = 14

    class Form(proto.Enum):
        r"""Depending on the language, Form can be categorizing different
        forms of verbs, adjectives, adverbs, etc. For example,
        categorizing inflected endings of verbs and adjectives or
        distinguishing between short and long forms of adjectives and
        participles
        """
        FORM_UNKNOWN = 0
        ADNOMIAL = 1
        AUXILIARY = 2
        COMPLEMENTIZER = 3
        FINAL_ENDING = 4
        GERUND = 5
        REALIS = 6
        IRREALIS = 7
        SHORT = 8
        LONG = 9
        ORDER = 10
        SPECIFIC = 11

    class Gender(proto.Enum):
        r"""Gender classes of nouns reflected in the behaviour of
        associated words.
        """
        GENDER_UNKNOWN = 0
        FEMININE = 1
        MASCULINE = 2
        NEUTER = 3

    class Mood(proto.Enum):
        r"""The grammatical feature of verbs, used for showing modality
        and attitude.
        """
        MOOD_UNKNOWN = 0
        CONDITIONAL_MOOD = 1
        IMPERATIVE = 2
        INDICATIVE = 3
        INTERROGATIVE = 4
        JUSSIVE = 5
        SUBJUNCTIVE = 6

    class Number(proto.Enum):
        r"""Count distinctions."""
        NUMBER_UNKNOWN = 0
        SINGULAR = 1
        PLURAL = 2
        DUAL = 3

    class Person(proto.Enum):
        r"""The distinction between the speaker, second person, third
        person, etc.
        """
        PERSON_UNKNOWN = 0
        FIRST = 1
        SECOND = 2
        THIRD = 3
        REFLEXIVE_PERSON = 4

    class Proper(proto.Enum):
        r"""This category shows if the token is part of a proper name."""
        PROPER_UNKNOWN = 0
        PROPER = 1
        NOT_PROPER = 2

    class Reciprocity(proto.Enum):
        r"""Reciprocal features of a pronoun."""
        RECIPROCITY_UNKNOWN = 0
        RECIPROCAL = 1
        NON_RECIPROCAL = 2

    class Tense(proto.Enum):
        r"""Time reference."""
        TENSE_UNKNOWN = 0
        CONDITIONAL_TENSE = 1
        FUTURE = 2
        PAST = 3
        PRESENT = 4
        IMPERFECT = 5
        PLUPERFECT = 6

    class Voice(proto.Enum):
        r"""The relationship between the action that a verb expresses and
        the participants identified by its arguments.
        """
        VOICE_UNKNOWN = 0
        ACTIVE = 1
        CAUSATIVE = 2
        PASSIVE = 3

    tag = proto.Field(proto.ENUM, number=1, enum=Tag,)
    aspect = proto.Field(proto.ENUM, number=2, enum=Aspect,)
    case = proto.Field(proto.ENUM, number=3, enum=Case,)
    form = proto.Field(proto.ENUM, number=4, enum=Form,)
    gender = proto.Field(proto.ENUM, number=5, enum=Gender,)
    mood = proto.Field(proto.ENUM, number=6, enum=Mood,)
    number = proto.Field(proto.ENUM, number=7, enum=Number,)
    person = proto.Field(proto.ENUM, number=8, enum=Person,)
    proper = proto.Field(proto.ENUM, number=9, enum=Proper,)
    reciprocity = proto.Field(proto.ENUM, number=10, enum=Reciprocity,)
    tense = proto.Field(proto.ENUM, number=11, enum=Tense,)
    voice = proto.Field(proto.ENUM, number=12, enum=Voice,)


class DependencyEdge(proto.Message):
    r"""Represents dependency parse tree information for a token.
    Attributes:
        head_token_index (int):
            Represents the head of this token in the dependency tree.
            This is the index of the token which has an arc going to
            this token. The index is the position of the token in the
            array of tokens returned by the API method. If this token is
            a root token, then the ``head_token_index`` is its own
            index.
        label (google.cloud.language_v1beta2.types.DependencyEdge.Label):
            The parse label for the token.
    """

    class Label(proto.Enum):
        r"""The parse label enum for the token."""
        UNKNOWN = 0
        ABBREV = 1
        ACOMP = 2
        ADVCL = 3
        ADVMOD = 4
        AMOD = 5
        APPOS = 6
        ATTR = 7
        AUX = 8
        AUXPASS = 9
        CC = 10
        CCOMP = 11
        CONJ = 12
        CSUBJ = 13
        CSUBJPASS = 14
        DEP = 15
        DET = 16
        DISCOURSE = 17
        DOBJ = 18
        EXPL = 19
        GOESWITH = 20
        IOBJ = 21
        MARK = 22
        MWE = 23
        MWV = 24
        NEG = 25
        NN = 26
        NPADVMOD = 27
        NSUBJ = 28
        NSUBJPASS = 29
        NUM = 30
        NUMBER = 31
        P = 32
        PARATAXIS = 33
        PARTMOD = 34
        PCOMP = 35
        POBJ = 36
        POSS = 37
        POSTNEG = 38
        PRECOMP = 39
        PRECONJ = 40
        PREDET = 41
        PREF = 42
        PREP = 43
        PRONL = 44
        PRT = 45
        PS = 46
        QUANTMOD = 47
        RCMOD = 48
        RCMODREL = 49
        RDROP = 50
        REF = 51
        REMNANT = 52
        REPARANDUM = 53
        ROOT = 54
        SNUM = 55
        SUFF = 56
        TMOD = 57
        TOPIC = 58
        VMOD = 59
        VOCATIVE = 60
        XCOMP = 61
        SUFFIX = 62
        TITLE = 63
        ADVPHMOD = 64
        AUXCAUS = 65
        AUXVV = 66
        DTMOD = 67
        FOREIGN = 68
        KW = 69
        LIST = 70
        NOMC = 71
        NOMCSUBJ = 72
        NOMCSUBJPASS = 73
        NUMC = 74
        COP = 75
        DISLOCATED = 76
        ASP = 77
        GMOD = 78
        GOBJ = 79
        INFMOD = 80
        MES = 81
        NCOMP = 82

    head_token_index = proto.Field(proto.INT32, number=1,)
    label = proto.Field(proto.ENUM, number=2, enum=Label,)


class EntityMention(proto.Message):
    r"""Represents a mention for an entity in the text. Currently,
    proper noun mentions are supported.

    Attributes:
        text (google.cloud.language_v1beta2.types.TextSpan):
            The mention text.
        type_ (google.cloud.language_v1beta2.types.EntityMention.Type):
            The type of the entity mention.
        sentiment (google.cloud.language_v1beta2.types.Sentiment):
            For calls to [AnalyzeEntitySentiment][] or if
            [AnnotateTextRequest.Features.extract_entity_sentiment][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_entity_sentiment]
            is set to true, this field will contain the sentiment
            expressed for this mention of the entity in the provided
            document.
    """

    class Type(proto.Enum):
        r"""The supported types of mentions."""
        TYPE_UNKNOWN = 0
        PROPER = 1
        COMMON = 2

    text = proto.Field(proto.MESSAGE, number=1, message="TextSpan",)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    sentiment = proto.Field(proto.MESSAGE, number=3, message="Sentiment",)


class TextSpan(proto.Message):
    r"""Represents an output piece of text.
    Attributes:
        content (str):
            The content of the output text.
        begin_offset (int):
            The API calculates the beginning offset of the content in
            the original document according to the
            [EncodingType][google.cloud.language.v1beta2.EncodingType]
            specified in the API request.
    """

    content = proto.Field(proto.STRING, number=1,)
    begin_offset = proto.Field(proto.INT32, number=2,)


class ClassificationCategory(proto.Message):
    r"""Represents a category returned from the text classifier.
    Attributes:
        name (str):
            The name of the category representing the document, from the
            `predefined
            taxonomy <https://cloud.google.com/natural-language/docs/categories>`__.
        confidence (float):
            The classifier's confidence of the category.
            Number represents how certain the classifier is
            that this category represents the given text.
    """

    name = proto.Field(proto.STRING, number=1,)
    confidence = proto.Field(proto.FLOAT, number=2,)


class AnalyzeSentimentRequest(proto.Message):
    r"""The sentiment analysis request message.
    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
        encoding_type (google.cloud.language_v1beta2.types.EncodingType):
            The encoding type used by the API to
            calculate sentence offsets for the sentence
            sentiment.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    encoding_type = proto.Field(proto.ENUM, number=2, enum="EncodingType",)


class AnalyzeSentimentResponse(proto.Message):
    r"""The sentiment analysis response message.
    Attributes:
        document_sentiment (google.cloud.language_v1beta2.types.Sentiment):
            The overall sentiment of the input document.
        language (str):
            The language of the text, which will be the same as the
            language specified in the request or, if not specified, the
            automatically-detected language. See
            [Document.language][google.cloud.language.v1beta2.Document.language]
            field for more details.
        sentences (Sequence[google.cloud.language_v1beta2.types.Sentence]):
            The sentiment for all the sentences in the
            document.
    """

    document_sentiment = proto.Field(proto.MESSAGE, number=1, message="Sentiment",)
    language = proto.Field(proto.STRING, number=2,)
    sentences = proto.RepeatedField(proto.MESSAGE, number=3, message="Sentence",)


class AnalyzeEntitySentimentRequest(proto.Message):
    r"""The entity-level sentiment analysis request message.
    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
        encoding_type (google.cloud.language_v1beta2.types.EncodingType):
            The encoding type used by the API to
            calculate offsets.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    encoding_type = proto.Field(proto.ENUM, number=2, enum="EncodingType",)


class AnalyzeEntitySentimentResponse(proto.Message):
    r"""The entity-level sentiment analysis response message.
    Attributes:
        entities (Sequence[google.cloud.language_v1beta2.types.Entity]):
            The recognized entities in the input document
            with associated sentiments.
        language (str):
            The language of the text, which will be the same as the
            language specified in the request or, if not specified, the
            automatically-detected language. See
            [Document.language][google.cloud.language.v1beta2.Document.language]
            field for more details.
    """

    entities = proto.RepeatedField(proto.MESSAGE, number=1, message="Entity",)
    language = proto.Field(proto.STRING, number=2,)


class AnalyzeEntitiesRequest(proto.Message):
    r"""The entity analysis request message.
    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
        encoding_type (google.cloud.language_v1beta2.types.EncodingType):
            The encoding type used by the API to
            calculate offsets.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    encoding_type = proto.Field(proto.ENUM, number=2, enum="EncodingType",)


class AnalyzeEntitiesResponse(proto.Message):
    r"""The entity analysis response message.
    Attributes:
        entities (Sequence[google.cloud.language_v1beta2.types.Entity]):
            The recognized entities in the input
            document.
        language (str):
            The language of the text, which will be the same as the
            language specified in the request or, if not specified, the
            automatically-detected language. See
            [Document.language][google.cloud.language.v1beta2.Document.language]
            field for more details.
    """

    entities = proto.RepeatedField(proto.MESSAGE, number=1, message="Entity",)
    language = proto.Field(proto.STRING, number=2,)


class AnalyzeSyntaxRequest(proto.Message):
    r"""The syntax analysis request message.
    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
        encoding_type (google.cloud.language_v1beta2.types.EncodingType):
            The encoding type used by the API to
            calculate offsets.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    encoding_type = proto.Field(proto.ENUM, number=2, enum="EncodingType",)


class AnalyzeSyntaxResponse(proto.Message):
    r"""The syntax analysis response message.
    Attributes:
        sentences (Sequence[google.cloud.language_v1beta2.types.Sentence]):
            Sentences in the input document.
        tokens (Sequence[google.cloud.language_v1beta2.types.Token]):
            Tokens, along with their syntactic
            information, in the input document.
        language (str):
            The language of the text, which will be the same as the
            language specified in the request or, if not specified, the
            automatically-detected language. See
            [Document.language][google.cloud.language.v1beta2.Document.language]
            field for more details.
    """

    sentences = proto.RepeatedField(proto.MESSAGE, number=1, message="Sentence",)
    tokens = proto.RepeatedField(proto.MESSAGE, number=2, message="Token",)
    language = proto.Field(proto.STRING, number=3,)


class ClassifyTextRequest(proto.Message):
    r"""The document classification request message.
    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)


class ClassifyTextResponse(proto.Message):
    r"""The document classification response message.
    Attributes:
        categories (Sequence[google.cloud.language_v1beta2.types.ClassificationCategory]):
            Categories representing the input document.
    """

    categories = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ClassificationCategory",
    )


class AnnotateTextRequest(proto.Message):
    r"""The request message for the text annotation API, which can
    perform multiple analysis types (sentiment, entities, and
    syntax) in one call.

    Attributes:
        document (google.cloud.language_v1beta2.types.Document):
            Required. Input document.
        features (google.cloud.language_v1beta2.types.AnnotateTextRequest.Features):
            Required. The enabled features.
        encoding_type (google.cloud.language_v1beta2.types.EncodingType):
            The encoding type used by the API to
            calculate offsets.
    """

    class Features(proto.Message):
        r"""All available features for sentiment, syntax, and semantic
        analysis. Setting each one to true will enable that specific
        analysis for the input. Next ID: 10

        Attributes:
            extract_syntax (bool):
                Extract syntax information.
            extract_entities (bool):
                Extract entities.
            extract_document_sentiment (bool):
                Extract document-level sentiment.
            extract_entity_sentiment (bool):
                Extract entities and their associated
                sentiment.
            classify_text (bool):
                Classify the full document into categories. If this is true,
                the API will use the default model which classifies into a
                `predefined
                taxonomy <https://cloud.google.com/natural-language/docs/categories>`__.
        """

        extract_syntax = proto.Field(proto.BOOL, number=1,)
        extract_entities = proto.Field(proto.BOOL, number=2,)
        extract_document_sentiment = proto.Field(proto.BOOL, number=3,)
        extract_entity_sentiment = proto.Field(proto.BOOL, number=4,)
        classify_text = proto.Field(proto.BOOL, number=6,)

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    features = proto.Field(proto.MESSAGE, number=2, message=Features,)
    encoding_type = proto.Field(proto.ENUM, number=3, enum="EncodingType",)


class AnnotateTextResponse(proto.Message):
    r"""The text annotations response message.
    Attributes:
        sentences (Sequence[google.cloud.language_v1beta2.types.Sentence]):
            Sentences in the input document. Populated if the user
            enables
            [AnnotateTextRequest.Features.extract_syntax][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_syntax].
        tokens (Sequence[google.cloud.language_v1beta2.types.Token]):
            Tokens, along with their syntactic information, in the input
            document. Populated if the user enables
            [AnnotateTextRequest.Features.extract_syntax][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_syntax].
        entities (Sequence[google.cloud.language_v1beta2.types.Entity]):
            Entities, along with their semantic information, in the
            input document. Populated if the user enables
            [AnnotateTextRequest.Features.extract_entities][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_entities].
        document_sentiment (google.cloud.language_v1beta2.types.Sentiment):
            The overall sentiment for the document. Populated if the
            user enables
            [AnnotateTextRequest.Features.extract_document_sentiment][google.cloud.language.v1beta2.AnnotateTextRequest.Features.extract_document_sentiment].
        language (str):
            The language of the text, which will be the same as the
            language specified in the request or, if not specified, the
            automatically-detected language. See
            [Document.language][google.cloud.language.v1beta2.Document.language]
            field for more details.
        categories (Sequence[google.cloud.language_v1beta2.types.ClassificationCategory]):
            Categories identified in the input document.
    """

    sentences = proto.RepeatedField(proto.MESSAGE, number=1, message="Sentence",)
    tokens = proto.RepeatedField(proto.MESSAGE, number=2, message="Token",)
    entities = proto.RepeatedField(proto.MESSAGE, number=3, message="Entity",)
    document_sentiment = proto.Field(proto.MESSAGE, number=4, message="Sentiment",)
    language = proto.Field(proto.STRING, number=5,)
    categories = proto.RepeatedField(
        proto.MESSAGE, number=6, message="ClassificationCategory",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
