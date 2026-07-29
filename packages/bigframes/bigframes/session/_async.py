# Copyright 2026 Google LLC
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

from __future__ import annotations

import asyncio
import threading
from typing import Optional

_bg_loop: Optional[asyncio.AbstractEventLoop] = None
_bg_thread: Optional[threading.Thread] = None
_bg_lock = threading.Lock()


def _get_bg_loop() -> asyncio.AbstractEventLoop:
    global _bg_loop, _bg_thread
    with _bg_lock:
        if _bg_loop is None:
            loop = asyncio.new_event_loop()
            _bg_loop = loop

            def run():
                asyncio.set_event_loop(loop)
                loop.run_forever()

            _bg_thread = threading.Thread(
                target=run, daemon=True, name="bigframes-bg-loop"
            )
            _bg_thread.start()
    return _bg_loop


def run_sync(coro):
    """
    Runs a coroutine synchronously, either in the current thread's event loop
    if none is running, or by scheduling it on a background thread's event loop.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is None:
        return asyncio.run(coro)
    else:
        bg_loop = _get_bg_loop()
        future = asyncio.run_coroutine_threadsafe(coro, bg_loop)
        return future.result()
