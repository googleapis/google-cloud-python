from code import interact
import os.path
import sys
import time

from gcloud import storage


__all__ = ['CLIENT_EMAIL', 'PRIVATE_KEY_PATH', 'PROJECT_NAME',
           'get_connection', 'main']


CLIENT_EMAIL = '606734090113-6ink7iugcv89da9sru7lii8bs3i0obqg@developer.gserviceaccount.com'
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(storage.__file__), 'demo.key')
PROJECT_NAME = 'gcloud-storage-demo'

extra_newline = False
code_globals, code_locals = globals(), locals()


def get_connection():
  return storage.get_connection(PROJECT_NAME, CLIENT_EMAIL, PRIVATE_KEY_PATH)


def write(*strings):
  # Add an extra newline if necessary.
  global extra_newline
  if extra_newline:
    print

  for string in strings:
    print string
  raw_input()

  # We don't need an extra newline after this.
  extra_newline = False


def code(string, comment=None):
  keypress_time = 0.05

  print '>>> ',
  for char in string:
    time.sleep(keypress_time)
    sys.stdout.write(char)
    sys.stdout.flush()

  if comment:
    sys.stdout.write('  # %s' % comment)

  # Wait for an enter key before continuing...
  raw_input()

  # Yes, this is crazy unsafe... but it's demo code.
  # Globalize these so our imports hang around...
  global code_globals
  global code_locals
  exec(string, code_globals, code_locals)

  # In the next non-code piece, we need an extra newline.
  global extra_newline
  extra_newline = True


def main():
  write('Welcome to the gCloud Storage Demo! (hit enter)')
  write('We\'re going to walk through some of the basics...',
          'Don\'t worry though. You don\'t need to do anything, just keep hitting enter...')

  write('Let\'s start by importing the demo module and getting a connection:')
  code('from gcloud.storage import demo')
  code('connection = demo.get_connection()')

  write('OK, now let\'s look at all of the buckets...')
  code('print connection.get_all_buckets()',
       'This might take a second...')

  write('Now let\'s create a new bucket...')
  code('import time')
  code('bucket_name = ("bucket-%s" % time.time()).replace(".", "")',
       'Get rid of dots...')
  code('print bucket_name')
  code('bucket = connection.create_bucket(bucket_name)')
  code('print bucket')

  write('Let\'s look at all of the buckets again...')
  code('print connection.get_all_buckets()')

  write('How about we create a new key inside this bucket.')
  code('key = bucket.new_key("my-new-file.txt")')

  write('Now let\'s put some data in there.')
  code('key.set_contents_from_string("this is some data!")')

  write('... and we can read that data back again.')
  code('print key.get_contents_as_string()')

  write('Now let\'s delete that key.')
  code('print key.delete()')

  write('And now that we\'re done, let\'s delete that bucket...')
  code('print bucket.delete()')

  write('Alright! That\'s all!',
          'Here\'s an interactive prompt for you now...')

  global code_locals
  interact('(Hit CTRL-D to exit...)', local=code_locals)


if __name__ == '__main__':
  main()
