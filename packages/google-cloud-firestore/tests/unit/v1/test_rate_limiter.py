# Copyright 2021 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import mock


# Pick a point in time as the center of our universe for this test run.
# It is okay for this to update every time the tests are run.
fake_now = datetime.datetime.utcnow()


def now_plus_n(seconds: int = 0, microseconds: int = 0) -> datetime.timedelta:
    return fake_now + datetime.timedelta(
        seconds=seconds,
        microseconds=microseconds,
    )


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_rate_limiter_basic(mocked_now):
    """Verifies that if the clock does not advance, the RateLimiter allows 500
    writes before crashing out.
    """
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now
    # This RateLimiter will never advance. Poor fella.
    ramp = rate_limiter.RateLimiter()
    for _ in range(rate_limiter.default_initial_tokens):
        assert ramp.take_tokens() == 1
    assert ramp.take_tokens() == 0


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_rate_limiter_with_refill(mocked_now):
    """Verifies that if the clock advances, the RateLimiter allows appropriate
    additional writes.
    """
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now
    ramp = rate_limiter.RateLimiter()
    ramp._available_tokens = 0
    assert ramp.take_tokens() == 0
    # Advance the clock 0.1 seconds
    mocked_now.return_value = now_plus_n(microseconds=100000)
    for _ in range(round(rate_limiter.default_initial_tokens / 10)):
        assert ramp.take_tokens() == 1
    assert ramp.take_tokens() == 0


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_rate_limiter_phase_length(mocked_now):
    """Verifies that if the clock advances, the RateLimiter allows appropriate
    additional writes.
    """
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now
    ramp = rate_limiter.RateLimiter()
    assert ramp.take_tokens() == 1
    ramp._available_tokens = 0
    assert ramp.take_tokens() == 0
    # Advance the clock 1 phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length,
        microseconds=1,
    )
    for _ in range(round(rate_limiter.default_initial_tokens * 3 / 2)):
        assert ramp.take_tokens()

    assert ramp.take_tokens() == 0


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_rate_limiter_idle_phase_length(mocked_now):
    """Verifies that if the clock advances but nothing happens, the RateLimiter
    doesn't ramp up.
    """
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now
    ramp = rate_limiter.RateLimiter()
    ramp._available_tokens = 0
    assert ramp.take_tokens() == 0
    # Advance the clock 1 phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length,
        microseconds=1,
    )
    for _ in range(round(rate_limiter.default_initial_tokens)):
        assert ramp.take_tokens() == 1
        assert ramp._maximum_tokens == 500
    assert ramp.take_tokens() == 0


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_take_batch_size(mocked_now):
    """Verifies that if the clock advances but nothing happens, the RateLimiter
    doesn't ramp up.
    """
    from google.cloud.firestore_v1 import rate_limiter

    page_size: int = 20
    mocked_now.return_value = fake_now
    ramp = rate_limiter.RateLimiter()
    ramp._available_tokens = 15
    assert ramp.take_tokens(page_size, allow_less=True) == 15
    # Advance the clock 1 phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length,
        microseconds=1,
    )
    ramp._check_phase()
    assert ramp._maximum_tokens == 750

    for _ in range(740 // page_size):
        assert ramp.take_tokens(page_size) == page_size
    assert ramp.take_tokens(page_size, allow_less=True) == 10
    assert ramp.take_tokens(page_size, allow_less=True) == 0


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_phase_progress(mocked_now):
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now

    ramp = rate_limiter.RateLimiter()
    assert ramp._phase == 0
    assert ramp._maximum_tokens == 500
    ramp.take_tokens()

    # Advance the clock 1 phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length,
        microseconds=1,
    )
    ramp.take_tokens()
    assert ramp._phase == 1
    assert ramp._maximum_tokens == 750

    # Advance the clock another phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length * 2,
        microseconds=1,
    )
    ramp.take_tokens()
    assert ramp._phase == 2
    assert ramp._maximum_tokens == 1125

    # Advance the clock another ms and the phase should not advance
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length * 2,
        microseconds=2,
    )
    ramp.take_tokens()
    assert ramp._phase == 2
    assert ramp._maximum_tokens == 1125


@mock.patch("google.cloud.firestore_v1.rate_limiter.utcnow")
def test_global_max_tokens(mocked_now):
    from google.cloud.firestore_v1 import rate_limiter

    mocked_now.return_value = fake_now

    ramp = rate_limiter.RateLimiter(
        global_max_tokens=499,
    )
    assert ramp._phase == 0
    assert ramp._maximum_tokens == 499
    ramp.take_tokens()

    # Advance the clock 1 phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length,
        microseconds=1,
    )
    ramp.take_tokens()
    assert ramp._phase == 1
    assert ramp._maximum_tokens == 499

    # Advance the clock another phase
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length * 2,
        microseconds=1,
    )
    ramp.take_tokens()
    assert ramp._phase == 2
    assert ramp._maximum_tokens == 499

    # Advance the clock another ms and the phase should not advance
    mocked_now.return_value = now_plus_n(
        seconds=rate_limiter.default_phase_length * 2,
        microseconds=2,
    )
    ramp.take_tokens()
    assert ramp._phase == 2
    assert ramp._maximum_tokens == 499


def test_utcnow():
    from google.cloud.firestore_v1 import rate_limiter

    now = rate_limiter.utcnow()
    assert isinstance(now, datetime.datetime)
