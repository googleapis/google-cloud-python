# Copyright 2014 Google Inc. All rights reserved.
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
# Welcome to the gCloud Datastore Demo! (hit enter)
# We're going to walk through some of the basics...
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and initializing our connection.
from gcloud.datastore import demo
demo.initialize()

# Let's create a new entity of type "Thing" and name it 'Toy':
from gcloud.datastore.key import Key
key = Key('Thing')
from gcloud.datastore.entity import Entity
toy = Entity(key)
toy.update({'name': 'Toy'})

# Now let's save it to our datastore:
toy.save()

# If we look it up by its key, we should find it...
from gcloud.datastore import get
print(get([toy.key]))

# And we should be able to delete it...
toy.key.delete()

# Since we deleted it, if we do another lookup it shouldn't be there again:
print(get([toy.key]))

# Now let's try a more advanced query.
# First, let's create some entities.
SAMPLE_DATA = [
    (1234, 'Computer', 10),
    (2345, 'Computer', 8),
    (3456, 'Laptop', 10),
    (4567, 'Printer', 11),
    (5678, 'Printer', 12),
    (6789, 'Computer', 13)]
samples = []
for id, name, age in SAMPLE_DATA:
    key = Key('Thing', id)
    samples.append(key)
    entity = Entity(key)
    entity['name'] = name
    entity['age'] = age
    entity.save()
# We'll start by look at all Thing entities:
from gcloud.datastore.query import Query
query = Query(kind='Thing')

# Let's look at the first two.
print(list(query.fetch(limit=2)))

# Now let's check for Thing entities named 'Computer'
query.add_filter('name', '=', 'Computer')
print(list(query.fetch()))

# If you want to filter by multiple attributes,
# you can call .add_filter multiple times on the query.
query.add_filter('age', '=', 10)
print(list(query.fetch()))

# Now delete them.
print([key.delete() for key in samples])

# You can also work inside a transaction.
# (Check the official docs for explanations of what's happening here.)
from gcloud.datastore.transaction import Transaction
with Transaction():
    print('Creating and savng an entity...')
    key = Key('Thing', 'foo')
    thing = Entity(key)
    thing['age'] = 10
    thing.save()

    print('Creating and saving another entity...')
    key2 = Key('Thing', 'bar')
    thing2 = Entity(key2)
    thing2['age'] = 15
    thing2.save()

    print('Committing the transaction...')

# Now that the transaction is commited, let's delete the entities.
print(key.delete(), key2.delete())

# To rollback a transaction, just call .rollback()
with Transaction() as t:
    key = Key('Thing', 'another')
    thing = Entity(key)
    thing.save()
    t.rollback()

# Let's check if the entity was actually created:
created = get([key])
print('yes' if created else 'no')

# Remember, a key won't be complete until the transaction is commited.
# That is, while inside the transaction block, thing.key will be incomplete.
with Transaction():
    key = Key('Thing')  # partial
    thing = Entity(key)
    thing.save()
    print(thing.key)  # This will still be partial

print(thing.key)  # This will be complete

# Now let's delete the entity.
thing.key.delete()
