"""The YCSB cient in Python.

Usage:

  # Set up instance and load data into database.

  # Set up environment variables. You should use your own credentials and gclod
  # project.
  $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
  $ export GCLOUD_PROJECT=gcloud-project-name

  # Run the benchmark.
  $ python spanner/benchmark/ycsb.py run -P pkb/workloada -p table=usertable \
    -p cloudspanner.instance=ycsb-542756a4 -p recordcount=5000 \
    -p operationcount=100 -p cloudspanner.database=ycsb -p num_worker=1

  # To make a package so it can work with PerfKitBenchmarker.
  $ cd spanner; tar -cvzf ycsb-python.0.0.5.tar.gz benchmark/*

"""

import numpy
import optparse
import random
import string
import threading
import timeit

from google.cloud import spanner


KEYS = []
OPERATIONS = ['readproportion', 'updateproportion', 'scanproportion',
              'insertproportion']


def ParseOptions():
  """Parses options."""
  parser = optparse.OptionParser()
  parser.add_option('-P', '--workload', action='store', dest='workload',
                    default='', help='The path to a YCSB workload file.')
  parser.add_option('-p', '--parameter', action='append', dest='parameters',
                    default=[], help='The key=value pair of parameter.')
  parser.add_option('-b', '--num_bucket', action='store', type='int',
                    dest='num_bucket', default=1000,
                    help='The number of buckets in output.')

  options, args = parser.parse_args()

  parameters = {}
  parameters['command'] = args[0]
  parameters['num_bucket'] = options.num_bucket

  for parameter in options.parameters:
    parts = parameter.strip().split('=')
    parameters[parts[0]] = parts[1]

  with open(options.workload, 'r') as f:
    for line in f.readlines():
      parts = line.split('=')
      key = parts[0].strip()
      if key in OPERATIONS:
        parameters[key] = parts[1].strip()

  return parameters


def OpenDatabase(parameters):
  """Opens a database specified by the parameters from ParseOptions()."""
  spanner_client = spanner.Client()
  instance_id = parameters['cloudspanner.instance']
  instance = spanner_client.instance(instance_id)
  database_id = parameters['cloudspanner.database']
  pool = spanner.BurstyPool(int(parameters['num_worker']))
  database = instance.database(database_id, pool=pool)

  return database


def LoadKeys(database, parameters):
  """Loads keys from database."""
  global KEYS
  KEYS = []
  results = database.execute_sql('SELECT u.id FROM %s u' % parameters['table'])

  for row in results:
    KEYS.append(row[0])


def Read(database, table, key):
  """Does a single read operation."""
  with database.snapshot() as snapshot:
    result = snapshot.execute_sql('SELECT u.* FROM %s u WHERE u.id="%s"' %
                                  (table, key))
    for row in result:
      key = row[0]
      for i in range(10):
        field = row[i + 1]


def Update(database, table, key):
  """Does a single update operation."""
  field = random.randrange(10)
  value = ''.join(random.choice(string.printable) for i in range(100))
  with database.batch() as batch:
    batch.update(table=table, columns=('id', 'field%d' % field),
                 values=[(key, value)])


def Insert(database, table, key):
  """Does a single insert operation."""
  raise Exception('Insert is not implemented.')


def Scan(database, table, key):
  """Does a single scan operation."""
  raise Exception('Scan is not implemented.')


def DoOperation(database, table, operation, latencies_ms):
  """Does a single operation and records latency."""
  key = random.choice(KEYS)
  start = timeit.default_timer()
  if operation == 'read':
    Read(database, table, key)
  elif operation == 'update':
    Update(database, table,  key)
  elif operation == 'insert':
    Insert(database, table, key)
  elif operation == 'scan':
    Scan(database, table, key)
  else:
    raise Exception('Unknown operation: %s' % operation)
  end = timeit.default_timer()
  latencies_ms[operation].append((end - start) * 1000)


def AggregateMetrics(latencies_ms, duration_ms, num_bucket):
  """Aggregates metrics."""
  overall_op_count = 0
  op_counts = {}
  for operation in latencies_ms.keys():
    op_counts[operation] = len(latencies_ms[operation])
    overall_op_count += op_counts[operation]

  print '[OVERALL], RumTime(ms), %f' % duration_ms
  print '[OVERALL], Throughput(ops/sec), %f' % (float(overall_op_count) /
                                                duration_ms * 1000.0)

  for operation in op_counts.keys():
    operation_upper = operation.upper()
    print '[%s], Operations, %d' % (operation_upper, op_counts[operation])
    print '[%s], AverageLatency(us), %f' % (
        operation_upper, numpy.average(latencies_ms[operation]) * 1000.0)
    print '[%s], LatencyVariance(us), %f' % (
        operation_upper, numpy.std(latencies_ms[operation]) * 1000.0)
    print '[%s], MinLatency(us), %f' % (
        operation_upper, min(latencies_ms[operation]) * 1000.0)
    print '[%s], MaxLatency(us), %f' % (
        operation_upper, max(latencies_ms[operation]) * 1000.0)
    print '[%s], 95thPercentileLatency(us), %f' % (
        operation_upper,
        numpy.percentile(latencies_ms[operation], 95.0) * 1000.0)
    print '[%s], 99thPercentileLatency(us), %f' % (
        operation_upper,
        numpy.percentile(latencies_ms[operation], 99.0) * 1000.0)
    print '[%s], 99.9thPercentileLatency(us), %f' % (
        operation_upper,
        numpy.percentile(latencies_ms[operation], 99.9) * 1000.0)
    print '[%s], Return=OK, %d' % (operation_upper, op_counts[operation])
    latency_array = numpy.array(latencies_ms[operation])
    for j in range(num_bucket):
      print '[%s], %d, %d' % (
          operation_upper, j,
          ((j <= latency_array) & (latency_array < (j + 1))).sum())
    print '[%s], >%d, %d' % (
          operation_upper, num_bucket, (num_bucket <= latency_array).sum())


class WorkloadThread(threading.Thread):
  """A single thread running workload."""

  def __init__(self, database, parameters, total_weight, weights, operations):
    threading.Thread.__init__(self)
    self._database = database
    self._parameters = parameters
    self._total_weight = total_weight
    self._weights = weights
    self._operations = operations
    self._latencies_ms = {}
    for operation in self._operations:
      self._latencies_ms[operation] = []

  def run(self):
    """Run a single thread of the workload."""
    i = 0
    operation_count = int(self._parameters['operationcount'])
    while i < operation_count:
      i += 1
      weight = random.uniform(0, self._total_weight)
      for j in range(len(self._weights)):
        if weight <= self._weights[j]:
          DoOperation(self._database, self._parameters['table'],
                      self._operations[j], self._latencies_ms)
          break

  def latencies_ms(self):
    """Returns the latencies."""
    return self._latencies_ms


def RunWorkload(database, parameters):
  """Runs workload against the database."""
  total_weight = 0.0
  weights = []
  operations = []
  latencies_ms = {}
  for operation in OPERATIONS:
    weight = float(parameters[operation])
    if weight <= 0.0:
      continue
    total_weight += weight
    op_code = operation.split('proportion')[0]
    operations.append(op_code)
    weights.append(total_weight)
    latencies_ms[op_code] = []

  threads = []
  start = timeit.default_timer()
  for i in range(int(parameters['num_worker'])):
    thread = WorkloadThread(database, parameters, total_weight, weights,
                            operations)
    thread.start()
    threads.append(thread)

  for thread in threads:
    thread.join()
  end = timeit.default_timer()

  for thread in threads:
    thread_latencies_ms = thread.latencies_ms()
    for key in latencies_ms.keys():
      latencies_ms[key].extend(thread_latencies_ms[key])

  AggregateMetrics(latencies_ms, (end - start) * 1000.0,
                   parameters['num_bucket'])


if __name__ == '__main__':
  parameters = ParseOptions()
  if parameters['command'] == 'run':
    if 'cloudspanner.channels' in parameters:
      assert parameters['cloudspanner.channels'] == 1, ('Python doesn\'t '
                                                        'support channels > 1.')
    database = OpenDatabase(parameters)
    LoadKeys(database, parameters)
    RunWorkload(database, parameters)
  else:
    raise Exception('Command %s not implemented.' % parameters['command'])
