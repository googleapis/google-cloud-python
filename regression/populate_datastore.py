"""Script to populate datastore with regression test data."""


from gcloud import datastore
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


ANCESTOR = {'kind': 'Book', 'name': 'GoT'}
RICKARD = {'kind': 'Character', 'name': 'Rickard'}
EDDARD = {'kind': 'Character', 'name': 'Eddard'}
KEY_PATHS = [
    [ANCESTOR, RICKARD],
    [ANCESTOR, RICKARD, EDDARD],
    [ANCESTOR,
     {'kind': 'Character', 'name': 'Catelyn'}],
    [ANCESTOR, RICKARD, EDDARD,
     {'kind': 'Character', 'name': 'Arya'}],
    [ANCESTOR, RICKARD, EDDARD,
     {'kind': 'Character', 'name': 'Sansa'}],
    [ANCESTOR, RICKARD, EDDARD,
     {'kind': 'Character', 'name': 'Robb'}],
    [ANCESTOR, RICKARD, EDDARD,
     {'kind': 'Character', 'name': 'Bran'}],
    [ANCESTOR, RICKARD, EDDARD,
     {'kind': 'Character', 'name': 'Jon Snow'}],
]
CHARACTERS = [
    {
        'name': u'Rickard',
        'family': u'Stark',
        'appearances': 0,
        'alive': False,
    }, {
        'name': u'Eddard',
        'family': u'Stark',
        'appearances': 9,
        'alive': False,
    }, {
        'name': u'Catelyn',
        'family': [u'Stark', u'Tully'],
        'appearances': 26,
        'alive': False,
    }, {
        'name': u'Arya',
        'family': u'Stark',
        'appearances': 33,
        'alive': True,
    }, {
        'name': u'Sansa',
        'family': u'Stark',
        'appearances': 31,
        'alive': True,
    }, {
        'name': u'Robb',
        'family': u'Stark',
        'appearances': 22,
        'alive': False,
    }, {
        'name': u'Bran',
        'family': u'Stark',
        'appearances': 25,
        'alive': True,
    }, {
        'name': u'Jon Snow',
        'family': u'Stark',
        'appearances': 32,
        'alive': True,
    },
]


def add_characters():
    dataset = regression_utils.get_dataset()
    with dataset.transaction():
        for key_path, character in zip(KEY_PATHS, CHARACTERS):
            if key_path[-1]['name'] != character['name']:
                raise ValueError(('Character and key don\'t agree',
                                  key_path, character))
            key = datastore.key.Key(path=key_path)
            entity = datastore.entity.Entity(dataset=dataset).key(key)
            entity.update(character)
            entity.save()
            print 'Adding Character %s %s' % (character['name'],
                                              character['family'])


if __name__ == '__main__':
    add_characters()
