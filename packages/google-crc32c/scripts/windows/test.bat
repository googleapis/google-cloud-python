@rem Copyright 2019 Google LLC. All rights reserved.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem     http://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.


@rem update python deps and build wheels (requires CRC32C_INSTALL_PREFIX is set)
@rem FOR %%V IN (3.5-64,3.5-32,3.6-64,3.6-32,3.7-64,3.7-32) DO (
@rem FOR %%V IN (3.5-64,3.6-64,3.7-64) DO (
FOR %%V IN (3.5-64,3.5-32,3.6-64,3.6-32,3.7-64,3.7-32) DO (

    py -%%V -m pip install --no-index --find-links=. google-crc32c
    py -%%V -m pip install pytest
    py -%%V -m pytest tests
)