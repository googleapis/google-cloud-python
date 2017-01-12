import os

our_keys = sorted(key for key in os.environ.keys()
                  if 'travis' in key.lower())
if our_keys:
    for key in our_keys:
        print('%s: %s' % (key, os.getenv(key)))
else:
    print('No keys here, sorry')
# Added just for a commit.
