# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-pubsub/#history

## 0.38.0

### Implementation Changes

- Fix race condition in recv()'s usage of self.call. ([#5935](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5935))
- Re-generate the underlying library from protos. ([#5953](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5953))
- Change 'BatchSettings.max_bytes' default. ([#5899](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5899))
- Fix race condition where pending Ack IDs can be modified by another thread. ([#5929](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5929))

### Internal / Testing Changes

- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))

## 0.37.2

### Implementation Changes

- Fix classmethod wrapping (#5826)

### Documentation

- Fix Sphinx rendering for publisher client. (#5822)

### Internal / Testing Changes

- Re-generate library, removing obsolete synth modifications. (#5825)
- Add test for testing invoking a wrapped class method on the class itself (#5828)

## 0.37.1

### Implementation Changes

- Make get_initial_request more resilient to race conditions. (#5803)

## 0.37.0

### Implementation Changes

- Make Publisher batch-related interfaces private (#5784)

## 0.36.0

### Implementation Changes
- Pubsub: Make 'Message.publish_time' return datetime (#5633)
- Ensure SPM methods check that 'self._consumer' is not None before use. (#5758)

### New Features
- PubSub: add geo-fencing support (#5769)
- Add 'Message.ack_id' property. (#5693)

## 0.35.4

### Implementation Changes

- Recover streams during the gRPC error callback. (#5446)
- Use operational lock when checking for activity on streams. (#5445)

## 0.35.3

### Implementation Changes

- Add additional error handling to unary RPCs (#5438)

## 0.35.2

### Implementation Changes
- Add heartbeating to the streaming pull manager (#5413)
- Fix retrying of bidirectional RPCs and closing the streaming pull manager (#5412)

## 0.35.1

### Implementation Changes
- Catch errors when re-retying send() or recv() in addition to open() (#5402)

## 0.35.0

### Implementation Changes

- Send requests during streaming pull over a separate unary RPC (#5377)
- Initialize references to helper threads before starting them (#5374)
- Make leaser exit more quickly (#5373)
- Make re-open failures bubble to callbacks (#5372)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Normalize overflow handling for max count and bytes (#5343)

### New Features

- Restore the synchronous pull method (#5379)
- Promote subscribe_experimental() to subscribe(), remove old subscriber implementation. (#5274)
- Wire up scheduler argument for subscribe() (#5279)

### Documentation

- Add link to streaming pull behavior documentation (#5378)
- Fix example in subscribe's documentation (#5375)

### Internal / Testing Changes

- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.34.0

### Implementation Changes

- Lower the flow control defaults. (#5248)

### New Features

- A new implementation of the subscriber has been added. This is available as `SubscriberClient.subscribe_experimental`. In the next release, this will be replace the current `subscribe` method. If you use this, please report your
findings to us on GitHub. (#5189, #5201, #5210, #5229, #5230, #5237, #5256)

### Dependencies

- Remove psutil dependency. (#5248)

## 0.33.1

### Implementation changes

- Surface publish RPC errors back to the publish futures (#5124)
- Make the pausable response iterator aware of the RPC state to prevent deadlock (#5108)
- Properly handle graceful stop in request generator (#5097)

## 0.33.0

### Implementation changes

- Drop leased messages after flow_control.max_lease_duration has passed. (#5020)
- Fix mantain leases to not modack messages it just dropped (#5045)
- Avoid race condition in maintain_leases by copying leased_messages (#5035)
- Retry subscription stream on InternalServerError, Unknown, and GatewayTimeout (#5021)
- Use the rpc's status to determine when to exit the request generator thread (#5054)
- Fix missing iter on request stream (#5078)
- Nack messages when the subscriber callback errors (#5019)

### Testing

- pubsub nox.py cleanup (#5056)
- Fix test that checks for retryable exceptions (#5034)

## 0.32.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)

## 0.32.0

### Implementation changes

- Added support for streaming pull receipts. (#4878)

## 0.31.0

### New features

- Added the ability for subscriber to batch requests. (#4895)
- Added pending request backpressure for subscriber. (#4892)

### Implementation changes

- Raise `ValueError` when a message is too large for a batch. (#4872)
- Updated the default batch size to 10 MB. (#4857)
- Allow a custom `Event` type in Pub / Sub futures. (#4643)

### Documentation

- Clarify that `modify_ack_deadline` resets the deadline. (#4822)

### Testing

- Fix unit test for default `max_bytes` value. (#4860)

## 0.30.1

### Notable Implementation Changes

- Moving lock factory used in publisher client to the Batch
  implementation (#4628).
- Use a UUID (rather than a sentinel object) on `Future` (#4634).
- Apply scopes to explicitly provided credentials if needed (#4594).
  Fixes #4479. This feature comes as part of `google-api-core==0.1.3`.

### Dependencies

- Upgrading to `google-api-core==0.1.3` which depends on the latest
  `grpcio==1.8.2` (#4642). This fixes #4600. For details, see related
  gRPC [bug](https://github.com/grpc/grpc/issues/9688) and
  [fix](https://github.com/grpc/grpc/pull/13665).

PyPI: https://pypi.org/project/google-cloud-pubsub/0.30.1/

## 0.30.0

### Notable Implementation Changes

- Dropping redundant `Policy._paused` data member (#4568).
- Removing redundant "active" check in policy (#4603).
- Adding a `Consumer.active` property (#4604).
- Making it impossible to call `Policy.open()` on an already opened
  policy (#4606).
- **Bug fix** (#4575): Fix bug with async publish for batches. There
  were two related bugs. The first: if a batch exceeds the `max_messages`
  from the batch settings, then the `commit()` will fail. The second:
  when a "monitor" worker calls `commit()` after `max_latency` seconds,
  a failure can occur if a new message is added to the batch **during**
  the commit. To fix, the following changes were implemented:
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

- Add more explicit documentation for `Message.attributes` (#4601).
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
