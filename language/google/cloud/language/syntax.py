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
    """Part of speech of a :class:`Token`."""

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

    :type part_of_speech: str
    :param part_of_speech: The part of speech of the token. See
                           :class:`PartOfSpeech` for possible values.

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
        part_of_speech = payload['partOfSpeech']['tag']
        edge = payload['dependencyEdge']
        edge_index = edge['headTokenIndex']
        edge_label = edge['label']
        lemma = payload['lemma']
        return cls(text_content, text_begin, part_of_speech,
                   edge_index, edge_label, lemma)
