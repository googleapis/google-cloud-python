# Copyright 2016-2017 Google Inc.
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

"""Google Cloud Natural Language API helpers for tokenized text.

The ``annotateText`` method, when used with the "syntax" feature,
breaks a document down into tokens and sentences.
"""


class PartOfSpeech(object):
    """A Google Cloud Natural Language API Part of speech object.

    These are the grammatical categories of the matched token in
    the sentence. https://cloud.google.com/natural-language/docs\
    /reference/rest/v1/Token#PartOfSpeech

    :type aspect: str
    :param aspect: The grammatical aspect. https://cloud.google\
                   .com/natural-language/docs/reference/rest/v1/\
                   Token#Aspect

    :type reciprocity: str
    :param reciprocity: The grammatical reciprocity. https://\
                        cloud.google.com/natural-language/docs/reference\
                        /rest/v1/Token#Reciprocity

    :type case: str
    :param case: The grammatical case. https://cloud.google.com/\
                 natural-language/docs/reference/rest/v1/Token#Case

    :type mood: str
    :param mood: The grammatical mood. https://cloud.google.com/\
                 natural-language/docs/reference/rest/v1/Token#Mood

    :type tag: str
    :param tag: The part of speech tag. https://cloud.google.com/natural\
                -language/docs/reference/rest/v1/Token#Tag

    :type person: str
    :param person: The grammatical person. https://cloud.google.com/\
                   natural-language/docs/reference/rest/v1/Token#Person

    :type number: str
    :param number: The grammatical number. https://cloud.google.com/natural\
                   -language/docs/reference/rest/v1/Token#Number

    :type tense: str
    :param tense: The grammatical tense. https://cloud.google.com/natural\
                  -language/docs/reference/rest/v1/Token#Tense

    :type form: str
    :param form: The grammatical form. https://cloud.google.com/natural\
                 -language/docs/reference/rest/v1/Token#Form

    :type proper: str
    :param proper: The grammatical properness. https://cloud.google.com/\
                   natural-language/docs/reference/rest/v1/Token#Proper

    :type voice: str
    :param voice: The grammatical voice. https://cloud.google.com/\
                  natural-language/docs/reference/rest/v1/Token#Voice

    :type gender: str
    :param gender: The grammatical gender. https://cloud.google.com/\
                   natural-language/docs/reference/rest/v1/Token#Gender
    """

    UNKNOWN = 'UNKNOWN'
    """Unknown part of speech."""

    ADJECTIVE = 'ADJ'
    """Part of speech: Adjective."""

    ADPOSITION = 'ADP'
    """Adposition (preposition and postposition)."""

    ADVERB = 'ADV'
    """Adverb."""

    CONJUNCTION = 'CONJ'
    """Conjunction."""

    DETERMINER = 'DET'
    """Determiner."""

    NOUN = 'NOUN'
    """Noun (common and proper)."""

    CARDINAL_NUMBER = 'NUM'
    """Cardinal number."""

    PRONOUN = 'PRON'
    """Pronoun."""

    PARTICIPLE = 'PRT'
    """Particle or other function word."""

    PUNCTUATION = 'PUNCT'
    """Punctuation."""

    VERB = 'VERB'
    """Verb (all tenses and modes)."""

    OTHER = 'X'
    """Other: foreign words, typos, abbreviations."""

    AFFIX = 'AFFIX'
    """Affix."""

    _REVERSE_MAP = {
        'UNKNOWN': 'UNKNOWN',
        'ADJ': 'ADJECTIVE',
        'ADP': 'ADPOSITION',
        'ADV': 'ADVERB',
        'CONJ': 'CONJUNCTION',
        'DET': 'DETERMINER',
        'NOUN': 'NOUN',
        'NUM': 'CARDINAL_NUMBER',
        'PRON': 'PRONOUN',
        'PRT': 'PARTICIPLE',
        'PUNCT': 'PUNCTUATION',
        'VERB': 'VERB',
        'X': 'OTHER',
        'AFFIX': 'AFFIX',
    }

    def __init__(self, aspect, reciprocity, case, mood, tag, person,
                 number, tense, form, proper, voice, gender):
        self.aspect = aspect
        self.reciprocity = reciprocity
        self.case = case
        self.mood = mood
        self.tag = tag
        self.person = person
        self.number = number
        self.tense = tense
        self.form = form
        self.proper = proper
        self.voice = voice
        self.gender = gender

    @classmethod
    def from_api_repr(cls, payload):
        return PartOfSpeech(aspect=payload['aspect'],
                            reciprocity=payload['reciprocity'],
                            case=payload['case'],
                            mood=payload['mood'],
                            tag=payload['tag'],
                            person=payload['person'],
                            number=payload['number'],
                            tense=payload['tense'],
                            form=payload['form'],
                            proper=payload['proper'],
                            voice=payload['voice'],
                            gender=payload['gender'])

    @classmethod
    def reverse(cls, tag):
        """Reverses the API's enum name for the one on this class.

        For example::

            >>> PartOfSpeech.OTHER
            'X'
            >>> PartOfSpeech.reverse('X')
            'OTHER'

        :rtype: str
        :returns: The attribute name corresponding to the API part of
                  speech enum.
        """
        return cls._REVERSE_MAP[tag]


class Token(object):
    """A Google Cloud Natural Language API token object.

    .. _Token message: https://cloud.google.com/natural-language/reference\
                       /rest/v1/documents/annotateText#Token
    .. _Lemma: https://en.wikipedia.org/wiki/Lemma_(morphology)
    .. _Label enum: https://cloud.google.com/natural-language/reference/\
                    rest/v1/documents/annotateText#Label

    See `Token message`_.

    :type text_content: str
    :param text_content: The text that the token is composed of.

    :type text_begin: int
    :param text_begin: The beginning offset of the content in the original
                       document according to the encoding type specified
                       in the API request.

    :type part_of_speech: PartOfSpeech
    :param part_of_speech: An object representing the Part of Speech of the
                           token with it's properties.

    :type edge_index: int
    :param edge_index: The head of this token in the dependency tree. This is
                       the index of the token which has an arc going to this
                       token. The index is the position of the token in the
                       array of tokens returned by the API method. If this
                       token is a root token, then the ``edge_index`` is
                       its own index.

    :type edge_label: str
    :param edge_label: See `Label enum`_.

    :type lemma: str
    :param lemma: The `Lemma`_ of the token.
    """

    def __init__(self, text_content, text_begin, part_of_speech,
                 edge_index, edge_label, lemma):
        self.text_content = text_content
        self.text_begin = text_begin
        self.part_of_speech = part_of_speech
        self.edge_index = edge_index
        self.edge_label = edge_label
        self.lemma = lemma

    @classmethod
    def from_api_repr(cls, payload):
        """Convert a token from the JSON API into a :class:`Token`.

        :param payload: dict
        :type payload: The value from the backend.

        :rtype: :class:`Token`
        :returns: The token parsed from the API representation.
        """
        text_span = payload['text']
        text_content = text_span['content']
        text_begin = text_span['beginOffset']
        part_of_speech = PartOfSpeech.from_api_repr(payload['partOfSpeech'])
        edge = payload['dependencyEdge']
        edge_index = edge['headTokenIndex']
        edge_label = edge['label']
        lemma = payload['lemma']
        return cls(text_content, text_begin, part_of_speech,
                   edge_index, edge_label, lemma)
