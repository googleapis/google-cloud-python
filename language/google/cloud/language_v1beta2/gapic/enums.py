# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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


class EncodingType(enum.IntEnum):
    """
    Represents the text encoding that the caller uses to process the output.
    Providing an ``EncodingType`` is recommended because the API provides
    the beginning offsets for various outputs, such as tokens and mentions,
    and languages that natively use different text encodings may access
    offsets differently.

    Attributes:
      NONE (int): If ``EncodingType`` is not specified, encoding-dependent information
      (such as ``begin_offset``) will be set at ``-1``.
      UTF8 (int): Encoding-dependent information (such as ``begin_offset``) is calculated
      based on the UTF-8 encoding of the input. C++ and Go are examples of
      languages that use this encoding natively.
      UTF16 (int): Encoding-dependent information (such as ``begin_offset``) is calculated
      based on the UTF-16 encoding of the input. Java and Javascript are
      examples of languages that use this encoding natively.
      UTF32 (int): Encoding-dependent information (such as ``begin_offset``) is calculated
      based on the UTF-32 encoding of the input. Python is an example of a
      language that uses this encoding natively.
    """

    NONE = 0
    UTF8 = 1
    UTF16 = 2
    UTF32 = 3


class DependencyEdge(object):
    class Label(enum.IntEnum):
        """
        The parse label enum for the token.

        Attributes:
          UNKNOWN (int): Unknown
          ABBREV (int): Abbreviation modifier
          ACOMP (int): Adjectival complement
          ADVCL (int): Adverbial clause modifier
          ADVMOD (int): Adverbial modifier
          AMOD (int): Adjectival modifier of an NP
          APPOS (int): Appositional modifier of an NP
          ATTR (int): Attribute dependent of a copular verb
          AUX (int): Auxiliary (non-main) verb
          AUXPASS (int): Passive auxiliary
          CC (int): Coordinating conjunction
          CCOMP (int): Clausal complement of a verb or adjective
          CONJ (int): Conjunct
          CSUBJ (int): Clausal subject
          CSUBJPASS (int): Clausal passive subject
          DEP (int): Dependency (unable to determine)
          DET (int): Determiner
          DISCOURSE (int): Discourse
          DOBJ (int): Direct object
          EXPL (int): Expletive
          GOESWITH (int): Goes with (part of a word in a text not well edited)
          IOBJ (int): Indirect object
          MARK (int): Marker (word introducing a subordinate clause)
          MWE (int): Multi-word expression
          MWV (int): Multi-word verbal expression
          NEG (int): Negation modifier
          NN (int): Noun compound modifier
          NPADVMOD (int): Noun phrase used as an adverbial modifier
          NSUBJ (int): Nominal subject
          NSUBJPASS (int): Passive nominal subject
          NUM (int): Numeric modifier of a noun
          NUMBER (int): Element of compound number
          P (int): Punctuation mark
          PARATAXIS (int): Parataxis relation
          PARTMOD (int): Participial modifier
          PCOMP (int): The complement of a preposition is a clause
          POBJ (int): Object of a preposition
          POSS (int): Possession modifier
          POSTNEG (int): Postverbal negative particle
          PRECOMP (int): Predicate complement
          PRECONJ (int): Preconjunt
          PREDET (int): Predeterminer
          PREF (int): Prefix
          PREP (int): Prepositional modifier
          PRONL (int): The relationship between a verb and verbal morpheme
          PRT (int): Particle
          PS (int): Associative or possessive marker
          QUANTMOD (int): Quantifier phrase modifier
          RCMOD (int): Relative clause modifier
          RCMODREL (int): Complementizer in relative clause
          RDROP (int): Ellipsis without a preceding predicate
          REF (int): Referent
          REMNANT (int): Remnant
          REPARANDUM (int): Reparandum
          ROOT (int): Root
          SNUM (int): Suffix specifying a unit of number
          SUFF (int): Suffix
          TMOD (int): Temporal modifier
          TOPIC (int): Topic marker
          VMOD (int): Clause headed by an infinite form of the verb that modifies a noun
          VOCATIVE (int): Vocative
          XCOMP (int): Open clausal complement
          SUFFIX (int): Name suffix
          TITLE (int): Name title
          ADVPHMOD (int): Adverbial phrase modifier
          AUXCAUS (int): Causative auxiliary
          AUXVV (int): Helper auxiliary
          DTMOD (int): Rentaishi (Prenominal modifier)
          FOREIGN (int): Foreign words
          KW (int): Keyword
          LIST (int): List for chains of comparable items
          NOMC (int): Nominalized clause
          NOMCSUBJ (int): Nominalized clausal subject
          NOMCSUBJPASS (int): Nominalized clausal passive
          NUMC (int): Compound of numeric modifier
          COP (int): Copula
          DISLOCATED (int): Dislocated relation (for fronted/topicalized elements)
          ASP (int): Aspect marker
          GMOD (int): Genitive modifier
          GOBJ (int): Genitive object
          INFMOD (int): Infinitival modifier
          MES (int): Measure
          NCOMP (int): Nominal complement of a noun
        """

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


class Document(object):
    class Type(enum.IntEnum):
        """
        The document types enum.

        Attributes:
          TYPE_UNSPECIFIED (int): The content type is not specified.
          PLAIN_TEXT (int): Plain text
          HTML (int): HTML
        """

        TYPE_UNSPECIFIED = 0
        PLAIN_TEXT = 1
        HTML = 2


class Entity(object):
    class Type(enum.IntEnum):
        """
        The type of the entity.

        Attributes:
          UNKNOWN (int): Unknown
          PERSON (int): Person
          LOCATION (int): Location
          ORGANIZATION (int): Organization
          EVENT (int): Event
          WORK_OF_ART (int): Work of art
          CONSUMER_GOOD (int): Consumer goods
          OTHER (int): Other types
        """

        UNKNOWN = 0
        PERSON = 1
        LOCATION = 2
        ORGANIZATION = 3
        EVENT = 4
        WORK_OF_ART = 5
        CONSUMER_GOOD = 6
        OTHER = 7


class EntityMention(object):
    class Type(enum.IntEnum):
        """
        The supported types of mentions.

        Attributes:
          TYPE_UNKNOWN (int): Unknown
          PROPER (int): Proper name
          COMMON (int): Common noun (or noun compound)
        """

        TYPE_UNKNOWN = 0
        PROPER = 1
        COMMON = 2


class PartOfSpeech(object):
    class Aspect(enum.IntEnum):
        """
        The characteristic of a verb that expresses time flow during an event.

        Attributes:
          ASPECT_UNKNOWN (int): Aspect is not applicable in the analyzed language or is not predicted.
          PERFECTIVE (int): Perfective
          IMPERFECTIVE (int): Imperfective
          PROGRESSIVE (int): Progressive
        """

        ASPECT_UNKNOWN = 0
        PERFECTIVE = 1
        IMPERFECTIVE = 2
        PROGRESSIVE = 3

    class Case(enum.IntEnum):
        """
        The grammatical function performed by a noun or pronoun in a phrase,
        clause, or sentence. In some languages, other parts of speech, such as
        adjective and determiner, take case inflection in agreement with the noun.

        Attributes:
          CASE_UNKNOWN (int): Case is not applicable in the analyzed language or is not predicted.
          ACCUSATIVE (int): Accusative
          ADVERBIAL (int): Adverbial
          COMPLEMENTIVE (int): Complementive
          DATIVE (int): Dative
          GENITIVE (int): Genitive
          INSTRUMENTAL (int): Instrumental
          LOCATIVE (int): Locative
          NOMINATIVE (int): Nominative
          OBLIQUE (int): Oblique
          PARTITIVE (int): Partitive
          PREPOSITIONAL (int): Prepositional
          REFLEXIVE_CASE (int): Reflexive
          RELATIVE_CASE (int): Relative
          VOCATIVE (int): Vocative
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

    class Form(enum.IntEnum):
        """
        Depending on the language, Form can be categorizing different forms of
        verbs, adjectives, adverbs, etc. For example, categorizing inflected
        endings of verbs and adjectives or distinguishing between short and long
        forms of adjectives and participles

        Attributes:
          FORM_UNKNOWN (int): Form is not applicable in the analyzed language or is not predicted.
          ADNOMIAL (int): Adnomial
          AUXILIARY (int): Auxiliary
          COMPLEMENTIZER (int): Complementizer
          FINAL_ENDING (int): Final ending
          GERUND (int): Gerund
          REALIS (int): Realis
          IRREALIS (int): Irrealis
          SHORT (int): Short form
          LONG (int): Long form
          ORDER (int): Order form
          SPECIFIC (int): Specific form
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

    class Gender(enum.IntEnum):
        """
        Gender classes of nouns reflected in the behaviour of associated words.

        Attributes:
          GENDER_UNKNOWN (int): Gender is not applicable in the analyzed language or is not predicted.
          FEMININE (int): Feminine
          MASCULINE (int): Masculine
          NEUTER (int): Neuter
        """

        GENDER_UNKNOWN = 0
        FEMININE = 1
        MASCULINE = 2
        NEUTER = 3

    class Mood(enum.IntEnum):
        """
        The grammatical feature of verbs, used for showing modality and attitude.

        Attributes:
          MOOD_UNKNOWN (int): Mood is not applicable in the analyzed language or is not predicted.
          CONDITIONAL_MOOD (int): Conditional
          IMPERATIVE (int): Imperative
          INDICATIVE (int): Indicative
          INTERROGATIVE (int): Interrogative
          JUSSIVE (int): Jussive
          SUBJUNCTIVE (int): Subjunctive
        """

        MOOD_UNKNOWN = 0
        CONDITIONAL_MOOD = 1
        IMPERATIVE = 2
        INDICATIVE = 3
        INTERROGATIVE = 4
        JUSSIVE = 5
        SUBJUNCTIVE = 6

    class Number(enum.IntEnum):
        """
        Count distinctions.

        Attributes:
          NUMBER_UNKNOWN (int): Number is not applicable in the analyzed language or is not predicted.
          SINGULAR (int): Singular
          PLURAL (int): Plural
          DUAL (int): Dual
        """

        NUMBER_UNKNOWN = 0
        SINGULAR = 1
        PLURAL = 2
        DUAL = 3

    class Person(enum.IntEnum):
        """
        The distinction between the speaker, second person, third person, etc.

        Attributes:
          PERSON_UNKNOWN (int): Person is not applicable in the analyzed language or is not predicted.
          FIRST (int): First
          SECOND (int): Second
          THIRD (int): Third
          REFLEXIVE_PERSON (int): Reflexive
        """

        PERSON_UNKNOWN = 0
        FIRST = 1
        SECOND = 2
        THIRD = 3
        REFLEXIVE_PERSON = 4

    class Proper(enum.IntEnum):
        """
        This category shows if the token is part of a proper name.

        Attributes:
          PROPER_UNKNOWN (int): Proper is not applicable in the analyzed language or is not predicted.
          PROPER (int): Proper
          NOT_PROPER (int): Not proper
        """

        PROPER_UNKNOWN = 0
        PROPER = 1
        NOT_PROPER = 2

    class Reciprocity(enum.IntEnum):
        """
        Reciprocal features of a pronoun.

        Attributes:
          RECIPROCITY_UNKNOWN (int): Reciprocity is not applicable in the analyzed language or is not
          predicted.
          RECIPROCAL (int): Reciprocal
          NON_RECIPROCAL (int): Non-reciprocal
        """

        RECIPROCITY_UNKNOWN = 0
        RECIPROCAL = 1
        NON_RECIPROCAL = 2

    class Tag(enum.IntEnum):
        """
        The part of speech tags enum.

        Attributes:
          UNKNOWN (int): Unknown
          ADJ (int): Adjective
          ADP (int): Adposition (preposition and postposition)
          ADV (int): Adverb
          CONJ (int): Conjunction
          DET (int): Determiner
          NOUN (int): Noun (common and proper)
          NUM (int): Cardinal number
          PRON (int): Pronoun
          PRT (int): Particle or other function word
          PUNCT (int): Punctuation
          VERB (int): Verb (all tenses and modes)
          X (int): Other: foreign words, typos, abbreviations
          AFFIX (int): Affix
        """

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

    class Tense(enum.IntEnum):
        """
        Time reference.

        Attributes:
          TENSE_UNKNOWN (int): Tense is not applicable in the analyzed language or is not predicted.
          CONDITIONAL_TENSE (int): Conditional
          FUTURE (int): Future
          PAST (int): Past
          PRESENT (int): Present
          IMPERFECT (int): Imperfect
          PLUPERFECT (int): Pluperfect
        """

        TENSE_UNKNOWN = 0
        CONDITIONAL_TENSE = 1
        FUTURE = 2
        PAST = 3
        PRESENT = 4
        IMPERFECT = 5
        PLUPERFECT = 6

    class Voice(enum.IntEnum):
        """
        The relationship between the action that a verb expresses and the
        participants identified by its arguments.

        Attributes:
          VOICE_UNKNOWN (int): Voice is not applicable in the analyzed language or is not predicted.
          ACTIVE (int): Active
          CAUSATIVE (int): Causative
          PASSIVE (int): Passive
        """

        VOICE_UNKNOWN = 0
        ACTIVE = 1
        CAUSATIVE = 2
        PASSIVE = 3
