

from connection import Connection
from dataset import Dataset


conn = Connection(credentials)
d = Dataset('dataset-id-here', conn, namespace='demo')
#defaults: namespace=None, force=False, read_option="DEFAULT"
"""
a dataset object has 4 mutators and 3 accessors for the datastore
all mutations are immediately and synchronously applied
to the datastore, note however that since the dataset<-->connection
relationship is possibly many-to-one nothing prevents a user
from creating multiple datasets with the same id.
In this case the user is responsible for handling synchronicity
"""

#the first three mutators upsert, insert, and update all have the same usage
d.upsert(
        ('ent','root', 'ent', 'treebeard'),
        dict(hates_sarumon=True, age=9001), #defaults {}
        unindexed=['talking_speed']) #defaults []

#upsert executes regardless of the state of the entity
#update will fail on entities which are not in the datastore
#update and upsert completely overwrite entities
#insert will fail on entities which are already in the datastore

#these three mutations can also insert using a partial id to automatically allocate and id
nameless_orc_key = d.upsert(('orc','root','orc'), dict(is_alive=True))
#the allocated key is returned in it's entirety
#>>> print nameless_orc_key
#('orc','root','orc',int)

d.delete('ent','root','ent','treebeard')
#delete simply uses the key path to delete entities

nameless_orc_props = d.get(*nameless_orc_key)
#get uses the same arguments, but returns the property dict
print nameless_orc_props
#{'is_alive':True}

#get_all() and query() will be covered later, but first...
#what if you want to insert a large number of entities,
#without slamming the datastore with calls

"""
calling d.batch_mutator() returns a batch mutator with the same
initialization settings as the calling dataset
BatchMutators have the same mutators with the same signature
as Datasets, but do not have accessor methods

Instead of immediately applying mutations, BatchMutators
accumulate them within a context, and apply the mutation
upon exiting a context. As such, auto-allocated keys will
not be returned upon insertion of partial keys.
Instead, a user who wants to retrieve theys keys calls
result() outside the context.
"""

b = d.batch_mutator()

try:
    b.insert(('orc','root','orc'))
except:
    print "mutations cannot be made outside of a context"


with b:
    b.insert(('orc','root','orc', 'azog'), dict(is_alive=True))

    azog = d.get('orc','root','orc', 'azog')
    #dataset methods can still be called within a context
    #however, changes made by the BulkMutator are not visible
    #until the context exits
    print azog
    #None

    #on the other hand, BulkMutators can effect data mutated by the
    #dataset during the context
    d.insert(('hobbit','root','hobbit','mary'), dict(underrated=True))

    b.delete('hobbit','root','hobbit','mary')

    for i in range(0,100):
        b.insert(('orc','root','orc'), dict(is_alive=True))


nameless_orc_army = b.result()

mary = d.get('hobbit','root','hobbit','mary')
print mary
#None

#also note that result() does not include keys with user-
#set names or ids
print ('orc','root','orc','azog') in nameless_orc_army
#False


"""
Transactions are objects that behave very similar to BatchMutators
however, they also have the accessor methods from Dataset
(and behave like transactions...)
"""

d.insert(('ent','root','ent','treebeard'), dict(age=9001))

t = d.transaction()

treebeard_props = d.get('ent','root','ent','treebeard')
treebeard_props['age'] += 1
d.update(('ent','root','ent','treebeard'), treebeard_props)

# t takes a snapshot of d, so changes made to d after t is
# initialized will not be visible inside the context



with t:

    d.upsert(('hobbit','root','hobbit','frodo'), dict(underrated=False))
    #additionally, changes made while in the context will not be visible
    #to transactional reads like t.get() or t.query()

    frodo = t.get('hobbit','root','hobbit','frodo')
    print frodo
    #None

    #if you need to get automatically allocate a key to mutate later in
    #a transaction, you can call t.allocate_id(*key)

    important_orc_key = t.allocate_id('orc','root','orc')
    t.upsert(important_orc_key, dict(carrying="explosives!", is_alive=True))


    treebeard_props = t.get('ent','root','ent','treebeard')
    #t.get() gets 'younger' treebeard
    treebeard_props['age'] += 1
    d.update(('ent','root','ent','treebeard'), treebeard_props)

treebeard_props = d.get('ent','root','ent', 'treebeard')

print treebeard_props['age']
#9002


"""
Using GQL is more consistent with the built-in-style of the library
Query syntax uses ordered arguments as the number-args,
and keyword arguments as the named-args, as well as a special arg
called "cursor" which is used for fetching pages
"""

query_string = 'SELECT __key__ FROM @kind OFFSET @cursor WHERE HAS ANCESTOR @1 AND @2=@3'

alive_orcs, more = d.query(
        query_string,
        'KEY(\'orc\', \'root\')',
        'is_alive',
        True,
        kind='orc'
        cursor=None)

while(more):
    more_alive_orcs, more = d.query(
        query_string,
        'KEY(\'orc\', \'root\')',
        'is_alive',
        True,
        kind='orc'
        cursor=more)

    alive_orcs.extend(more_alive_orcs)

print ('orc', 'root', 'orc', 'azog') in alive_orcs
#True

print important_orc_key in alive_orcs
#True
