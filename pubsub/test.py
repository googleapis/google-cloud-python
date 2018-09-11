
import logging
import random
import threading
import time

import google.api_core.exceptions
from google.cloud import pubsub

message_count = 0
message_count_lock = threading.Lock()


def monitor(future, interval=10):
    import datetime
    import textwrap
    import time

    manager = future._manager
    start_time = datetime.datetime.now()

    while not future.done():
        run_time = datetime.datetime.now() - start_time
        rate = message_count / run_time.total_seconds()
        status = textwrap.dedent("""\
            Messages processed: {message_count}
            Rate: {rate:.2f} Messages/second
            Run time: {run_time}
            Load: {load:.2f}
            p99 ack: {ack_deadline} seconds
            Leased Messages: {leased_messages}
            Executor queue size: {work_queue}
            Callback queue size: {callback_size}
            Request queue size: {queue_size}
        """).format(
            message_count=message_count,
            rate=rate,
            run_time=run_time,
            ack_deadline=manager.ack_deadline,
            load=manager.load,
            leased_messages=manager.leaser.message_count,
            work_queue=manager._scheduler._executor._work_queue.qsize(),
            callback_size=manager._scheduler.queue.qsize(),
            queue_size=manager._rpc.pending_requests
        )

        #print('===== Subscriber Monitor =====')
        #print(status)

        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            future.cancel()

    print('waiting on future...')
    print(future.result())
    print('clean exit')


def incr_count():
    # Note: this should be done within a lock as multiple threads mess with
    # this, however, using a lock slows down the program enough to possibly
    # affect the results. Consider this count as incredibly inaccurate and
    # best-effort.
    global message_count
    message_count += 1
    return message_count


def callback(message):
    incr_count()

    # Sleep a random amount of time to simulate a heterogenous load.
    time.sleep(random.uniform(5, 10))

    message.ack()


def main():
    # Enabling logging will output a *ton* of stuff, but it might be helpful.
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger(
        'google.cloud.pubsub_v1.subscriber._protocol.leaser').setLevel('INFO')

    subscriber = pubsub.SubscriberClient()
    topic = 'projects/{project_id}/topics/{topic}'.format(
        project_id='python-docs-samples-tests',
        topic='repro-topic',  # Set this to something appropriate.
    )
    subscription = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id='python-docs-samples-tests',
        sub='repro-sub2',  # Set this to something appropriate.
    )

    try:
        subscriber.create_subscription(subscription, topic)
    except google.api_core.exceptions.AlreadyExists:
        print('subscription exists')
        pass

    future = subscriber.subscribe(
        subscription=subscription,
        callback=callback)

    print('listening')
    monitor(future)


if __name__ == '__main__':
    main()
