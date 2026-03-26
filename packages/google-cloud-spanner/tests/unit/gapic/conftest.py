import asyncio
import sys

import pytest


@pytest.fixture(autouse=True)
def provide_loop_to_sync_grpc_tests():
    """
    GAPIC creates synchronous methods testing Asyncio transports.
    If no global loop exists, `grpc.aio` engine crashes during initialization.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    yield
    # No close here, just ensure existance
