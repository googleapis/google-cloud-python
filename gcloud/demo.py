from code import interact
import os.path
import sys
import time

from gcloud import storage


__all__ = ['CLIENT_EMAIL', 'PRIVATE_KEY_PATH', 'PROJECT_NAME',
           'get_connection', 'main']


CLIENT_EMAIL = '606734090113-6ink7iugcv89da9sru7lii8bs3i0obqg@developer.gserviceaccount.com'
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'demo.key')
PROJECT_NAME = 'gcloud-storage-demo'

extra_newline = False
code_globals, code_locals = globals(), locals()


def get_storage_connection():
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

def is_empty(line): return not bool(line.strip())
def is_comment(line): return line.startswith('#')
def is_code(line): return not is_empty(line) and not is_comment(line)

def consume(is_a, lines):
  result = []
  for l in lines:
    if not is_a(l):
      break
    result.append(l)
  return (result, lines[len(result):])

def trim_until_main(lines):
  main_tag = 'if __name__ == \'__main__\':'
  return lines[:lines.index(main_tag)] if main_tag in lines else lines

def run(script):
  with open(script) as f:
    lines = trim_until_main([l.strip() for l in f])
    while len(lines):
      comments, lines = consume(is_comment, lines)
      if comments:
        write(*comments)
      loc, lines = consume(is_code, lines)
      for c in loc:
        code(c)
      _, lines = consume(is_empty, lines)

  global code_locals
  interact('(Hit CTRL-D to exit...)', local=code_locals)
