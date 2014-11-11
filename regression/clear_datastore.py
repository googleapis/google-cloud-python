"""Script to populate datastore with regression test data."""


# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


FETCH_MAX = 20
ALL_KINDS = [
    'Character',
    'Company',
    'Kind',
    'Person',
    'Post',
]


def remove_kind(dataset, kind):
    dataset_id = dataset.id()
    connection = dataset.connection()

    with dataset.transaction():
        query = dataset.query(kind=kind).limit(
            FETCH_MAX).projection(['__key__'])
        results = []
        more_results = True
        while more_results:
            # Make new query.
            if query._cursor is not None:
                query = query.with_cursor(query._cursor)

            curr_results = query.fetch()
            results.extend(curr_results)

            more_results = len(curr_results) == FETCH_MAX

        # Now that we have all results, we seek to delete.
        key_pbs = [entity.key().to_protobuf() for entity in results]
        connection.delete_entities(dataset_id, key_pbs)


def remove_all_entities():
    print 'This command will remove all entities for the following kinds:'
    print '\n'.join(['- ' + val for val in ALL_KINDS])
    response = raw_input('Is this OK [y/n]? ')
    if response.lower() != 'y':
        print 'Doing nothing.'
        return

    dataset = regression_utils.get_dataset()
    for kind in ALL_KINDS:
        remove_kind(dataset, kind)


if __name__ == '__main__':
    remove_all_entities()
