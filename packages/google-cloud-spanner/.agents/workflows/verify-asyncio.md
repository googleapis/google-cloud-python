---
description: How to verify a Spanner Asyncio launch is ready.
---
# Spanner Asyncio Launch Verification Workflow

This workflow provides the necessary steps to verify that the Spanner Asyncio implementation is correct, stable, and ready for launch.

## 1. Run Async Unit Tests
Run the complete suite of asynchronous unit tests across all supported Python versions.
```bash
nox -s unit
```
Ensure that all tests in `tests/unit/_async/` pass.

## 2. Run Async System Tests
Verify the asynchronous behavior against the Spanner Emulator.
// turbo
```bash
export SPANNER_EMULATOR_HOST="localhost:9010"
export GCLOUD_PROJECT="emulator-test-project"
export GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE="true"
nox -s system -- tests/system/_async
```
**Note**: Ensure `pytest-asyncio` is installed in the system test environment.

## 3. Verify Sync/Async Parity
Run the cross-sync generation tool and ensure no regressions in the synchronous codebase.
```bash
python3 .cross_sync/generate.py
nox -s unit-3.14
nox -s system-3.14
```

## 4. Check for Coroutine Leaks
Ensure all asynchronous GAPIC calls are properly awaited. Search for any unawaited coroutines in the `_async` directory.
```bash
grep -r "await " google/cloud/spanner_v1/_async | grep -v "async def"
```

## 5. Verify Sample Code
Verify that the provided samples work correctly.
```bash
python3 samples/async_samples.py
```
