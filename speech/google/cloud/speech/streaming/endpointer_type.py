class EndpointerType(object):
    ENDPOINTER_EVENT_UNSPECIFIED = 0
    START_OF_SPEECH = 1
    END_OF_SPEECH = 2
    END_OF_AUDIO = 3
    END_OF_UTTERANCE = 4

    reverse_map = {
        0: 'ENDPOINTER_EVENT_UNSPECIFIED',
        1: 'START_OF_SPEECH',
        2: 'END_OF_SPEECH',
        3: 'END_OF_AUDIO',
        4: 'END_OF_UTTERANCE'
    }
