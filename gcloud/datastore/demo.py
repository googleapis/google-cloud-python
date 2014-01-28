import os.path

import gcloud.datastore
from gcloud.datastore.key import Key


__all__ = ['CLIENT_EMAIL', 'DATASET_ID', 'PRIVATE_KEY_PATH',
           'get_dataset', 'main']


DATASET_ID = 'gcloud-datastore-demo'
CLIENT_EMAIL = '754762820716-gimou6egs2hq1rli7el2t621a1b04t9i@developer.gserviceaccount.com'
PRIVATE_KEY_PATH = os.path.dirname(gcloud.datastore.__file__) + '/demo.key'


def get_dataset():
  """A helper method to be used in a Python console."""

  return gcloud.datastore.get_dataset(
      DATASET_ID, CLIENT_EMAIL, PRIVATE_KEY_PATH)


def main():
  """A full example script demonstrating how to use the client."""

  # Establish a connection to use for querying.
  connection = gcloud.datastore.get_connection(CLIENT_EMAIL, PRIVATE_KEY_PATH)
  dataset = connection.dataset(DATASET_ID)

  print '\nCreating a new Thing called Toy...'
  toy = dataset.entity('Thing')
  toy.update({'name': 'Toy', 'some_int_value': 1234})
  toy.save()

  print '\nLooking up the Toy...'
  print dataset.get_entities([toy.key()])

  print '\nDeleting the Toy...'
  toy.delete()

  print '\nLooking up the Toy again (this should be empty)...'
  print dataset.get_entities([toy.key()])

  query = dataset.query().kind('Thing')

  print '\nShowing first 2 Things...'
  print query.limit(2).fetch()

  print '\nShowing Things named Computer...'
  print query.filter('name =', 'Computer').fetch()

  print '\nFilter by multiple things...'
  print query.filter('name =', 'Computer').filter(
      'my_int_value =', 1234).fetch()

  print '\nStarting a transaction...'
  with dataset.transaction():
    print 'Creating and savng an entity...'
    thing = dataset.entity('Thing')
    thing.key(thing.key().name('foo'))
    thing['age'] = 10
    thing.save()

    print 'Creating and saving another entity...'
    thing2 = dataset.entity('Thing')
    thing2.key(thing2.key().name('bar'))
    thing2['age'] = 15
    thing2.save()

    print 'Committing the transaction...',

  print 'done.'

  print '\nDeleting the entities...'
  print thing.delete(), thing2.delete()

  print '\nStarting another transaction...'
  with dataset.transaction() as t:
    print 'Creating an entity...'
    thing = dataset.entity('Thing')
    thing.key(thing.key().name('another'))
    thing.save()

    print 'Rolling back the transaction...'
    t.rollback()

  print 'Was the entity actually created? ... ',

  if dataset.get_entities([thing.key()]):
    print 'yes.'
  else:
    print 'no.'

  print '\nStarting one more transaction...'
  with dataset.transaction():
    print 'Creating a simple thing'
    thing = dataset.entity('Thing')
    thing.save()

    print 'Before committing, the key should be incomplete...', thing.key()

  print 'After committing, the key should be complete...', thing.key()

  print 'Deleting the entity...'
  thing.delete()


if __name__ == '__main__':
  main()
