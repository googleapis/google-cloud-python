# Benchmark Tests

## Overview

This directory contains scripts for performance benchmarking of various components of BigFrames.

## Execution Details

Scripts in this directory can be executed as part of the benchmarking session or independently from the command line. This allows for quick, standalone runs for immediate debugging and validation without the overhead of initiating full benchmark sessions.

## Why Separate Processes?

Each benchmark is executed in a separate process to mitigate the effects of any residual caching or settings that may persist in BigFrames, ensuring that each test is conducted in a clean state.
