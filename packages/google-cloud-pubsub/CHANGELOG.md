# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-pubsub/#history

## 0.30.0

### Notable Implementation Changes

- Dropping redundant Pub / Sub `Policy._paused` data member (#4568).
- Removing redundant "active" check in policy (#4603).
- Adding a `Consumer.active` property (#4604).
- Making it impossible to call `Policy.open()` on an already opened
  policy (#4606).
- **Bug fix** (#4575): Fix bug with async publish for batches. There
  were two related bugs. The first: if a batch exceeds the `max_messages`
  from the batch settings, then the `commit()` will fail. The second:
  when a "monitor" worker that after `max_latency` seconds, a failure
  can occur if a new message is added to the batch during the publish.
  To fix, the following changes were implemented:
  - Adding a "STARTING" status for `Batch.commit()` (#4614). This
    fixes the issue when the batch exceeds `max_messages`.
  - Adding extra check in `Batch.will_accept` for the number of
    messages (#4612).
  - Moving `will_accept()` check out of `PublisherClient.batch()`
    factory (#4613).
  - Checking `Batch.will_accept` in thread-safe way (#4616).
- **Breaking API change**: As part of #4613, changing `PublisherClient.batch()`
  to no longer accept a `message` (since the `will_accept` check needs to
  happen in a more concurrency friendly way). In addition, changing the
  `create` argument so that it means "create even if batch already exists"
  rather than "create if missing".

### Documentation

- Add more explicit documentation for Pub / Sub `Message.attributes` (#4601).
- Make `Message.__repr__` a bit prettier / more useful (#4602).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.30.0/

## 0.29.4

### Notable Implementation Changes

- **Bug fix**: Restore previous behavior of the subscription lease
  maintenance worker. This was accidentally "stopped" in `0.29.3`
  due to a change in implementation that went from an `active`
  boolean to an "inactive" / `stopped` boolean, so `True` became
  `False` and vice-versa (#4564).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.4/

## 0.29.3

### Notable Implementation Changes

- In subscription consumer thread: Making sure the request generator
  attached to an inactive bidirectional streaming pull is stopped before
  spawning a new request generator. This way we have a (fairly strong)
  guarantee that requests in the queue don't get sent into an inactive
  stream (#4503, #4554).
- Adding `pause` / `resume` to subscription consumer thread and using these
  methods during flow control. The previous implementation tried to close the
  subscription (which involved 3 worker threads and 10 executors in a thread
  pool) and then re-open a new subscription. But, this was not entirely
  possible to shut down correctly from **within** one of the worker threads.
  Instead, we only pause the worker (of the 3) that is pulling new responses
  from the bidirectional streaming pull (#4558).
- **Bug fix** (#4516): Using `max` where `min` was used by mistake to
  ensure the number of bytes tracked for subscription flow control
  remained non-negative (#4514).
- Raising `TypeError` if `SubscriberClient.subscribe` receives a
  non-callable callback (#4497).
- Shutting down thread pool executor when closing a subscriber
  policy (#4522).
- Renaming `Policy.on_callback_request` to `Policy.dispatch_callback`
  and making the behavior much less dynamic (#4511).
- Make sure subscription consumer thread doesn't try to join itself
  when exiting in error (#4540).

### Dependencies

- Upgrading `google-api-core` dependency to latest revision (`0.1.2`)
  since we rely on the latest version of the `concurrent.futures` backport
  to provide the `thread_name_prefix` argument for thread pool
  executor (#4521, #4559).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.3/

## 0.29.2

### Notable Implementation Changes

- **Bug fix** (#4463): Making a subscription consumer actually stop
  running after encountering an exception (#4472, #4498). This bug
  is the **only** reason for the `0.29.2` release.
- Thread Changes
  - Added names to all threads created directly by Pub / Sub (#4474,
    #4476, #4480). Also removing spaces and colons from thread
    names (#4476).
- Logging changes
  - Adding debug logs when lease management exits (#4484)
  - Adding debug logs when `QueueCallbackThread` exits (#4494).
    Instances handle the processing of messages in a
    subscription (e.g. to `ack`).
  - Using a named logger in `publisher.batch.thread` (#4473)
  - Adding newlines before logging protobuf payloads (#4471)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.2/

## 0.29.1

### Notable Implementation Changes

- **Bug fix** (#4234): Adding retries for connection `UNAVAILABLE`. This
  bug made the Pub / Sub client mostly unusable for subscribers to topics
  that don't have a steady stream of messages. After ~2 minutes of inactivity,
  the gRPC connection would timeout and raise `UNAVAILABLE` locally, i.e. not
  due to a response from the backend. (#4444)
- Updating autogenerated packages (#4438)

### Documentation

- Fixing broken examples in quick start (#4398)
- Fixing broken example in README (#4402, h/t to @mehmetboraezer)
- Updating old/dead link to usage doc in README (#4406, h/t to @mehmetboraezer)

### Dependencies

- Dropping dependency on `google-cloud-core` in exchange for
  `google-api-core` (#4438)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.1/

## 0.29.0

### Notable Implementation Changes

- Honor `max_messages` always (#4262)
- Add futures for subscriptions (#4265)
- Set gRPC message options and keepalive (#4269)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-pubsub/0.29.0/
