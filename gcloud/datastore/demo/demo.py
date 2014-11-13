# pragma NO COVER
# Welcome to the gCloud Datastore Demo! (hit enter)

# We're going to walk through some of the basics...
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and getting a dataset:
from gcloud.datastore import demo
dataset = demo.get_dataset()

# Let's create a new entity of type "Thing" and name it 'Toy':
toy = dataset.entity('Thing')
toy.update({'name': 'Toy'})

# Now let's save it to our datastore:
toy.save()

# If we look it up by its key, we should find it...
print(dataset.get_entities([toy.key()]))

# And we should be able to delete it...
toy.delete()

# Since we deleted it, if we do another lookup it shouldn't be there again:
print(dataset.get_entities([toy.key()]))

# Now let's try a more advanced query.
# We'll start by look at all Thing entities:
query = dataset.query().kind('Thing')

# Let's look at the first two.
print(query.limit(2).fetch())

# Now let's check for Thing entities named 'Computer'
print(query.filter('name =', 'Computer').fetch())

# If you want to filter by multiple attributes,
# you can string .filter() calls together.
print(query.filter('name =', 'Computer').filter('age =', 10).fetch())

# You can also work inside a transaction.
# (Check the official docs for explanations of what's happening here.)
with dataset.transaction():
    print('Creating and savng an entity...')
    thing = dataset.entity('Thing')
    thing.key(thing.key().name('foo'))
    thing['age'] = 10
    thing.save()

    print('Creating and saving another entity...')
    thing2 = dataset.entity('Thing')
    thing2.key(thing2.key().name('bar'))
    thing2['age'] = 15
    thing2.save()

    print('Committing the transaction...')

# Now that the transaction is commited, let's delete the entities.
print(thing.delete(), thing2.delete())

# To rollback a transaction, just call .rollback()
with dataset.transaction() as t:
    thing = dataset.entity('Thing')
    thing.key(thing.key().name('another'))
    thing.save()
    t.rollback()

# Let's check if the entity was actually created:
created = dataset.get_entities([thing.key()])
print('yes' if created else 'no')

# Remember, a key won't be complete until the transaction is commited.
# That is, while inside the transaction block, thing.key() will be incomplete.
with dataset.transaction():
    thing = dataset.entity('Thing')
    thing.save()
    print(thing.key())  # This will be partial

print(thing.key())  # This will be complete

# Now let's delete the entity.
thing.delete()
