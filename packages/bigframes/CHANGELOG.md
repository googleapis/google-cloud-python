# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigframes/#history

## [2.31.0](https://github.com/googleapis/google-cloud-python/compare/bigframes-v2.30.0...bigframes-v2.31.0) (2025-12-10)


### Features

* add `bigframes.bigquery.ml` methods (#2300) ([719b278c844ca80c1bec741873b30a9ee4fd6c56](https://github.com/googleapis/google-cloud-python/commit/719b278c844ca80c1bec741873b30a9ee4fd6c56))
* add 'weekday' property to DatatimeMethod (#2304) ([fafd7c732d434eca3f8b5d849a87149f106e3d5d](https://github.com/googleapis/google-cloud-python/commit/fafd7c732d434eca3f8b5d849a87149f106e3d5d))


### Bug Fixes

* cache DataFrames to temp tables in bigframes.bigquery.ml methods to avoid time travel (#2318) ([d99383195ac3f1683842cfe472cca5a914b04d8e](https://github.com/googleapis/google-cloud-python/commit/d99383195ac3f1683842cfe472cca5a914b04d8e))

## [2.30.0](https://github.com/googleapis/google-cloud-python/compare/bigframes-v2.29.0...bigframes-v2.30.0) (2025-12-03)


### Documentation

* Add Google Analytics configuration to conf.py (#2301) ([0b266da10f4d3d0ef9b4dd71ddadebfc7d5064ca](https://github.com/googleapis/google-cloud-python/commit/0b266da10f4d3d0ef9b4dd71ddadebfc7d5064ca))
* fix LogisticRegression docs rendering (#2295) ([32e531343c764156b45c6fb9de49793d26c19f02](https://github.com/googleapis/google-cloud-python/commit/32e531343c764156b45c6fb9de49793d26c19f02))
* update API reference to new `dataframes.bigquery.dev` location (#2293) ([da064397acd2358c16fdd9659edf23afde5c882a](https://github.com/googleapis/google-cloud-python/commit/da064397acd2358c16fdd9659edf23afde5c882a))
* use autosummary to split documentation pages (#2251) ([f7fd2d20896fe3e0e210c3833b6a4c3913270ebc](https://github.com/googleapis/google-cloud-python/commit/f7fd2d20896fe3e0e210c3833b6a4c3913270ebc))
* update docs and tests for Gemini 2.5 models (#2279) ([08c0c0c8fe8f806f6224dc403a3f1d4db708573a](https://github.com/googleapis/google-cloud-python/commit/08c0c0c8fe8f806f6224dc403a3f1d4db708573a))


### Features

* Allow drop_duplicates over unordered dataframe (#2303) ([52665fa57ef13c58254bfc8736afcc521f7f0f11](https://github.com/googleapis/google-cloud-python/commit/52665fa57ef13c58254bfc8736afcc521f7f0f11))
* Add agg/aggregate methods to windows (#2288) ([c4cb39dcbd388356f5f1c48ff28b19b79b996485](https://github.com/googleapis/google-cloud-python/commit/c4cb39dcbd388356f5f1c48ff28b19b79b996485))
* Implement single-column sorting for interactive table widget (#2255) ([d1ecc61bf448651a0cca0fc760673da54f5c2183](https://github.com/googleapis/google-cloud-python/commit/d1ecc61bf448651a0cca0fc760673da54f5c2183))
* add bigquery.json_keys (#2286) ([b487cf1f6ecacb1ee3b35ffdd934221516bbd558](https://github.com/googleapis/google-cloud-python/commit/b487cf1f6ecacb1ee3b35ffdd934221516bbd558))
* use end user credentials for `bigframes.bigquery.ai` functions when `connection_id` is not present  (#2272) ([7c062a68c6a3c9737865985b4f1fd80117490c73](https://github.com/googleapis/google-cloud-python/commit/7c062a68c6a3c9737865985b4f1fd80117490c73))
* pivot_table supports fill_value arg (#2257) ([8f490e68a9a2584236486060ad3b55923781d975](https://github.com/googleapis/google-cloud-python/commit/8f490e68a9a2584236486060ad3b55923781d975))
* Support mixed scalar-analytic expressions (#2239) ([20ab469d29767a2f04fe02aa66797893ecd1c539](https://github.com/googleapis/google-cloud-python/commit/20ab469d29767a2f04fe02aa66797893ecd1c539))
* Support builtins funcs for df.agg (#2256) ([956a5b00dff55b73e3cbebb4e6e81672680f1f63](https://github.com/googleapis/google-cloud-python/commit/956a5b00dff55b73e3cbebb4e6e81672680f1f63))
* Preserve source names better for more readable sql (#2243) ([64995d659837a8576b2ee9335921904e577c7014](https://github.com/googleapis/google-cloud-python/commit/64995d659837a8576b2ee9335921904e577c7014))
* Add bigframes.pandas.crosstab (#2231) ([c62e5535ed4c19b6d65f9a46cb1531e8099621b2](https://github.com/googleapis/google-cloud-python/commit/c62e5535ed4c19b6d65f9a46cb1531e8099621b2))


### Bug Fixes

* Update max_instances default to reflect actual value (#2302) ([4489687eafc9a1ea1b985600010296a4245cef94](https://github.com/googleapis/google-cloud-python/commit/4489687eafc9a1ea1b985600010296a4245cef94))
* Fix issue with stream upload batch size upload limit (#2290) ([6cdf64b0674d0e673f86362032d549316850837b](https://github.com/googleapis/google-cloud-python/commit/6cdf64b0674d0e673f86362032d549316850837b))
* Pass credentials properly for read api instantiation (#2280) ([3e3fe259567d249d91f90786a577b05577e2b9fd](https://github.com/googleapis/google-cloud-python/commit/3e3fe259567d249d91f90786a577b05577e2b9fd))
* Improve Anywidget pagination and display for unknown row counts (#2258) ([508deae5869e06cdad7bb94537c9c58d8f083d86](https://github.com/googleapis/google-cloud-python/commit/508deae5869e06cdad7bb94537c9c58d8f083d86))
* calling info() on empty dataframes no longer leads to errors (#2267) ([95a83f7774766cd19cb583dfaa3417882b5c9b1e](https://github.com/googleapis/google-cloud-python/commit/95a83f7774766cd19cb583dfaa3417882b5c9b1e))
* do not warn with DefaultIndexWarning in partial ordering mode (#2230) ([cc2dbae684103a21fe8838468f7eb8267188780d](https://github.com/googleapis/google-cloud-python/commit/cc2dbae684103a21fe8838468f7eb8267188780d))

## [2.29.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.28.0...v2.29.0) (2025-11-10)


### Features

* Add bigframes.bigquery.st_regionstats to join raster data from Earth Engine ([#2228](https://github.com/googleapis/python-bigquery-dataframes/issues/2228)) ([10ec52f](https://github.com/googleapis/python-bigquery-dataframes/commit/10ec52f30a0a9c61b9eda9cf4f9bd6aa0cd95db5))
* Add DataFrame.resample and Series.resample ([#2213](https://github.com/googleapis/python-bigquery-dataframes/issues/2213)) ([c9ca02c](https://github.com/googleapis/python-bigquery-dataframes/commit/c9ca02c5194c8b8e9b940eddd2224efd2ff0d5d9))
* SQL Cell no longer escapes formatted string values ([#2245](https://github.com/googleapis/python-bigquery-dataframes/issues/2245)) ([d2d38f9](https://github.com/googleapis/python-bigquery-dataframes/commit/d2d38f94ed8333eae6f9cff3833177756eefe85a))
* Support left_index and right_index for merge ([#2220](https://github.com/googleapis/python-bigquery-dataframes/issues/2220)) ([da9ba26](https://github.com/googleapis/python-bigquery-dataframes/commit/da9ba267812c01ffa6fa0b09943d7a4c63b8f187))


### Bug Fixes

* Correctly iterate over null struct values in ManagedArrowTable ([#2209](https://github.com/googleapis/python-bigquery-dataframes/issues/2209)) ([12e04d5](https://github.com/googleapis/python-bigquery-dataframes/commit/12e04d55f0d6aef1297b7ca773935aecf3313ee7))
* Simplify UnsupportedTypeError message ([#2212](https://github.com/googleapis/python-bigquery-dataframes/issues/2212)) ([6c9a18d](https://github.com/googleapis/python-bigquery-dataframes/commit/6c9a18d7e67841c6fe6c1c6f34f80b950815141f))
* Support results with STRUCT and ARRAY columns containing JSON subfields in `to_pandas_batches()` ([#2216](https://github.com/googleapis/python-bigquery-dataframes/issues/2216)) ([3d8b17f](https://github.com/googleapis/python-bigquery-dataframes/commit/3d8b17fa5eb9bbfc9e151031141a419f2dc3acb4))


### Documentation

* Switch API reference docs to pydata theme ([#2237](https://github.com/googleapis/python-bigquery-dataframes/issues/2237)) ([9b86dcf](https://github.com/googleapis/python-bigquery-dataframes/commit/9b86dcf87929648bf5ab565dfd46a23b639f01ac))
* Update notebook for JSON subfields support in to_pandas_batches() ([#2138](https://github.com/googleapis/python-bigquery-dataframes/issues/2138)) ([5663d2a](https://github.com/googleapis/python-bigquery-dataframes/commit/5663d2a18064589596558af109e915f87d426eb0))

## [2.28.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.27.0...v2.28.0) (2025-11-03)


### Features

* Add bigframes.bigquery.st_simplify ([#2210](https://github.com/googleapis/python-bigquery-dataframes/issues/2210)) ([ecee2bc](https://github.com/googleapis/python-bigquery-dataframes/commit/ecee2bc6ada0bc968fc56ed7194dc8c043547e93))
* Add Series.dt.day_name ([#2218](https://github.com/googleapis/python-bigquery-dataframes/issues/2218)) ([5e006e4](https://github.com/googleapis/python-bigquery-dataframes/commit/5e006e404b65c32e5b1d342ebfcfce59ee592c8c))
* Polars engine supports std, var ([#2215](https://github.com/googleapis/python-bigquery-dataframes/issues/2215)) ([ef5e83a](https://github.com/googleapis/python-bigquery-dataframes/commit/ef5e83acedf005cbe1e6ad174bec523ac50517d7))
* Support INFORMATION_SCHEMA views in `read_gbq` ([#1895](https://github.com/googleapis/python-bigquery-dataframes/issues/1895)) ([d97cafc](https://github.com/googleapis/python-bigquery-dataframes/commit/d97cafcb5921fca2351b18011b0e54e2631cc53d))
* Support some python standard lib callables in apply/combine ([#2187](https://github.com/googleapis/python-bigquery-dataframes/issues/2187)) ([86a2756](https://github.com/googleapis/python-bigquery-dataframes/commit/86a27564b48b854a32b3d11cd2105aa0fa496279))


### Bug Fixes

* Correct connection normalization in blob system tests ([#2222](https://github.com/googleapis/python-bigquery-dataframes/issues/2222)) ([a0e1e50](https://github.com/googleapis/python-bigquery-dataframes/commit/a0e1e50e47c758bdceb54d04180ed36b35cf2e35))
* Improve error handling in blob operations ([#2194](https://github.com/googleapis/python-bigquery-dataframes/issues/2194)) ([d410046](https://github.com/googleapis/python-bigquery-dataframes/commit/d4100466612df0523d01ed01ca1e115dabd6ef45))
* Resolve AttributeError in TableWidget and improve initialization ([#1937](https://github.com/googleapis/python-bigquery-dataframes/issues/1937)) ([4c4c9b1](https://github.com/googleapis/python-bigquery-dataframes/commit/4c4c9b14657b7cda1940ef39e7d4db20a9ff5308))


### Documentation

* Update bq_dataframes_llm_output_schema.ipynb ([#2004](https://github.com/googleapis/python-bigquery-dataframes/issues/2004)) ([316ba9f](https://github.com/googleapis/python-bigquery-dataframes/commit/316ba9f557d792117d5a7845d7567498f78dd513))

## [2.27.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.26.0...v2.27.0) (2025-10-24)


### Features

* Add __abs__ to dataframe ([#2186](https://github.com/googleapis/python-bigquery-dataframes/issues/2186)) ([c331dfe](https://github.com/googleapis/python-bigquery-dataframes/commit/c331dfed59174962fbdc8ace175dd00fcc3d5d50))
* Add df.groupby().corr()/cov() support ([#2190](https://github.com/googleapis/python-bigquery-dataframes/issues/2190)) ([ccd7c07](https://github.com/googleapis/python-bigquery-dataframes/commit/ccd7c0774a65d09e6cf31d2b62d0bc64bd7c4248))
* Add str accessor to index ([#2179](https://github.com/googleapis/python-bigquery-dataframes/issues/2179)) ([cd87ce0](https://github.com/googleapis/python-bigquery-dataframes/commit/cd87ce0d504747f44d1b5a55f869a2e0fca6df17))
* Add support for `np.isnan` and `np.isfinite` ufuncs ([#2188](https://github.com/googleapis/python-bigquery-dataframes/issues/2188)) ([68723bc](https://github.com/googleapis/python-bigquery-dataframes/commit/68723bc1f08013e43a8b11752f908bf8fd6d51f5))
* Include local data bytes in the dry run report when available ([#2185](https://github.com/googleapis/python-bigquery-dataframes/issues/2185)) ([ee2c40c](https://github.com/googleapis/python-bigquery-dataframes/commit/ee2c40c6789535e259fb6a9774831d6913d16212))
* Support len() on Groupby objects ([#2183](https://github.com/googleapis/python-bigquery-dataframes/issues/2183)) ([4191821](https://github.com/googleapis/python-bigquery-dataframes/commit/4191821b0976281a96c8965336ef51f061b0c481))
* Support pa.json_(pa.string()) in struct/list if available ([#2180](https://github.com/googleapis/python-bigquery-dataframes/issues/2180)) ([5ec3cc0](https://github.com/googleapis/python-bigquery-dataframes/commit/5ec3cc0298c7a6195d5bd12a08d996e7df57fc5f))


### Documentation

* Update AI operators deprecation notice ([#2182](https://github.com/googleapis/python-bigquery-dataframes/issues/2182)) ([2c50310](https://github.com/googleapis/python-bigquery-dataframes/commit/2c503107e17c59232b14b0d7bc40c350bb087d6f))

## [2.26.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.25.0...v2.26.0) (2025-10-17)


### ⚠ BREAKING CHANGES

* turn Series.struct.dtypes into a property to match pandas (https://github.com/googleapis/python-bigquery-dataframes/pull/2169)

### Features

* Add df.sort_index(axis=1) ([#2173](https://github.com/googleapis/python-bigquery-dataframes/issues/2173)) ([ebf95e3](https://github.com/googleapis/python-bigquery-dataframes/commit/ebf95e3ef77822650f2e190df7b868011174d412))
* Enhanced multimodal error handling with verbose mode for blob image functions ([#2024](https://github.com/googleapis/python-bigquery-dataframes/issues/2024)) ([f9e28fe](https://github.com/googleapis/python-bigquery-dataframes/commit/f9e28fe3f883cc4d486178fe241bc8b76473700f))
* Implement cos, sin, and log operations for polars compiler ([#2170](https://github.com/googleapis/python-bigquery-dataframes/issues/2170)) ([5613e44](https://github.com/googleapis/python-bigquery-dataframes/commit/5613e4454f198691209ec28e58ce652104ac2de4))
* Make `all` and `any` compatible with integer columns on Polars session ([#2154](https://github.com/googleapis/python-bigquery-dataframes/issues/2154)) ([6353d6e](https://github.com/googleapis/python-bigquery-dataframes/commit/6353d6ecad5139551ef68376c08f8749dd440014))


### Bug Fixes

* `blob.display()` shows &lt;NA&gt; for null rows ([#2158](https://github.com/googleapis/python-bigquery-dataframes/issues/2158)) ([ddb4df0](https://github.com/googleapis/python-bigquery-dataframes/commit/ddb4df0dd991bef051e2a365c5cacf502803014d))
* Turn Series.struct.dtypes into a property to match pandas (https://github.com/googleapis/python-bigquery-dataframes/pull/2169) ([62f7e9f](https://github.com/googleapis/python-bigquery-dataframes/commit/62f7e9f38f26b6eb549219a4cbf2c9b9023c9c35))


### Documentation

* Clarify that only NULL values are handled by fillna/isna, not NaN ([#2176](https://github.com/googleapis/python-bigquery-dataframes/issues/2176)) ([8f27e73](https://github.com/googleapis/python-bigquery-dataframes/commit/8f27e737fc78a182238090025d09479fac90b326))
* Remove import bigframes.pandas as bpd boilerplate from many samples ([#2147](https://github.com/googleapis/python-bigquery-dataframes/issues/2147)) ([1a01ab9](https://github.com/googleapis/python-bigquery-dataframes/commit/1a01ab97f103361f489f37b0af8c4b4d7806707c))

## [2.25.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.24.0...v2.25.0) (2025-10-13)


### Features

* Add barh, pie plot types ([#2146](https://github.com/googleapis/python-bigquery-dataframes/issues/2146)) ([5cc3c5b](https://github.com/googleapis/python-bigquery-dataframes/commit/5cc3c5b1391a7dfa062b1d77f001726b013f6337))
* Add Index.__eq__ for consts, aligned objects ([#2141](https://github.com/googleapis/python-bigquery-dataframes/issues/2141)) ([8514200](https://github.com/googleapis/python-bigquery-dataframes/commit/85142008ec895fa078d192bbab942d0257f70df3))
* Add output_schema parameter to ai.generate() ([#2139](https://github.com/googleapis/python-bigquery-dataframes/issues/2139)) ([ef0b0b7](https://github.com/googleapis/python-bigquery-dataframes/commit/ef0b0b73843da2a93baf08e4cd5457fbb590b89c))
* Create session-scoped `cut`, `DataFrame`, `MultiIndex`, `Index`, `Series`, `to_datetime`, and `to_timedelta` methods ([#2157](https://github.com/googleapis/python-bigquery-dataframes/issues/2157)) ([5e1e809](https://github.com/googleapis/python-bigquery-dataframes/commit/5e1e8098ecf212c91d73fa80d722d1cb3e46668b))
* Replace ML.GENERATE_TEXT with AI.GENERATE for audio transcription ([#2151](https://github.com/googleapis/python-bigquery-dataframes/issues/2151)) ([a410d0a](https://github.com/googleapis/python-bigquery-dataframes/commit/a410d0ae43ef3b053b650804156eda0b1f569da9))
* Support string literal inputs for AI functions ([#2152](https://github.com/googleapis/python-bigquery-dataframes/issues/2152)) ([7600001](https://github.com/googleapis/python-bigquery-dataframes/commit/760000122dc190ac8a3303234cf4cbee1bbb9493))


### Bug Fixes

* Address typo in error message ([#2142](https://github.com/googleapis/python-bigquery-dataframes/issues/2142)) ([cdf2dd5](https://github.com/googleapis/python-bigquery-dataframes/commit/cdf2dd55a0c03da50ab92de09788cafac0abf6f6))
* Avoid possible circular imports in global session ([#2115](https://github.com/googleapis/python-bigquery-dataframes/issues/2115)) ([095c0b8](https://github.com/googleapis/python-bigquery-dataframes/commit/095c0b85a25a2e51087880909597cc62a0341c93))
* Fix too many cluster columns requested by caching ([#2155](https://github.com/googleapis/python-bigquery-dataframes/issues/2155)) ([35c1c33](https://github.com/googleapis/python-bigquery-dataframes/commit/35c1c33b85d1b92e402aab73677df3ffe43a51b4))
* Show progress even in job optional queries ([#2119](https://github.com/googleapis/python-bigquery-dataframes/issues/2119)) ([1f48d3a](https://github.com/googleapis/python-bigquery-dataframes/commit/1f48d3a62e7e6dac4acb39e911daf766b8e2fe62))
* Yield row count from read session if otherwise unknown ([#2148](https://github.com/googleapis/python-bigquery-dataframes/issues/2148)) ([8997d4d](https://github.com/googleapis/python-bigquery-dataframes/commit/8997d4d7d9965e473195f98c550c80657035b7e1))


### Documentation

* Add a brief intro notebook for bbq AI functions ([#2150](https://github.com/googleapis/python-bigquery-dataframes/issues/2150)) ([1f434fb](https://github.com/googleapis/python-bigquery-dataframes/commit/1f434fb5c7c00601654b3ab19c6ad7fceb258bd6))
* Fix ai function related docs ([#2149](https://github.com/googleapis/python-bigquery-dataframes/issues/2149)) ([93a0749](https://github.com/googleapis/python-bigquery-dataframes/commit/93a0749392b84f27162654fe5ea5baa329a23f99))
* Remove progress bar from getting started template ([#2143](https://github.com/googleapis/python-bigquery-dataframes/issues/2143)) ([d13abad](https://github.com/googleapis/python-bigquery-dataframes/commit/d13abadbcd68d03997e8dc11bb7a2b14bbd57fcc))

## [2.24.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.23.0...v2.24.0) (2025-10-07)


### Features

* Add ai.classify() to bigframes.bigquery package ([#2137](https://github.com/googleapis/python-bigquery-dataframes/issues/2137)) ([56e5033](https://github.com/googleapis/python-bigquery-dataframes/commit/56e50331d198b7f517f85695c208f893ab9389d2))
* Add ai.generate() to bigframes.bigquery module ([#2128](https://github.com/googleapis/python-bigquery-dataframes/issues/2128)) ([3810452](https://github.com/googleapis/python-bigquery-dataframes/commit/3810452f16d8d6c9d3eb9075f1537177d98b4725))
* Add ai.if_() and ai.score() to bigframes.bigquery package ([#2132](https://github.com/googleapis/python-bigquery-dataframes/issues/2132)) ([32502f4](https://github.com/googleapis/python-bigquery-dataframes/commit/32502f4195306d262788f39d1ab4206fc84ae50e))


### Bug Fixes

* Fix internal type errors with temporal accessors ([#2125](https://github.com/googleapis/python-bigquery-dataframes/issues/2125)) ([c390da1](https://github.com/googleapis/python-bigquery-dataframes/commit/c390da11b7c2aa710bc2fbc692efb9f06059e4c4))
* Fix row count local execution bug ([#2133](https://github.com/googleapis/python-bigquery-dataframes/issues/2133)) ([ece0762](https://github.com/googleapis/python-bigquery-dataframes/commit/ece07623e354a1dde2bd37020349e13f682e863f))
* Join on, how args are now positional ([#2140](https://github.com/googleapis/python-bigquery-dataframes/issues/2140)) ([b711815](https://github.com/googleapis/python-bigquery-dataframes/commit/b7118152bfecc6ecf67aa4df23ec3f0a2b08aa30))
* Only show JSON dtype warning when accessing dtypes directly ([#2136](https://github.com/googleapis/python-bigquery-dataframes/issues/2136)) ([eca22ee](https://github.com/googleapis/python-bigquery-dataframes/commit/eca22ee3104104cea96189391e527cad09bd7509))
* Remove noisy AmbiguousWindowWarning from partial ordering mode ([#2129](https://github.com/googleapis/python-bigquery-dataframes/issues/2129)) ([4607f86](https://github.com/googleapis/python-bigquery-dataframes/commit/4607f86ebd77b916aafc37f69725b676e203b332))


### Performance Improvements

* Scale read stream workers to cpu count ([#2135](https://github.com/googleapis/python-bigquery-dataframes/issues/2135)) ([67e46cd](https://github.com/googleapis/python-bigquery-dataframes/commit/67e46cd47933b84b55808003ed344b559e47c498))

## [2.23.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.22.0...v2.23.0) (2025-09-29)


### Features

* Add ai.generate_double to bigframes.bigquery package ([#2111](https://github.com/googleapis/python-bigquery-dataframes/issues/2111)) ([6b8154c](https://github.com/googleapis/python-bigquery-dataframes/commit/6b8154c578bb1a276e9cf8fe494d91f8cd6260f2))


### Bug Fixes

* Prevent invalid syntax for no-op .replace ops ([#2112](https://github.com/googleapis/python-bigquery-dataframes/issues/2112)) ([c311876](https://github.com/googleapis/python-bigquery-dataframes/commit/c311876b2adbc0b66ae5e463c6e56466c6a6a495))


### Documentation

* Add timedelta notebook sample ([#2124](https://github.com/googleapis/python-bigquery-dataframes/issues/2124)) ([d1a9888](https://github.com/googleapis/python-bigquery-dataframes/commit/d1a9888a2b47de6aca5dddc94d0c8f280344b58a))

## [2.22.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.21.0...v2.22.0) (2025-09-25)


### Features

* Add `GroupBy.__iter__` ([#1394](https://github.com/googleapis/python-bigquery-dataframes/issues/1394)) ([c56a78c](https://github.com/googleapis/python-bigquery-dataframes/commit/c56a78cd509a535d4998d5b9a99ec3ecd334b883))
* Add ai.generate_int to bigframes.bigquery package ([#2109](https://github.com/googleapis/python-bigquery-dataframes/issues/2109)) ([af6b862](https://github.com/googleapis/python-bigquery-dataframes/commit/af6b862de5c3921684210ec169338815f45b19dd))
* Add Groupby.describe() ([#2088](https://github.com/googleapis/python-bigquery-dataframes/issues/2088)) ([328a765](https://github.com/googleapis/python-bigquery-dataframes/commit/328a765e746138806a021bea22475e8c03512aeb))
* Implement `Index.to_list()` ([#2106](https://github.com/googleapis/python-bigquery-dataframes/issues/2106)) ([60056ca](https://github.com/googleapis/python-bigquery-dataframes/commit/60056ca06511f99092647fe55fc02eeab486b4ca))
* Implement inplace parameter for `DataFrame.drop` ([#2105](https://github.com/googleapis/python-bigquery-dataframes/issues/2105)) ([3487f13](https://github.com/googleapis/python-bigquery-dataframes/commit/3487f13d12e34999b385c2e11551b5e27bfbf4ff))
* Support callable for series map method ([#2100](https://github.com/googleapis/python-bigquery-dataframes/issues/2100)) ([ac25618](https://github.com/googleapis/python-bigquery-dataframes/commit/ac25618feed2da11fe4fb85058d498d262c085c0))
* Support df.info() with null index ([#2094](https://github.com/googleapis/python-bigquery-dataframes/issues/2094)) ([fb81eea](https://github.com/googleapis/python-bigquery-dataframes/commit/fb81eeaf13af059f32cb38e7f117fb3504243d51))


### Bug Fixes

* Avoid ibis fillna warning in compiler ([#2113](https://github.com/googleapis/python-bigquery-dataframes/issues/2113)) ([7ef667b](https://github.com/googleapis/python-bigquery-dataframes/commit/7ef667b0f46f13bcc8ad4f2ed8f81278132b5aec))
* Negative start and stop parameter values in Series.str.slice() ([#2104](https://github.com/googleapis/python-bigquery-dataframes/issues/2104)) ([f57a348](https://github.com/googleapis/python-bigquery-dataframes/commit/f57a348f1935a4e2bb14c501bb4c47cd552d102a))
* Throw type error for incomparable join keys ([#2098](https://github.com/googleapis/python-bigquery-dataframes/issues/2098)) ([9dc9695](https://github.com/googleapis/python-bigquery-dataframes/commit/9dc96959a84b751d18b290129c2926df6e50b3f5))
* Transformers with non-standard column names throw errors ([#2089](https://github.com/googleapis/python-bigquery-dataframes/issues/2089)) ([a2daa3f](https://github.com/googleapis/python-bigquery-dataframes/commit/a2daa3fffe6743327edb9f4c74db93198bd12f8e))

## [2.21.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.20.0...v2.21.0) (2025-09-17)


### Features

* Add bigframes.bigquery.to_json ([#2078](https://github.com/googleapis/python-bigquery-dataframes/issues/2078)) ([0fc795a](https://github.com/googleapis/python-bigquery-dataframes/commit/0fc795a9fb56f469b62603462c3f0f56f52bfe04))
* Support average='binary' in precision_score() ([#2080](https://github.com/googleapis/python-bigquery-dataframes/issues/2080)) ([920f381](https://github.com/googleapis/python-bigquery-dataframes/commit/920f381aec7e0a0b986886cdbc333e86335c6d7d))
* Support pandas series in ai.generate_bool ([#2086](https://github.com/googleapis/python-bigquery-dataframes/issues/2086)) ([a3de53f](https://github.com/googleapis/python-bigquery-dataframes/commit/a3de53f68b2a24f4ed85a474dfaff9b59570a2f1))


### Bug Fixes

* Allow bigframes.options.bigquery.credentials to be `None` ([#2092](https://github.com/googleapis/python-bigquery-dataframes/issues/2092)) ([78f4001](https://github.com/googleapis/python-bigquery-dataframes/commit/78f4001e8fcfc77fc82f3893d58e0d04c0f6d3db))

## [2.20.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.19.0...v2.20.0) (2025-09-16)


### Features

* Add `__dataframe__` interchange support ([#2063](https://github.com/googleapis/python-bigquery-dataframes/issues/2063)) ([3b46a0d](https://github.com/googleapis/python-bigquery-dataframes/commit/3b46a0d91eb379c61ced45ae0b25339281326c3d))
* Add ai_generate_bool to the bigframes.bigquery package ([#2060](https://github.com/googleapis/python-bigquery-dataframes/issues/2060)) ([70d6562](https://github.com/googleapis/python-bigquery-dataframes/commit/70d6562df64b2aef4ff0024df6f57702d52dcaf8))
* Add bigframes.bigquery.to_json_string ([#2076](https://github.com/googleapis/python-bigquery-dataframes/issues/2076)) ([41e8f33](https://github.com/googleapis/python-bigquery-dataframes/commit/41e8f33ceb46a7c2a75d1c59a4a3f2f9413d281d))
* Add rank(pct=True) support ([#2084](https://github.com/googleapis/python-bigquery-dataframes/issues/2084)) ([c1e871d](https://github.com/googleapis/python-bigquery-dataframes/commit/c1e871d9327bf6c920d17e1476fed3088d506f5f))
* Add StreamingDataFrame.to_bigtable and .to_pubsub start_timestamp parameter ([#2066](https://github.com/googleapis/python-bigquery-dataframes/issues/2066)) ([a63cbae](https://github.com/googleapis/python-bigquery-dataframes/commit/a63cbae24ff2dc191f0a53dced885bc95f38ec96))
* Can call agg with some callables ([#2055](https://github.com/googleapis/python-bigquery-dataframes/issues/2055)) ([17a1ed9](https://github.com/googleapis/python-bigquery-dataframes/commit/17a1ed99ec8c6d3215d3431848814d5d458d4ff1))
* Support astype to json ([#2073](https://github.com/googleapis/python-bigquery-dataframes/issues/2073)) ([6bd6738](https://github.com/googleapis/python-bigquery-dataframes/commit/6bd67386341de7a92ada948381702430c399406e))
* Support pandas.Index as key for DataFrame.__setitem__() ([#2062](https://github.com/googleapis/python-bigquery-dataframes/issues/2062)) ([b3cf824](https://github.com/googleapis/python-bigquery-dataframes/commit/b3cf8248e3b8ea76637ded64fb12028d439448d1))
* Support pd.cut() for array-like type ([#2064](https://github.com/googleapis/python-bigquery-dataframes/issues/2064)) ([21eb213](https://github.com/googleapis/python-bigquery-dataframes/commit/21eb213c5f0e0f696f2d1ca1f1263678d791cf7c))
* Support to cast struct to json ([#2067](https://github.com/googleapis/python-bigquery-dataframes/issues/2067)) ([b0ff718](https://github.com/googleapis/python-bigquery-dataframes/commit/b0ff718a04fadda33cfa3613b1d02822cde34bc2))


### Bug Fixes

* Deflake ai_gen_bool multimodel test ([#2085](https://github.com/googleapis/python-bigquery-dataframes/issues/2085)) ([566a37a](https://github.com/googleapis/python-bigquery-dataframes/commit/566a37a30ad5677aef0c5f79bdd46bca2139cc1e))
* Do not scroll page selector in anywidget `repr_mode` ([#2082](https://github.com/googleapis/python-bigquery-dataframes/issues/2082)) ([5ce5d63](https://github.com/googleapis/python-bigquery-dataframes/commit/5ce5d63fcb51bfb3df2769108b7486287896ccb9))
* Fix the potential invalid VPC egress configuration ([#2068](https://github.com/googleapis/python-bigquery-dataframes/issues/2068)) ([cce4966](https://github.com/googleapis/python-bigquery-dataframes/commit/cce496605385f2ac7ab0becc0773800ed5901aa5))
* Return a DataFrame containing query stats for all non-SELECT statements ([#2071](https://github.com/googleapis/python-bigquery-dataframes/issues/2071)) ([a52b913](https://github.com/googleapis/python-bigquery-dataframes/commit/a52b913d9d8794b4b959ea54744a38d9f2f174e7))
* Use the remote and managed functions for bigframes results ([#2079](https://github.com/googleapis/python-bigquery-dataframes/issues/2079)) ([49b91e8](https://github.com/googleapis/python-bigquery-dataframes/commit/49b91e878de651de23649756259ee35709e3f5a8))


### Performance Improvements

* Avoid re-authenticating if credentials have already been fetched ([#2058](https://github.com/googleapis/python-bigquery-dataframes/issues/2058)) ([913de1b](https://github.com/googleapis/python-bigquery-dataframes/commit/913de1b31f3bb0b306846fddae5dcaff6be3cec4))
* Improve apply axis=1 performance ([#2077](https://github.com/googleapis/python-bigquery-dataframes/issues/2077)) ([12e4380](https://github.com/googleapis/python-bigquery-dataframes/commit/12e438051134577e911c1a6ce9d5a5885a0b45ad))

## [2.19.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.18.0...v2.19.0) (2025-09-09)


### Features

* Add str.join method ([#2054](https://github.com/googleapis/python-bigquery-dataframes/issues/2054)) ([8804ada](https://github.com/googleapis/python-bigquery-dataframes/commit/8804adaf8ba23fdcad6e42a7bf034bd0a11c890f))
* Support display.max_colwidth option ([#2053](https://github.com/googleapis/python-bigquery-dataframes/issues/2053)) ([5229e07](https://github.com/googleapis/python-bigquery-dataframes/commit/5229e07b4535c01b0cdbd731455ff225a373b5c8))
* Support VPC egress setting in remote function ([#2059](https://github.com/googleapis/python-bigquery-dataframes/issues/2059)) ([5df779d](https://github.com/googleapis/python-bigquery-dataframes/commit/5df779d4f421d3ba777cfd928d99ca2e8a3f79ad))


### Bug Fixes

* Fix issue mishandling chunked array while loading data ([#2051](https://github.com/googleapis/python-bigquery-dataframes/issues/2051)) ([873d0ee](https://github.com/googleapis/python-bigquery-dataframes/commit/873d0eee474ed34f1d5164c37383f2737dbec4db))
* Remove warning for slot_millis_sum ([#2047](https://github.com/googleapis/python-bigquery-dataframes/issues/2047)) ([425a691](https://github.com/googleapis/python-bigquery-dataframes/commit/425a6917d5442eeb4df486c6eed1fd136bbcedfb))

## [2.18.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.17.0...v2.18.0) (2025-09-03)


### ⚠ BREAKING CHANGES

* add `allow_large_results` option to `read_gbq_query`, aligning with `bpd.options.compute.allow_large_results` option ([#1935](https://github.com/googleapis/python-bigquery-dataframes/issues/1935))

### Features

* Add `allow_large_results` option to `read_gbq_query`, aligning with `bpd.options.compute.allow_large_results` option ([#1935](https://github.com/googleapis/python-bigquery-dataframes/issues/1935)) ([a7963fe](https://github.com/googleapis/python-bigquery-dataframes/commit/a7963fe57a0e141debf726f0bc7b0e953ebe9634))
* Add parameter shuffle for ml.model_selection.train_test_split ([#2030](https://github.com/googleapis/python-bigquery-dataframes/issues/2030)) ([2c72c56](https://github.com/googleapis/python-bigquery-dataframes/commit/2c72c56fb5893eb01d5aec6273d11945c9c532c5))
* Can pivot unordered, unindexed dataframe ([#2040](https://github.com/googleapis/python-bigquery-dataframes/issues/2040)) ([1a0f710](https://github.com/googleapis/python-bigquery-dataframes/commit/1a0f710ac11418fd71ab3373f3f6002fa581b180))
* Local date accessor execution support ([#2034](https://github.com/googleapis/python-bigquery-dataframes/issues/2034)) ([7ac6fe1](https://github.com/googleapis/python-bigquery-dataframes/commit/7ac6fe16f7f2c09d2efac6ab813ec841c21baef8))
* Support args in dataframe apply method ([#2026](https://github.com/googleapis/python-bigquery-dataframes/issues/2026)) ([164c481](https://github.com/googleapis/python-bigquery-dataframes/commit/164c4818bc4ff2990dca16b9f22a798f47e0a60b))
* Support args in series apply method ([#2013](https://github.com/googleapis/python-bigquery-dataframes/issues/2013)) ([d9d725c](https://github.com/googleapis/python-bigquery-dataframes/commit/d9d725cfbc3dca9e66b460cae4084e25162f2acf))
* Support callable for dataframe mask method ([#2020](https://github.com/googleapis/python-bigquery-dataframes/issues/2020)) ([9d4504b](https://github.com/googleapis/python-bigquery-dataframes/commit/9d4504be310d38b63515d67c0f60d2e48e68c7b5))
* Support multi-column assignment for DataFrame ([#2028](https://github.com/googleapis/python-bigquery-dataframes/issues/2028)) ([ba0d23b](https://github.com/googleapis/python-bigquery-dataframes/commit/ba0d23b59c44ba5a46ace8182ad0e0cfc703b3ab))
* Support string matching in local executor ([#2032](https://github.com/googleapis/python-bigquery-dataframes/issues/2032)) ([c0b54f0](https://github.com/googleapis/python-bigquery-dataframes/commit/c0b54f03849ee3115413670e690e68f3ef10f2ec))


### Bug Fixes

* Fix scalar op lowering tree walk ([#2029](https://github.com/googleapis/python-bigquery-dataframes/issues/2029)) ([935af10](https://github.com/googleapis/python-bigquery-dataframes/commit/935af107ef98837fb2b81d72185d0b6a9e09fbcf))
* Read_csv fails when check file size for wildcard gcs files ([#2019](https://github.com/googleapis/python-bigquery-dataframes/issues/2019)) ([b0d620b](https://github.com/googleapis/python-bigquery-dataframes/commit/b0d620bbe8227189bbdc2ba5a913b03c70575296))
* Resolve the validation issue for other arg in dataframe where method ([#2042](https://github.com/googleapis/python-bigquery-dataframes/issues/2042)) ([8689199](https://github.com/googleapis/python-bigquery-dataframes/commit/8689199aa82212ed300fff592097093812e0290e))


### Performance Improvements

* Improve axis=1 aggregation performance ([#2036](https://github.com/googleapis/python-bigquery-dataframes/issues/2036)) ([fbb2094](https://github.com/googleapis/python-bigquery-dataframes/commit/fbb209468297a8057d9d49c40e425c3bfdeb92bd))
* Improve iter_nodes_topo performance using Kahn's algorithm ([#2038](https://github.com/googleapis/python-bigquery-dataframes/issues/2038)) ([3961637](https://github.com/googleapis/python-bigquery-dataframes/commit/39616374bba424996ebeb9a12096bfaf22660b44))

## [2.17.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.16.0...v2.17.0) (2025-08-22)


### Features

* Add isin local execution impl ([#1993](https://github.com/googleapis/python-bigquery-dataframes/issues/1993)) ([26df6e6](https://github.com/googleapis/python-bigquery-dataframes/commit/26df6e691bb27ed09322a81214faedbf3639b32e))
* Add reset_index names, col_level, col_fill, allow_duplicates args ([#2017](https://github.com/googleapis/python-bigquery-dataframes/issues/2017)) ([c02a1b6](https://github.com/googleapis/python-bigquery-dataframes/commit/c02a1b67d27758815430bb8006ac3a72cea55a89))
* Support callable for series mask method ([#2014](https://github.com/googleapis/python-bigquery-dataframes/issues/2014)) ([5ac32eb](https://github.com/googleapis/python-bigquery-dataframes/commit/5ac32ebe17cfda447870859f5dd344b082b4d3d0))

## [2.16.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.15.0...v2.16.0) (2025-08-20)


### Features

* Add `bigframes.pandas.options.display.precision` option ([#1979](https://github.com/googleapis/python-bigquery-dataframes/issues/1979)) ([15e6175](https://github.com/googleapis/python-bigquery-dataframes/commit/15e6175ec0aeb1b7b02d0bba9e8e1e018bd11c31))
* Add level, inplace params to reset_index ([#1988](https://github.com/googleapis/python-bigquery-dataframes/issues/1988)) ([3446950](https://github.com/googleapis/python-bigquery-dataframes/commit/34469504b79a082d3380f9f25c597483aef2068a))
* Add ML code samples from dbt blog post ([#1978](https://github.com/googleapis/python-bigquery-dataframes/issues/1978)) ([ebaa244](https://github.com/googleapis/python-bigquery-dataframes/commit/ebaa244a9eb7b87f7f9fd9c3bebe5c7db24cd013))
* Add where, coalesce, fillna, casewhen, invert local impl ([#1976](https://github.com/googleapis/python-bigquery-dataframes/issues/1976)) ([f7f686c](https://github.com/googleapis/python-bigquery-dataframes/commit/f7f686cf85ab7e265d9c07ebc7f0cd59babc5357))
* Adjust anywidget CSS to prevent overflow ([#1981](https://github.com/googleapis/python-bigquery-dataframes/issues/1981)) ([204f083](https://github.com/googleapis/python-bigquery-dataframes/commit/204f083a2f00fcc9fd1500dcd7a738eda3904d2f))
* Format page number in table widget ([#1992](https://github.com/googleapis/python-bigquery-dataframes/issues/1992)) ([e83836e](https://github.com/googleapis/python-bigquery-dataframes/commit/e83836e8e1357f009f3f95666f1661bdbe0d3751))
* Or, And, Xor can execute locally ([#1994](https://github.com/googleapis/python-bigquery-dataframes/issues/1994)) ([59c52a5](https://github.com/googleapis/python-bigquery-dataframes/commit/59c52a55ebea697855eb4c70529e226cc077141f))
* Support callable bigframes function for dataframe where ([#1990](https://github.com/googleapis/python-bigquery-dataframes/issues/1990)) ([44c1ec4](https://github.com/googleapis/python-bigquery-dataframes/commit/44c1ec48cc4db1c4c9c15ec1fab43d4ef0758e56))
* Support callable for series where method ([#2005](https://github.com/googleapis/python-bigquery-dataframes/issues/2005)) ([768b82a](https://github.com/googleapis/python-bigquery-dataframes/commit/768b82af96a5dd0c434edcb171036eb42cfb9b41))
* When using `repr_mode = "anywidget"`, numeric values align right ([15e6175](https://github.com/googleapis/python-bigquery-dataframes/commit/15e6175ec0aeb1b7b02d0bba9e8e1e018bd11c31))


### Bug Fixes

* Address the packages issue for bigframes function ([#1991](https://github.com/googleapis/python-bigquery-dataframes/issues/1991)) ([68f1d22](https://github.com/googleapis/python-bigquery-dataframes/commit/68f1d22d5ed8457a5cabc7751ed1d178063dd63e))
* Correct pypdf dependency specifier for remote PDF functions ([#1980](https://github.com/googleapis/python-bigquery-dataframes/issues/1980)) ([0bd5e1b](https://github.com/googleapis/python-bigquery-dataframes/commit/0bd5e1b3c004124d2100c3fbec2fbe1e965d1e96))
* Enable default retries in calls to BQ Storage Read API ([#1985](https://github.com/googleapis/python-bigquery-dataframes/issues/1985)) ([f25d7bd](https://github.com/googleapis/python-bigquery-dataframes/commit/f25d7bd30800dffa65b6c31b0b7ac711a13d790f))
* Fix the copyright year in dbt sample files ([#1996](https://github.com/googleapis/python-bigquery-dataframes/issues/1996)) ([fad5722](https://github.com/googleapis/python-bigquery-dataframes/commit/fad57223d129f0c95d0c6a066179bb66880edd06))


### Performance Improvements

* Faster session startup by defering anon dataset fetch ([#1982](https://github.com/googleapis/python-bigquery-dataframes/issues/1982)) ([2720c4c](https://github.com/googleapis/python-bigquery-dataframes/commit/2720c4cf070bf57a0930d7623bfc41d89cc053ee))


### Documentation

* Add examples of running bigframes in kaggle ([#2002](https://github.com/googleapis/python-bigquery-dataframes/issues/2002)) ([7d89d76](https://github.com/googleapis/python-bigquery-dataframes/commit/7d89d76976595b75cb0105fbe7b4f7ca2fdf49f2))
* Remove preview warning from partial ordering mode sample notebook ([#1986](https://github.com/googleapis/python-bigquery-dataframes/issues/1986)) ([132e0ed](https://github.com/googleapis/python-bigquery-dataframes/commit/132e0edfe9f96c15753649d77fcb6edd0b0708a3))

## [2.15.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.14.0...v2.15.0) (2025-08-11)


### Features

* Add `st_buffer`, `st_centroid`, and `st_convexhull` and their corresponding GeoSeries methods ([#1963](https://github.com/googleapis/python-bigquery-dataframes/issues/1963)) ([c4c7fa5](https://github.com/googleapis/python-bigquery-dataframes/commit/c4c7fa578e135e7f0e31ad3063db379514957acc))
* Add first, last support to GroupBy ([#1969](https://github.com/googleapis/python-bigquery-dataframes/issues/1969)) ([41dda88](https://github.com/googleapis/python-bigquery-dataframes/commit/41dda889860c0ed8ca2eab81b34a9d71372c69f7))
* Add value_counts to GroupBy classes ([#1974](https://github.com/googleapis/python-bigquery-dataframes/issues/1974)) ([82175a4](https://github.com/googleapis/python-bigquery-dataframes/commit/82175a4d0fa41d8aee11efdf8778a21bb70b1c0f))
* Allow callable as a conditional or replacement input in DataFrame.where ([#1971](https://github.com/googleapis/python-bigquery-dataframes/issues/1971)) ([a8d57d2](https://github.com/googleapis/python-bigquery-dataframes/commit/a8d57d2f7075158eff69ec65a14c232756ab72a6))
* Can cast locally in hybrid engine ([#1944](https://github.com/googleapis/python-bigquery-dataframes/issues/1944)) ([d9bc4a5](https://github.com/googleapis/python-bigquery-dataframes/commit/d9bc4a5940e9930d5e3c3bfffdadd2f91f96b53b))
* Df.join lsuffix and rsuffix support ([#1857](https://github.com/googleapis/python-bigquery-dataframes/issues/1857)) ([26515c3](https://github.com/googleapis/python-bigquery-dataframes/commit/26515c34c4f0a5e4602d2f59bf229d41e0fc9196))


### Bug Fixes

* Add warnings for duplicated or conflicting type hints in bigfram… ([#1956](https://github.com/googleapis/python-bigquery-dataframes/issues/1956)) ([d38e42c](https://github.com/googleapis/python-bigquery-dataframes/commit/d38e42ce689e65f57223e9a8b14c4262cba08966))
* Make `remote_function` more robust when there are `create_function` retries ([#1973](https://github.com/googleapis/python-bigquery-dataframes/issues/1973)) ([cd954ac](https://github.com/googleapis/python-bigquery-dataframes/commit/cd954ac07ad5e5820a20b941d3c6cab7cfcc1f29))
* Make ExecutionMetrics stats tracking more robust to missing stats ([#1977](https://github.com/googleapis/python-bigquery-dataframes/issues/1977)) ([feb3ff4](https://github.com/googleapis/python-bigquery-dataframes/commit/feb3ff4b543eb8acbf6adf335b67a266a1cf4297))


### Performance Improvements

* Remove an unnecessary extra `dry_run` query from `read_gbq_table` ([#1972](https://github.com/googleapis/python-bigquery-dataframes/issues/1972)) ([d17b711](https://github.com/googleapis/python-bigquery-dataframes/commit/d17b711750d281ef3efd42c160f3784cd60021ae))


### Documentation

* Divide BQ DataFrames quickstart code cell ([#1975](https://github.com/googleapis/python-bigquery-dataframes/issues/1975)) ([fedb8f2](https://github.com/googleapis/python-bigquery-dataframes/commit/fedb8f23120aa315c7e9dd6f1bf1255ccf1ebc48))

## [2.14.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.13.0...v2.14.0) (2025-08-05)


### Features

* Dynamic table width for better display across devices (https://github.com/googleapis/python-bigquery-dataframes/issues/1948) ([a6d30ae](https://github.com/googleapis/python-bigquery-dataframes/commit/a6d30ae3f4358925c999c53b558c1ecd3ee03e6c)) ([a6d30ae](https://github.com/googleapis/python-bigquery-dataframes/commit/a6d30ae3f4358925c999c53b558c1ecd3ee03e6c))
* Retry AI/ML jobs that fail more often ([#1965](https://github.com/googleapis/python-bigquery-dataframes/issues/1965)) ([25bde9f](https://github.com/googleapis/python-bigquery-dataframes/commit/25bde9f9b89112db0efcc119bf29b6d1f3896c33))
* Support series input in managed function ([#1920](https://github.com/googleapis/python-bigquery-dataframes/issues/1920)) ([62a189f](https://github.com/googleapis/python-bigquery-dataframes/commit/62a189f4d69f6c05fe348a1acd1fbac364fa60b9))


### Bug Fixes

* Enhance type error messages for bigframes functions ([#1958](https://github.com/googleapis/python-bigquery-dataframes/issues/1958)) ([770918e](https://github.com/googleapis/python-bigquery-dataframes/commit/770918e998bf1fde7a656e8f8a0ff0a8c68509f2))


### Performance Improvements

* Use promote_offsets for consistent row number generation for index.get_loc  ([#1957](https://github.com/googleapis/python-bigquery-dataframes/issues/1957)) ([c67a25a](https://github.com/googleapis/python-bigquery-dataframes/commit/c67a25a879ab2a35ca9053a81c9c85b5660206ae))


### Documentation

* Add code snippet for storing dataframes to a CSV file ([#1943](https://github.com/googleapis/python-bigquery-dataframes/issues/1943)) ([a511e09](https://github.com/googleapis/python-bigquery-dataframes/commit/a511e09e6924d2e8302af2eb4a602c6b9e5d2d72))
* Add code snippet for storing dataframes to a CSV file ([#1953](https://github.com/googleapis/python-bigquery-dataframes/issues/1953)) ([a298a02](https://github.com/googleapis/python-bigquery-dataframes/commit/a298a02b451f03ca200fe0756b9a7b57e3d1bf0e))

## [2.13.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.12.0...v2.13.0) (2025-07-25)


### Features

* _read_gbq_colab creates hybrid session ([#1901](https://github.com/googleapis/python-bigquery-dataframes/issues/1901)) ([31b17b0](https://github.com/googleapis/python-bigquery-dataframes/commit/31b17b01706ccfcee9a2d838c43a9609ec4dc218))
* Add CSS styling for TableWidget pagination interface ([#1934](https://github.com/googleapis/python-bigquery-dataframes/issues/1934)) ([5b232d7](https://github.com/googleapis/python-bigquery-dataframes/commit/5b232d7e33563196316f5dbb50b28c6be388d440))
* Add row numbering local pushdown in hybrid execution ([#1932](https://github.com/googleapis/python-bigquery-dataframes/issues/1932)) ([92a2377](https://github.com/googleapis/python-bigquery-dataframes/commit/92a237712aa4ce516b1a44748127b34d7780fff6))
* Implement Index.get_loc ([#1921](https://github.com/googleapis/python-bigquery-dataframes/issues/1921)) ([bbbcaf3](https://github.com/googleapis/python-bigquery-dataframes/commit/bbbcaf35df113617fd6bb8ae36468cf3f7ab493b))


### Bug Fixes

* Add license header and correct issues in dbt sample ([#1931](https://github.com/googleapis/python-bigquery-dataframes/issues/1931)) ([ab01b0a](https://github.com/googleapis/python-bigquery-dataframes/commit/ab01b0a236ffc7b667f258e0497105ea5c3d3aab))


### Dependencies

* Replace `google-cloud-iam` with `grpc-google-iam-v1` ([#1864](https://github.com/googleapis/python-bigquery-dataframes/issues/1864)) ([e5ff8f7](https://github.com/googleapis/python-bigquery-dataframes/commit/e5ff8f7d9fdac3ea47dabcc80a2598d601f39e64))

## [2.12.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.11.0...v2.12.0) (2025-07-23)


### Features

* Add code samples for dbt bigframes integration ([#1898](https://github.com/googleapis/python-bigquery-dataframes/issues/1898)) ([7e03252](https://github.com/googleapis/python-bigquery-dataframes/commit/7e03252d31e505731db113eb38af77842bf29b9b))
* Add isin local execution to hybrid engine ([#1915](https://github.com/googleapis/python-bigquery-dataframes/issues/1915)) ([c0cefd3](https://github.com/googleapis/python-bigquery-dataframes/commit/c0cefd36cfd55962b86178d2a612d625ed17f79c))
* Add ml.metrics.mean_absolute_error method ([#1910](https://github.com/googleapis/python-bigquery-dataframes/issues/1910)) ([15b8449](https://github.com/googleapis/python-bigquery-dataframes/commit/15b8449dc5ad0c8190a5cbf47894436de18c8e88))
* Allow local arithmetic execution in hybrid engine ([#1906](https://github.com/googleapis/python-bigquery-dataframes/issues/1906)) ([ebdcd02](https://github.com/googleapis/python-bigquery-dataframes/commit/ebdcd0240f0d8edaef3094b3a4e664b4a84d4a25))
* Provide day_of_year and day_of_week for dt accessor ([#1911](https://github.com/googleapis/python-bigquery-dataframes/issues/1911)) ([40e7638](https://github.com/googleapis/python-bigquery-dataframes/commit/40e76383948a79bde48108f6180fd6ae2b3d0875))
* Support params `max_batching_rows`, `container_cpu`, and `container_memory` for `udf` ([#1897](https://github.com/googleapis/python-bigquery-dataframes/issues/1897)) ([8baa912](https://github.com/googleapis/python-bigquery-dataframes/commit/8baa9126e595ae682469a6bb462244240699f57f))
* Support typed pyarrow.Scalar in assignment  ([#1930](https://github.com/googleapis/python-bigquery-dataframes/issues/1930)) ([cd28e12](https://github.com/googleapis/python-bigquery-dataframes/commit/cd28e12b3f70a6934a68963a7f25dbd5e3c67335))


### Bug Fixes

* Correct min field from max() to min() in remote function tests ([#1917](https://github.com/googleapis/python-bigquery-dataframes/issues/1917)) ([d5c54fc](https://github.com/googleapis/python-bigquery-dataframes/commit/d5c54fca32ed75c1aef52c99781db7f8ac7426e1))
* Resolve location reset issue in bigquery options ([#1914](https://github.com/googleapis/python-bigquery-dataframes/issues/1914)) ([c15cb8a](https://github.com/googleapis/python-bigquery-dataframes/commit/c15cb8a1a9c834c2c1c2984930415b246f3f948b))
* Series.str.isdigit in unicode superscripts and fractions ([#1924](https://github.com/googleapis/python-bigquery-dataframes/issues/1924)) ([8d46c36](https://github.com/googleapis/python-bigquery-dataframes/commit/8d46c36da7881a99861166c03a0831beff8ee0dd))


### Documentation

* Add code snippets for session and IO public docs ([#1919](https://github.com/googleapis/python-bigquery-dataframes/issues/1919)) ([6e01cbe](https://github.com/googleapis/python-bigquery-dataframes/commit/6e01cbec0dcf40e528b4a96e944681df18773c11))
* Add snippets for performance optimization doc ([#1923](https://github.com/googleapis/python-bigquery-dataframes/issues/1923)) ([4da309e](https://github.com/googleapis/python-bigquery-dataframes/commit/4da309e27bd58a685e8aca953717da75d4ba5305))

## [2.11.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.10.0...v2.11.0) (2025-07-15)


### Features

* Add `__contains__` to Index, Series, DataFrame ([#1899](https://github.com/googleapis/python-bigquery-dataframes/issues/1899)) ([07222bf](https://github.com/googleapis/python-bigquery-dataframes/commit/07222bfe2f6ae60859d33eb366598d7dee5c0572))
* Add `thresh` param for Dataframe.dropna ([#1885](https://github.com/googleapis/python-bigquery-dataframes/issues/1885)) ([1395a50](https://github.com/googleapis/python-bigquery-dataframes/commit/1395a502ffa0faf4b7462045dcb0657485c7ce26))
* Add concat pushdown for hybrid engine ([#1891](https://github.com/googleapis/python-bigquery-dataframes/issues/1891)) ([813624d](https://github.com/googleapis/python-bigquery-dataframes/commit/813624dddfd4f2396c8b1c9768c0c831bb0681ac))
* Add pagination buttons (prev/next) to anywidget mode for DataFrames ([#1841](https://github.com/googleapis/python-bigquery-dataframes/issues/1841)) ([8eca767](https://github.com/googleapis/python-bigquery-dataframes/commit/8eca767425c7910c8f907747a8a8b335df0caa1a))
* Add total_rows property to pandas batches iterator ([#1888](https://github.com/googleapis/python-bigquery-dataframes/issues/1888)) ([e3f5e65](https://github.com/googleapis/python-bigquery-dataframes/commit/e3f5e6539d220f8da57f08f67863ade29df4ad16))
* Hybrid engine local join support ([#1900](https://github.com/googleapis/python-bigquery-dataframes/issues/1900)) ([1aa7950](https://github.com/googleapis/python-bigquery-dataframes/commit/1aa7950334bdc826a9a0a1894dad67ca6f755425))
* Support `date` data type for to_datetime() ([#1902](https://github.com/googleapis/python-bigquery-dataframes/issues/1902)) ([24050cb](https://github.com/googleapis/python-bigquery-dataframes/commit/24050cb00247f68eb4ece827fd31ee1dd8b25380))
* Support bpd.Series(json_data, dtype="json") ([#1882](https://github.com/googleapis/python-bigquery-dataframes/issues/1882)) ([05cb7d0](https://github.com/googleapis/python-bigquery-dataframes/commit/05cb7d0bc3599054acf8ecb8b15eb2045b9bf463))


### Bug Fixes

* Bpd.merge on common columns ([#1905](https://github.com/googleapis/python-bigquery-dataframes/issues/1905)) ([a1fa112](https://github.com/googleapis/python-bigquery-dataframes/commit/a1fa11291305a1da0d6a4121436c09ed04b224b5))
* DataFrame string addition respects order ([#1894](https://github.com/googleapis/python-bigquery-dataframes/issues/1894)) ([52c8233](https://github.com/googleapis/python-bigquery-dataframes/commit/52c82337bcc9f2b6cfc1c6ac14deb83b693d114d))
* Show slot_millis_sum warning only when `allow_large_results=False` ([#1892](https://github.com/googleapis/python-bigquery-dataframes/issues/1892)) ([25efabc](https://github.com/googleapis/python-bigquery-dataframes/commit/25efabc4897e0692725618ce43134127a7f2c2ee))
* Used query row count metadata instead of table metadata ([#1893](https://github.com/googleapis/python-bigquery-dataframes/issues/1893)) ([e1ebc53](https://github.com/googleapis/python-bigquery-dataframes/commit/e1ebc5369a416280cec0ab1513e763b7a2fe3c20))

## [2.10.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.9.0...v2.10.0) (2025-07-08)


### Features

* `df.to_pandas_batches()` returns one empty DataFrame if `df` is empty ([#1878](https://github.com/googleapis/python-bigquery-dataframes/issues/1878)) ([e43d15d](https://github.com/googleapis/python-bigquery-dataframes/commit/e43d15d535d6d5fd73c33967271f3591c41dffb3))
* Add filter pushdown to hybrid engine ([#1871](https://github.com/googleapis/python-bigquery-dataframes/issues/1871)) ([6454aff](https://github.com/googleapis/python-bigquery-dataframes/commit/6454aff726dee791acbac98f893075ee5ee6d9a1))
* Add simple stats support to hybrid local pushdown ([#1873](https://github.com/googleapis/python-bigquery-dataframes/issues/1873)) ([8715105](https://github.com/googleapis/python-bigquery-dataframes/commit/8715105239216bffe899ddcbb15805f2e3063af4))


### Bug Fixes

* Fix issues where duration type returned as int ([#1875](https://github.com/googleapis/python-bigquery-dataframes/issues/1875)) ([f30f750](https://github.com/googleapis/python-bigquery-dataframes/commit/f30f75053a6966abd1a6a644c23efb86b2ac568d))


### Documentation

* Update gsutil commands to gcloud commands ([#1876](https://github.com/googleapis/python-bigquery-dataframes/issues/1876)) ([c289f70](https://github.com/googleapis/python-bigquery-dataframes/commit/c289f7061320ec6d9de099cab2416cc9f289baac))

## [2.9.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.8.0...v2.9.0) (2025-06-30)


### Features

* Add `bpd.read_arrow` to convert an Arrow object into a bigframes DataFrame ([#1855](https://github.com/googleapis/python-bigquery-dataframes/issues/1855)) ([633bf98](https://github.com/googleapis/python-bigquery-dataframes/commit/633bf98fde33264be4fc9d7454e541c560589152))
* Add experimental polars execution ([#1747](https://github.com/googleapis/python-bigquery-dataframes/issues/1747)) ([daf0c3b](https://github.com/googleapis/python-bigquery-dataframes/commit/daf0c3b349fb1e85e7070c54a2d3f5460f5e40c9))
* Add size op support in local engine ([#1865](https://github.com/googleapis/python-bigquery-dataframes/issues/1865)) ([942e66c](https://github.com/googleapis/python-bigquery-dataframes/commit/942e66c483c9afbb680a7af56c9e9a76172a33e1))
* Create `deploy_remote_function` and `deploy_udf` functions to immediately deploy functions to BigQuery ([#1832](https://github.com/googleapis/python-bigquery-dataframes/issues/1832)) ([c706759](https://github.com/googleapis/python-bigquery-dataframes/commit/c706759b85359b6d23ce3449f6ab138ad2d22f9d))
* Support index item assign in Series ([#1868](https://github.com/googleapis/python-bigquery-dataframes/issues/1868)) ([c5d251a](https://github.com/googleapis/python-bigquery-dataframes/commit/c5d251a1d454bb4ef55ea9905faeadd646a23b14))
* Support item assignment in series ([#1859](https://github.com/googleapis/python-bigquery-dataframes/issues/1859)) ([25684ff](https://github.com/googleapis/python-bigquery-dataframes/commit/25684ff60367f49dd318d4677a7438abdc98bff9))
* Support local execution of comparison ops ([#1849](https://github.com/googleapis/python-bigquery-dataframes/issues/1849)) ([1c45ccb](https://github.com/googleapis/python-bigquery-dataframes/commit/1c45ccb133091aa85bc34450704fc8cab3d9296b))


### Bug Fixes

* Fix bug selecting column repeatedly ([#1858](https://github.com/googleapis/python-bigquery-dataframes/issues/1858)) ([cc339e9](https://github.com/googleapis/python-bigquery-dataframes/commit/cc339e9938129cac896460e3a794b3ec8479fa4a))
* Fix bug with DataFrame.agg for string values ([#1870](https://github.com/googleapis/python-bigquery-dataframes/issues/1870)) ([81e4d64](https://github.com/googleapis/python-bigquery-dataframes/commit/81e4d64c5a3bd8d30edaf909d0bef2d1d1a51c01))
* Generate GoogleSQL instead of legacy SQL data types for `dry_run=True` from `bpd._read_gbq_colab` with local pandas DataFrame ([#1867](https://github.com/googleapis/python-bigquery-dataframes/issues/1867)) ([fab3c38](https://github.com/googleapis/python-bigquery-dataframes/commit/fab3c387b2ad66043244fa813a366e613b41c60f))
* Revert dict back to protobuf in the iam binding update ([#1838](https://github.com/googleapis/python-bigquery-dataframes/issues/1838)) ([9fb3cb4](https://github.com/googleapis/python-bigquery-dataframes/commit/9fb3cb444607df6736d383a2807059bca470c453))


### Documentation

* Add data visualization samples for public doc ([#1847](https://github.com/googleapis/python-bigquery-dataframes/issues/1847)) ([15e1277](https://github.com/googleapis/python-bigquery-dataframes/commit/15e1277b1413de18a5e36f72959a99701d6df08b))
* Changed broken logo ([#1866](https://github.com/googleapis/python-bigquery-dataframes/issues/1866)) ([e3c06b4](https://github.com/googleapis/python-bigquery-dataframes/commit/e3c06b4a07d0669a42460d081f1582b681ae3dd5))
* Update ai.forecast notebook ([#1844](https://github.com/googleapis/python-bigquery-dataframes/issues/1844)) ([1863538](https://github.com/googleapis/python-bigquery-dataframes/commit/186353888db537b561ee994256f998df361b4071))

## [2.8.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.7.0...v2.8.0) (2025-06-23)


### ⚠ BREAKING CHANGES

* add required param 'engine' to multimodal functions ([#1834](https://github.com/googleapis/python-bigquery-dataframes/issues/1834))

### Features

* Add `bpd.options.compute.maximum_result_rows` option to limit client data download ([#1829](https://github.com/googleapis/python-bigquery-dataframes/issues/1829)) ([e22a3f6](https://github.com/googleapis/python-bigquery-dataframes/commit/e22a3f61a02cc1b7a5155556e5a07a1a2fea1d82))
* Add `bpd.options.display.repr_mode = "anywidget"` to create an interactive display of the results ([#1820](https://github.com/googleapis/python-bigquery-dataframes/issues/1820)) ([be0a3cf](https://github.com/googleapis/python-bigquery-dataframes/commit/be0a3cf7711dadc68d8366ea90b99855773e2a2e))
* Add DataFrame.ai.forecast() support ([#1828](https://github.com/googleapis/python-bigquery-dataframes/issues/1828)) ([7bc7f36](https://github.com/googleapis/python-bigquery-dataframes/commit/7bc7f36fc20d233f4cf5ed688cc5dcaf100ce4fb))
* Add describe() method to Series ([#1827](https://github.com/googleapis/python-bigquery-dataframes/issues/1827)) ([a4205f8](https://github.com/googleapis/python-bigquery-dataframes/commit/a4205f882012820c034cb15d73b2768ec4ad3ac8))
* Add required param 'engine' to multimodal functions ([#1834](https://github.com/googleapis/python-bigquery-dataframes/issues/1834)) ([37666e4](https://github.com/googleapis/python-bigquery-dataframes/commit/37666e4c137d52c28ab13477dfbcc6e92b913334))


### Performance Improvements

* Produce simpler sql ([#1836](https://github.com/googleapis/python-bigquery-dataframes/issues/1836)) ([cf9c22a](https://github.com/googleapis/python-bigquery-dataframes/commit/cf9c22a09c4e668a598fa1dad0f6a07b59bc6524))


### Documentation

* Add ai.forecast notebook ([#1840](https://github.com/googleapis/python-bigquery-dataframes/issues/1840)) ([2430497](https://github.com/googleapis/python-bigquery-dataframes/commit/24304972fdbdfd12c25c7f4ef5a7b280f334801a))

## [2.7.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.6.0...v2.7.0) (2025-06-16)


### Features

* Add bbq.json_query_array and warn bbq.json_extract_array deprecated ([#1811](https://github.com/googleapis/python-bigquery-dataframes/issues/1811)) ([dc9eb27](https://github.com/googleapis/python-bigquery-dataframes/commit/dc9eb27fa75e90c2c95a0619551bf67aea6ef63b))
* Add bbq.json_value_array and deprecate bbq.json_extract_string_array ([#1818](https://github.com/googleapis/python-bigquery-dataframes/issues/1818)) ([019051e](https://github.com/googleapis/python-bigquery-dataframes/commit/019051e453d81769891aa398475ebd04d1826e81))
* Add groupby cumcount ([#1798](https://github.com/googleapis/python-bigquery-dataframes/issues/1798)) ([18f43e8](https://github.com/googleapis/python-bigquery-dataframes/commit/18f43e8b58e03a27b021bce07566a3d006ac3679))
* Support custom build service account in `remote_function` ([#1796](https://github.com/googleapis/python-bigquery-dataframes/issues/1796)) ([e586151](https://github.com/googleapis/python-bigquery-dataframes/commit/e586151df81917b49f702ae496aaacbd02931636))


### Bug Fixes

* Correct read_csv behaviours with use_cols, names, index_col ([#1804](https://github.com/googleapis/python-bigquery-dataframes/issues/1804)) ([855031a](https://github.com/googleapis/python-bigquery-dataframes/commit/855031a316a6957731a5d1c5e59dedb9757d9f7a))
* Fix single row broadcast with null index ([#1803](https://github.com/googleapis/python-bigquery-dataframes/issues/1803)) ([080eb7b](https://github.com/googleapis/python-bigquery-dataframes/commit/080eb7be3cde591e08cad0d5c52c68cc0b25ade8))


### Documentation

* Document how to use ai.map() for information extraction ([#1808](https://github.com/googleapis/python-bigquery-dataframes/issues/1808)) ([b586746](https://github.com/googleapis/python-bigquery-dataframes/commit/b5867464a5bf30300dcfc069eda546b11f03146c))
* Rearrange README.rst to include a short code sample ([#1812](https://github.com/googleapis/python-bigquery-dataframes/issues/1812)) ([f6265db](https://github.com/googleapis/python-bigquery-dataframes/commit/f6265dbb8e22de81bb59c7def175cd325e85c041))
* Use pandas API instead of pandas-like or pandas-compatible ([#1825](https://github.com/googleapis/python-bigquery-dataframes/issues/1825)) ([aa32369](https://github.com/googleapis/python-bigquery-dataframes/commit/aa323694e161f558bc5e60490c2f21008961e2ca))

## [2.6.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.5.0...v2.6.0) (2025-06-09)


### Features

* Add blob.transcribe function ([#1773](https://github.com/googleapis/python-bigquery-dataframes/issues/1773)) ([86159a7](https://github.com/googleapis/python-bigquery-dataframes/commit/86159a7d24102574c26764a056478757844e2eca))
* Implement ai.classify() ([#1781](https://github.com/googleapis/python-bigquery-dataframes/issues/1781)) ([8af26d0](https://github.com/googleapis/python-bigquery-dataframes/commit/8af26d07cf3e8b22e0c69dd0172352fadc1857d8))
* Implement item() for Series and Index ([#1792](https://github.com/googleapis/python-bigquery-dataframes/issues/1792)) ([d2154c8](https://github.com/googleapis/python-bigquery-dataframes/commit/d2154c82fa0fed6e89c47db747d3c9cd57f9c618))
* Implement ST_ISCLOSED geography function ([#1789](https://github.com/googleapis/python-bigquery-dataframes/issues/1789)) ([36bc179](https://github.com/googleapis/python-bigquery-dataframes/commit/36bc179ee7ef9b0b6799f98f8fac3f64d91412af))
* Implement ST_LENGTH geography function ([#1791](https://github.com/googleapis/python-bigquery-dataframes/issues/1791)) ([c5b7fda](https://github.com/googleapis/python-bigquery-dataframes/commit/c5b7fdae74a22e581f7705bc0cf5390e928f4425))
* Support isin with bigframes.pandas.Index arg ([#1779](https://github.com/googleapis/python-bigquery-dataframes/issues/1779)) ([e480d29](https://github.com/googleapis/python-bigquery-dataframes/commit/e480d29f03636fa9824404ef90c510701e510195))


### Bug Fixes

* Address `read_csv` with both `index_col` and `use_cols` behavior inconsistency with pandas ([#1785](https://github.com/googleapis/python-bigquery-dataframes/issues/1785)) ([ba7c313](https://github.com/googleapis/python-bigquery-dataframes/commit/ba7c313c8d308e3ff3f736b60978cb7a51715209))
* Allow KMeans model init parameter as k-means++ alias ([#1790](https://github.com/googleapis/python-bigquery-dataframes/issues/1790)) ([0b59cf1](https://github.com/googleapis/python-bigquery-dataframes/commit/0b59cf1008613770fa1433c6da395e755c86fe22))
* Replace function now can handle pd.NA value. ([#1786](https://github.com/googleapis/python-bigquery-dataframes/issues/1786)) ([7269512](https://github.com/googleapis/python-bigquery-dataframes/commit/7269512a28eb42029447d5380c764353278a74e1))


### Documentation

* Adjust strip method examples to match latest pandas ([#1797](https://github.com/googleapis/python-bigquery-dataframes/issues/1797)) ([817b0c0](https://github.com/googleapis/python-bigquery-dataframes/commit/817b0c0c5dc481598fbfdbe40fd925fb38f3a066))
* Fix docstrings to improve html rendering of code examples ([#1788](https://github.com/googleapis/python-bigquery-dataframes/issues/1788)) ([38d9b73](https://github.com/googleapis/python-bigquery-dataframes/commit/38d9b7376697f8e19124e5d1f5fccda82d920b92))

## [2.5.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.4.0...v2.5.0) (2025-05-30)


### ⚠ BREAKING CHANGES

* the updated `ai.map()` parameter list is not backward-compatible

### Features

* Add `bpd.options.bigquery.requests_transport_adapters` option ([#1755](https://github.com/googleapis/python-bigquery-dataframes/issues/1755)) ([bb45db8](https://github.com/googleapis/python-bigquery-dataframes/commit/bb45db8afdffa1417f11c050d40d4ec6d15b8654))
* Add bbq.json_query and warn bbq.json_extract deprecated ([#1756](https://github.com/googleapis/python-bigquery-dataframes/issues/1756)) ([ec81dd2](https://github.com/googleapis/python-bigquery-dataframes/commit/ec81dd2228697d5bf193d86396cf7f3212e0289d))
* Add bpd.options.reset() method ([#1743](https://github.com/googleapis/python-bigquery-dataframes/issues/1743)) ([36c359d](https://github.com/googleapis/python-bigquery-dataframes/commit/36c359d2521089e186a412d353daf9de6cfbc8f4))
* Add DataFrame.round method ([#1742](https://github.com/googleapis/python-bigquery-dataframes/issues/1742)) ([3ea6043](https://github.com/googleapis/python-bigquery-dataframes/commit/3ea6043be7025fa7a11cca27b02f5505bbc9b129))
* Add deferred data uploading ([#1720](https://github.com/googleapis/python-bigquery-dataframes/issues/1720)) ([1f6442e](https://github.com/googleapis/python-bigquery-dataframes/commit/1f6442e576c35ec784ccf9cab3d081d46e45a5ce))
* Add deprecation warning to Gemini-1.5-X, text-embedding-004, and remove remove legacy models in notebooks and docs ([#1723](https://github.com/googleapis/python-bigquery-dataframes/issues/1723)) ([80aad9a](https://github.com/googleapis/python-bigquery-dataframes/commit/80aad9af794c2e06d1608c879f459a836fd4448b))
* Add structured output for ai map, ai filter and ai join ([#1746](https://github.com/googleapis/python-bigquery-dataframes/issues/1746)) ([133ac6b](https://github.com/googleapis/python-bigquery-dataframes/commit/133ac6b0e1f1e7a12844a4b6fd5b26df59f7ef37))
* Add support for df.loc[list, column(s)] ([#1761](https://github.com/googleapis/python-bigquery-dataframes/issues/1761)) ([768a757](https://github.com/googleapis/python-bigquery-dataframes/commit/768a7570845c4eb88f495d7f3c0f3158accdc231))
* Include bq schema and query string in dry run results ([#1752](https://github.com/googleapis/python-bigquery-dataframes/issues/1752)) ([bb51147](https://github.com/googleapis/python-bigquery-dataframes/commit/bb511475b74cc253230725846098a9045be2e324))
* Support `inplace=True` in `rename` and `rename_axis` ([#1744](https://github.com/googleapis/python-bigquery-dataframes/issues/1744)) ([734cc65](https://github.com/googleapis/python-bigquery-dataframes/commit/734cc652e435dc5d97a23411735aa51b7824e381))
* Support `unique()`  for Index ([#1750](https://github.com/googleapis/python-bigquery-dataframes/issues/1750)) ([27fac78](https://github.com/googleapis/python-bigquery-dataframes/commit/27fac78cb5654e5655aec861062837a7d4f3f679))
* Support astype conversions to and from JSON dtypes ([#1716](https://github.com/googleapis/python-bigquery-dataframes/issues/1716)) ([8ef4de1](https://github.com/googleapis/python-bigquery-dataframes/commit/8ef4de10151717f88364a909b29fa7600e959ada))
* Support dict param for dataframe.agg() ([#1772](https://github.com/googleapis/python-bigquery-dataframes/issues/1772)) ([f9c29c8](https://github.com/googleapis/python-bigquery-dataframes/commit/f9c29c85053d8111a74ce382490daed36f8bb35b))
* Support dtype parameter in read_csv for bigquery engine ([#1749](https://github.com/googleapis/python-bigquery-dataframes/issues/1749)) ([50dca4c](https://github.com/googleapis/python-bigquery-dataframes/commit/50dca4c706d78673b03f90eccf776118247ba30b))
* Use read api for some peek ops ([#1731](https://github.com/googleapis/python-bigquery-dataframes/issues/1731)) ([108f4d2](https://github.com/googleapis/python-bigquery-dataframes/commit/108f4d259e1bcfbe6c7aa3c3c3f8f605cf7615ee))


### Bug Fixes

* Fix clip int series with float bounds ([#1739](https://github.com/googleapis/python-bigquery-dataframes/issues/1739)) ([d451aef](https://github.com/googleapis/python-bigquery-dataframes/commit/d451aefd2181aef250c3b48cceac09063081cab2))
* Fix error with self-merge operations ([#1774](https://github.com/googleapis/python-bigquery-dataframes/issues/1774)) ([e5fe143](https://github.com/googleapis/python-bigquery-dataframes/commit/e5fe14339b4a40ab4a25657ee0453e4108cf8bba))
* Fix the default value for na_value for numpy conversions ([#1766](https://github.com/googleapis/python-bigquery-dataframes/issues/1766)) ([0629cac](https://github.com/googleapis/python-bigquery-dataframes/commit/0629cac7f9a9370a72c1ae25e014eb478a4c8c08))
* Include location in Session-based temporary storage manager DDL queries ([#1780](https://github.com/googleapis/python-bigquery-dataframes/issues/1780)) ([acba032](https://github.com/googleapis/python-bigquery-dataframes/commit/acba0321cafeb49f3e560a364ebbf3d15fb8af88))
* Prevent creating unnecessary client objects in multithreaded environments ([#1757](https://github.com/googleapis/python-bigquery-dataframes/issues/1757)) ([1cf9f5e](https://github.com/googleapis/python-bigquery-dataframes/commit/1cf9f5e8dba733ee26d15fc5edc44c81e094e9a0))
* Reduce bigquery table modification via DML for to_gbq ([#1737](https://github.com/googleapis/python-bigquery-dataframes/issues/1737)) ([545cdca](https://github.com/googleapis/python-bigquery-dataframes/commit/545cdcac1361607678c2574f0f31eb43950073e5))
* Stop ignoring arguments to `MatrixFactorization.score(X, y)` ([#1726](https://github.com/googleapis/python-bigquery-dataframes/issues/1726)) ([55c07e9](https://github.com/googleapis/python-bigquery-dataframes/commit/55c07e9d4315949c37ffa3e03c8fedc6daf17faf))
* Support JSON and STRUCT for bbq.sql_scalar ([#1754](https://github.com/googleapis/python-bigquery-dataframes/issues/1754)) ([190390b](https://github.com/googleapis/python-bigquery-dataframes/commit/190390b804c2131c2eaa624d7f025febb7784b01))
* Support str.replace re.compile with flags ([#1736](https://github.com/googleapis/python-bigquery-dataframes/issues/1736)) ([f8d2cd2](https://github.com/googleapis/python-bigquery-dataframes/commit/f8d2cd24281415f4a8f9193b676f5483128cd173))


### Performance Improvements

* Faster local data comparison using idenitity ([#1738](https://github.com/googleapis/python-bigquery-dataframes/issues/1738)) ([2858b1e](https://github.com/googleapis/python-bigquery-dataframes/commit/2858b1efb4fe74097dcb17c086ee1dc18e53053c))
* Optimize repr for unordered gbq table ([#1778](https://github.com/googleapis/python-bigquery-dataframes/issues/1778)) ([2bc4fbc](https://github.com/googleapis/python-bigquery-dataframes/commit/2bc4fbc78eba4bb2ee335e0475700a7ca5bc84d7))
* Use JOB_CREATION_OPTIONAL when `allow_large_results=False` ([#1763](https://github.com/googleapis/python-bigquery-dataframes/issues/1763)) ([15f3f2a](https://github.com/googleapis/python-bigquery-dataframes/commit/15f3f2aa42cfe4a2233f62c5f8906e7f7658f9fa))


### Dependencies

* Avoid `gcsfs==2025.5.0` ([#1762](https://github.com/googleapis/python-bigquery-dataframes/issues/1762)) ([68d5e2c](https://github.com/googleapis/python-bigquery-dataframes/commit/68d5e2cbef3510cadc7e9dd199117c1e3b02d19f))


### Documentation

* Add llm output_schema notebook ([#1732](https://github.com/googleapis/python-bigquery-dataframes/issues/1732)) ([b2261cc](https://github.com/googleapis/python-bigquery-dataframes/commit/b2261cc07cd58b51d212f9bf495c5022e587f816))
* Add MatrixFactorization to the table of contents ([#1725](https://github.com/googleapis/python-bigquery-dataframes/issues/1725)) ([611e43b](https://github.com/googleapis/python-bigquery-dataframes/commit/611e43b156483848a5470f889fb7b2b473ecff4d))
* Fix typo for "population" in the `GeminiTextGenerator.predict(..., output_schema={...})` sample notebook ([#1748](https://github.com/googleapis/python-bigquery-dataframes/issues/1748)) ([bd07e05](https://github.com/googleapis/python-bigquery-dataframes/commit/bd07e05d26820313c052eaf41c267a1ab20b4fc6))
* Integrations notebook extracts token from `bqclient._http.credentials` instead of `bqclient._credentials` ([#1784](https://github.com/googleapis/python-bigquery-dataframes/issues/1784)) ([6e63eca](https://github.com/googleapis/python-bigquery-dataframes/commit/6e63eca29f20d83435878273604816ce7595c396))
* Updated multimodal notebook instructions ([#1745](https://github.com/googleapis/python-bigquery-dataframes/issues/1745)) ([1df8ca6](https://github.com/googleapis/python-bigquery-dataframes/commit/1df8ca6312ee428d55c2091a00c73b13d9a6b193))
* Use partial ordering mode in the quickstart sample ([#1734](https://github.com/googleapis/python-bigquery-dataframes/issues/1734)) ([476b7dd](https://github.com/googleapis/python-bigquery-dataframes/commit/476b7dd7c2639cb6804272d06aa5c1db666819da))

## [2.4.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.3.0...v2.4.0) (2025-05-12)


### Features

* Add "dayofyear" property for `dt` accessors ([#1692](https://github.com/googleapis/python-bigquery-dataframes/issues/1692)) ([9d4a59d](https://github.com/googleapis/python-bigquery-dataframes/commit/9d4a59ddf22793d4e0587ea2f8648fae937875f3))
* Add `.dt.days`, `.dt.seconds`, `dt.microseconds`, and `dt.total_seconds()` for timedelta series. ([#1713](https://github.com/googleapis/python-bigquery-dataframes/issues/1713)) ([2b3a45f](https://github.com/googleapis/python-bigquery-dataframes/commit/2b3a45f8c1fd299ee97cf1c343df7c80175b4287))
* Add `DatetimeIndex` class ([#1719](https://github.com/googleapis/python-bigquery-dataframes/issues/1719)) ([c3c830c](https://github.com/googleapis/python-bigquery-dataframes/commit/c3c830cf20397830d531a89edf5302aede5d48a0))
* Add `isocalendar()` for dt accessor" ([#1717](https://github.com/googleapis/python-bigquery-dataframes/issues/1717)) ([0479763](https://github.com/googleapis/python-bigquery-dataframes/commit/047976315dcbaed86e50d47f545b76c3a513dafb))
* Add bigframes.bigquery.json_value ([#1697](https://github.com/googleapis/python-bigquery-dataframes/issues/1697)) ([46a9c53](https://github.com/googleapis/python-bigquery-dataframes/commit/46a9c53256be2a293f96122ba6b330564383bcd5))
* Add blob.exif function support ([#1703](https://github.com/googleapis/python-bigquery-dataframes/issues/1703)) ([3f79528](https://github.com/googleapis/python-bigquery-dataframes/commit/3f79528781abe9bfc122f6f6e26bfa08b029265a))
* Add inplace arg support to sort methods ([#1710](https://github.com/googleapis/python-bigquery-dataframes/issues/1710)) ([d1ccb52](https://github.com/googleapis/python-bigquery-dataframes/commit/d1ccb524ea26deac1cf9e481e9d55f9ae166247b))
* Improve error message in `Series.apply` for direct udfs ([#1673](https://github.com/googleapis/python-bigquery-dataframes/issues/1673)) ([1a658b2](https://github.com/googleapis/python-bigquery-dataframes/commit/1a658b2aa43c4a7a7f2007a509b0e1401f925dab))
* Publish bigframes blob(Multimodal) to preview ([#1693](https://github.com/googleapis/python-bigquery-dataframes/issues/1693)) ([e4c85ba](https://github.com/googleapis/python-bigquery-dataframes/commit/e4c85ba4813469d39edd7352201aefc26642d14c))
* Support () operator between timedeltas ([#1702](https://github.com/googleapis/python-bigquery-dataframes/issues/1702)) ([edaac89](https://github.com/googleapis/python-bigquery-dataframes/commit/edaac89c03db1ffc93b56275c765d8a964f7d02d))
* Support forecast_limit_lower_bound and forecast_limit_upper_bound in ARIMA_PLUS (and ARIMA_PLUS_XREG) models ([#1305](https://github.com/googleapis/python-bigquery-dataframes/issues/1305)) ([b16740e](https://github.com/googleapis/python-bigquery-dataframes/commit/b16740ef4ad7b1fbf731595238cf087c93c93066))
* Support to_strip parameter for str.strip, str.lstrip and str.rstrip ([#1705](https://github.com/googleapis/python-bigquery-dataframes/issues/1705)) ([a84ee75](https://github.com/googleapis/python-bigquery-dataframes/commit/a84ee75ddd4d9dae1463e505549d74eb4f819338))


### Bug Fixes

* Fix dayofyear doc test ([#1701](https://github.com/googleapis/python-bigquery-dataframes/issues/1701)) ([9b777a0](https://github.com/googleapis/python-bigquery-dataframes/commit/9b777a019aa31a115a22289f21c7cd9df07aa8b9))
* Fix issues with chunked arrow data ([#1700](https://github.com/googleapis/python-bigquery-dataframes/issues/1700)) ([e3289b7](https://github.com/googleapis/python-bigquery-dataframes/commit/e3289b7a64ee1400c6cb78e75cff4759d8da8b7a))
* Rename columns with protected names such as `_TABLE_SUFFIX` in `to_gbq()` ([#1691](https://github.com/googleapis/python-bigquery-dataframes/issues/1691)) ([8ec6079](https://github.com/googleapis/python-bigquery-dataframes/commit/8ec607986fd38f357746fbaeabef2ce7ab3e501f))


### Performance Improvements

* Defer query in `read_gbq` with wildcard tables ([#1661](https://github.com/googleapis/python-bigquery-dataframes/issues/1661)) ([5c125c9](https://github.com/googleapis/python-bigquery-dataframes/commit/5c125c99d4632c617425c2ef5c399d17878c0043))
* Rechunk result pages client side ([#1680](https://github.com/googleapis/python-bigquery-dataframes/issues/1680)) ([67d8760](https://github.com/googleapis/python-bigquery-dataframes/commit/67d876076027b6123e49d1d8ddee4e45eaa28f5d))


### Dependencies

* Move bigtable and pubsub to extras ([#1696](https://github.com/googleapis/python-bigquery-dataframes/issues/1696)) ([597d817](https://github.com/googleapis/python-bigquery-dataframes/commit/597d8178048b203cea4777f29b1ce95de7b0670e))


### Documentation

* Add snippets for Matrix Factorization tutorials ([#1630](https://github.com/googleapis/python-bigquery-dataframes/issues/1630)) ([24b37ae](https://github.com/googleapis/python-bigquery-dataframes/commit/24b37aece60460aabecce306397eb1bf6686f8a7))
* Deprecate `bpd.options.bigquery.allow_large_results` in favor of `bpd.options.compute.allow_large_results` ([#1597](https://github.com/googleapis/python-bigquery-dataframes/issues/1597)) ([18780b4](https://github.com/googleapis/python-bigquery-dataframes/commit/18780b48a17dba2b3b3542500f027ae9527f6bee))
* Include import statement in the bigframes code snippet ([#1699](https://github.com/googleapis/python-bigquery-dataframes/issues/1699)) ([08d70b6](https://github.com/googleapis/python-bigquery-dataframes/commit/08d70b6ad3ab3ac7b9a57d93da00168a8de7df9a))
* Include the clean-up step in the udf code snippet ([#1698](https://github.com/googleapis/python-bigquery-dataframes/issues/1698)) ([48992e2](https://github.com/googleapis/python-bigquery-dataframes/commit/48992e26d460832704401bd2a3eedb800c5061cc))
* Move multimodal notebook out of experimental folder ([#1712](https://github.com/googleapis/python-bigquery-dataframes/issues/1712)) ([68b6532](https://github.com/googleapis/python-bigquery-dataframes/commit/68b6532a780d6349a4b65994b696c8026457eb94))
* Update blob_display option in snippets ([#1714](https://github.com/googleapis/python-bigquery-dataframes/issues/1714)) ([8b30143](https://github.com/googleapis/python-bigquery-dataframes/commit/8b30143e3320a730df168b5a72e6d18e631135ee))

## [2.3.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.2.0...v2.3.0) (2025-05-06)


### Features

* Add dry_run parameter to `read_gbq()`, `read_gbq_table()` and `read_gbq_query()` ([#1674](https://github.com/googleapis/python-bigquery-dataframes/issues/1674)) ([4c5dee5](https://github.com/googleapis/python-bigquery-dataframes/commit/4c5dee5e6f4b30deb01e258670aa21dbf3ac9aa5))


### Bug Fixes

* Guarantee guid thread safety across threads ([#1684](https://github.com/googleapis/python-bigquery-dataframes/issues/1684)) ([cb0267d](https://github.com/googleapis/python-bigquery-dataframes/commit/cb0267deea227ea85f20d6dbef8c29cf03526d7a))
* Support large lists of lists in bpd.Series() constructor ([#1662](https://github.com/googleapis/python-bigquery-dataframes/issues/1662)) ([0f4024c](https://github.com/googleapis/python-bigquery-dataframes/commit/0f4024c84508c17657a9104ef1f8718094827ada))
* Use value equality to check types for unix epoch functions and timestamp diff ([#1690](https://github.com/googleapis/python-bigquery-dataframes/issues/1690)) ([81e8fb8](https://github.com/googleapis/python-bigquery-dataframes/commit/81e8fb8627f1d35423dbbdcc99d02ab0ad362d11))


### Performance Improvements

* `to_datetime()` now avoids caching inputs unless data is inspected to infer format ([#1667](https://github.com/googleapis/python-bigquery-dataframes/issues/1667)) ([dd08857](https://github.com/googleapis/python-bigquery-dataframes/commit/dd08857f65140cbe5c524050d2d538949897c3cc))


### Documentation

* Add a visualization notebook to BigFrame samples ([#1675](https://github.com/googleapis/python-bigquery-dataframes/issues/1675)) ([ee062bf](https://github.com/googleapis/python-bigquery-dataframes/commit/ee062bfc29c27949205ca21d6c1dcd6125300e5e))
* Fix spacing of k-means code snippet ([#1687](https://github.com/googleapis/python-bigquery-dataframes/issues/1687)) ([99f45dd](https://github.com/googleapis/python-bigquery-dataframes/commit/99f45dd14bd9632d209389a5fef009f18c57adbf))
* Update snippet for `Create a k-means` model tutorial ([#1664](https://github.com/googleapis/python-bigquery-dataframes/issues/1664)) ([761c364](https://github.com/googleapis/python-bigquery-dataframes/commit/761c364f4df045b9e9d8d3d5fee91d9a87b772db))

## [2.2.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.1.0...v2.2.0) (2025-04-30)


### Features

* Add gemini-2.0-flash-001 and gemini-2.0-flash-lite-001 to fine tune score endponts and multimodal endpoints ([#1650](https://github.com/googleapis/python-bigquery-dataframes/issues/1650)) ([4fb54df](https://github.com/googleapis/python-bigquery-dataframes/commit/4fb54dfe448604a90fc1818cf18b1e77e1e7227b))
* Add GeminiTextGenerator.predict structured output ([#1653](https://github.com/googleapis/python-bigquery-dataframes/issues/1653)) ([6199023](https://github.com/googleapis/python-bigquery-dataframes/commit/6199023a6a71e72e926f5879e74a15215bc6e4a0))
* DataFrames.__getitem__ support for slice input ([#1668](https://github.com/googleapis/python-bigquery-dataframes/issues/1668)) ([563f0cb](https://github.com/googleapis/python-bigquery-dataframes/commit/563f0cbdf4a18c3cd1bd2a4b52de823165638911))
* Print right origin of `PreviewWarning` for the `bpd.udf` ([#1629](https://github.com/googleapis/python-bigquery-dataframes/issues/1629)) ([48d10d1](https://github.com/googleapis/python-bigquery-dataframes/commit/48d10d1f0150a29dd3b91f505f8d3874e0b88c42))
* Session.bytes_processed_sum will be updated when allow_large_re… ([#1669](https://github.com/googleapis/python-bigquery-dataframes/issues/1669)) ([ae312db](https://github.com/googleapis/python-bigquery-dataframes/commit/ae312dbed25da6da5e2817d5c9838654c2a1ad1c))
* Short circuit query for local scan ([#1618](https://github.com/googleapis/python-bigquery-dataframes/issues/1618)) ([e84f232](https://github.com/googleapis/python-bigquery-dataframes/commit/e84f232b0fc5e2167a7cddb355cf0c8837ae5422))
* Support names parameter in read_csv for bigquery engine ([#1659](https://github.com/googleapis/python-bigquery-dataframes/issues/1659)) ([3388191](https://github.com/googleapis/python-bigquery-dataframes/commit/33881914ab5b8d0e701eabd9c731aed1deab3d49))
* Support passing list of values to bigframes.core.sql.simple_literal ([#1641](https://github.com/googleapis/python-bigquery-dataframes/issues/1641)) ([102d363](https://github.com/googleapis/python-bigquery-dataframes/commit/102d363aa7e3245ff262c817bc756ea0eaee57e7))
* Support write api as loading option ([#1617](https://github.com/googleapis/python-bigquery-dataframes/issues/1617)) ([c46ad06](https://github.com/googleapis/python-bigquery-dataframes/commit/c46ad0647785a9207359eba0fb5b6f7a16610f2a))


### Bug Fixes

* DataFrame accessors is not pupulated ([#1639](https://github.com/googleapis/python-bigquery-dataframes/issues/1639)) ([28afa2c](https://github.com/googleapis/python-bigquery-dataframes/commit/28afa2c73c0517f9365fab05193706631b656551))
* Prefer remote schema instead of throwing on materialize conflicts ([#1644](https://github.com/googleapis/python-bigquery-dataframes/issues/1644)) ([53fc25b](https://github.com/googleapis/python-bigquery-dataframes/commit/53fc25bfc86e166b91e5001506051b1cac34c996))
* Remove itertools.pairwise usage ([#1638](https://github.com/googleapis/python-bigquery-dataframes/issues/1638)) ([9662745](https://github.com/googleapis/python-bigquery-dataframes/commit/9662745265c8c6e42f372629bd2c7806542cee1a))
* Resolve issue where pre-release versions of google-auth are installed ([#1491](https://github.com/googleapis/python-bigquery-dataframes/issues/1491)) ([ebb7a5e](https://github.com/googleapis/python-bigquery-dataframes/commit/ebb7a5e2b24fa57d6fe6a76d9b857ad44c67d194))
* Resolve some of the typo errors ([#1655](https://github.com/googleapis/python-bigquery-dataframes/issues/1655)) ([cd7fbde](https://github.com/googleapis/python-bigquery-dataframes/commit/cd7fbde026522f53a23a4bb6585ad8629769fad1))


### Performance Improvements

* Fold row count ops when known ([#1656](https://github.com/googleapis/python-bigquery-dataframes/issues/1656)) ([c958dbe](https://github.com/googleapis/python-bigquery-dataframes/commit/c958dbea32b77cec9fddfc09e3b40d1da220a42c))
* Use flyweight for node fields ([#1654](https://github.com/googleapis/python-bigquery-dataframes/issues/1654)) ([8482bfc](https://github.com/googleapis/python-bigquery-dataframes/commit/8482bfc1d4caa91a35c4fbf0be420301d05ad544))


### Dependencies

* Support shapely 1.8.5+ again ([#1651](https://github.com/googleapis/python-bigquery-dataframes/issues/1651)) ([ae83e61](https://github.com/googleapis/python-bigquery-dataframes/commit/ae83e61c49ade64d6f727e9f364bd2f1aeec6e19))


### Documentation

* Add JSON data types notebook ([#1647](https://github.com/googleapis/python-bigquery-dataframes/issues/1647)) ([9128c4a](https://github.com/googleapis/python-bigquery-dataframes/commit/9128c4a31dab487bc23f67c43380abd0beda5b1c))
* Add sample code snippets for `udf` ([#1649](https://github.com/googleapis/python-bigquery-dataframes/issues/1649)) ([53caa8d](https://github.com/googleapis/python-bigquery-dataframes/commit/53caa8d689e64436f5313095ee27479a06d8e8a8))
* Fix `bq_dataframes_template` notebook to work if partial ordering mode is enabled ([#1665](https://github.com/googleapis/python-bigquery-dataframes/issues/1665)) ([f442e7a](https://github.com/googleapis/python-bigquery-dataframes/commit/f442e7a07ff273ba3af74eeabafb62110b78f692))
* Note that `udf` is in preview and must be python 3.11 compatible ([#1629](https://github.com/googleapis/python-bigquery-dataframes/issues/1629)) ([48d10d1](https://github.com/googleapis/python-bigquery-dataframes/commit/48d10d1f0150a29dd3b91f505f8d3874e0b88c42))

## [2.1.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v2.0.0...v2.1.0) (2025-04-22)


### Features

* Add `bigframes.bigquery.st_distance` function ([#1637](https://github.com/googleapis/python-bigquery-dataframes/issues/1637)) ([bf1ae70](https://github.com/googleapis/python-bigquery-dataframes/commit/bf1ae7091a02ad28d222fa63d311ed5ef3800807))
* Enable local json string validations ([#1614](https://github.com/googleapis/python-bigquery-dataframes/issues/1614)) ([233347a](https://github.com/googleapis/python-bigquery-dataframes/commit/233347aca0ac55b2407e0f49430bf13536986e25))
* Enhance `read_csv` `index_col` parameter support ([#1631](https://github.com/googleapis/python-bigquery-dataframes/issues/1631)) ([f4e5b26](https://github.com/googleapis/python-bigquery-dataframes/commit/f4e5b26b7b7b00ef807987c4b9c5fded56ad883f))


### Bug Fixes

* Add retry for test_clean_up_via_context_manager ([#1627](https://github.com/googleapis/python-bigquery-dataframes/issues/1627)) ([58e7cb0](https://github.com/googleapis/python-bigquery-dataframes/commit/58e7cb025a86959164643cebb725c853dc2ebc34))
* Improve robustness of managed udf code extraction ([#1634](https://github.com/googleapis/python-bigquery-dataframes/issues/1634)) ([8cc56d5](https://github.com/googleapis/python-bigquery-dataframes/commit/8cc56d5118017beb2931519ddd1eb8e151852849))


### Documentation

* Add code samples in the `udf` API docstring ([#1632](https://github.com/googleapis/python-bigquery-dataframes/issues/1632)) ([f68b80c](https://github.com/googleapis/python-bigquery-dataframes/commit/f68b80cce2451a8c8d931a54e0cb69e02f34ce10))

## [2.0.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.42.0...v2.0.0) (2025-04-17)


### ⚠ BREAKING CHANGES

* make `dataset` and `name` params mandatory in `udf` ([#1619](https://github.com/googleapis/python-bigquery-dataframes/issues/1619))
* Locational endpoints support is not available in BigFrames 2.0.
* change default LLM model to gemini-2.0-flash-001, drop PaLM2TextGenerator and PaLM2TextEmbeddingGenerator  ([#1558](https://github.com/googleapis/python-bigquery-dataframes/issues/1558))
* change default ingress setting for `remote_function` to internal-only ([#1544](https://github.com/googleapis/python-bigquery-dataframes/issues/1544))
* make `remote_function` params keyword only ([#1537](https://github.com/googleapis/python-bigquery-dataframes/issues/1537))
* make `remote_function` default service account explicit ([#1537](https://github.com/googleapis/python-bigquery-dataframes/issues/1537))
* set `allow_large_results=False` by default ([#1541](https://github.com/googleapis/python-bigquery-dataframes/issues/1541))

### Features

* Add `on`  parameter in `dataframe.rolling()` and `dataframe.groupby.rolling()` ([#1556](https://github.com/googleapis/python-bigquery-dataframes/issues/1556)) ([45c9d9f](https://github.com/googleapis/python-bigquery-dataframes/commit/45c9d9fd1c5c13a8692435aa22861820fc11e347))
* Add component to manage temporary tables ([#1559](https://github.com/googleapis/python-bigquery-dataframes/issues/1559)) ([0a4e245](https://github.com/googleapis/python-bigquery-dataframes/commit/0a4e245670e678f4ead0aec8f8b534e7fe97d112))
* Add Series.to_pandas_batches() method ([#1592](https://github.com/googleapis/python-bigquery-dataframes/issues/1592)) ([09ce979](https://github.com/googleapis/python-bigquery-dataframes/commit/09ce97999cfc1ded72906b1c7307da5950978ae6))
* Add support for creating a Matrix Factorization model ([#1330](https://github.com/googleapis/python-bigquery-dataframes/issues/1330)) ([b5297f9](https://github.com/googleapis/python-bigquery-dataframes/commit/b5297f909b08928b97d887764d6e5142c763a5a3))
* Allow `input_types`, `output_type`, and `dataset` to be used positionally in `remote_function` ([#1560](https://github.com/googleapis/python-bigquery-dataframes/issues/1560)) ([bcac8c6](https://github.com/googleapis/python-bigquery-dataframes/commit/bcac8c6ed0b40902d0ccaef3f907e6acbe6a52ed))
* Allow pandas.cut 'labels' parameter to accept a list of string ([#1549](https://github.com/googleapis/python-bigquery-dataframes/issues/1549)) ([af842b1](https://github.com/googleapis/python-bigquery-dataframes/commit/af842b174de7eef4908b397d6a745caf8eda7b3d))
* Change default ingress setting for `remote_function` to internal-only ([#1544](https://github.com/googleapis/python-bigquery-dataframes/issues/1544)) ([c848a80](https://github.com/googleapis/python-bigquery-dataframes/commit/c848a80766ff68ea92c05a5dc5c26508e6755381))
* Detect duplicate column/index names in read_gbq before send query. ([#1615](https://github.com/googleapis/python-bigquery-dataframes/issues/1615)) ([40d6960](https://github.com/googleapis/python-bigquery-dataframes/commit/40d696088114fb08e68df74be261144350b785c8))
* Drop support for locational endpoints ([#1542](https://github.com/googleapis/python-bigquery-dataframes/issues/1542)) ([4bf2e43](https://github.com/googleapis/python-bigquery-dataframes/commit/4bf2e43ef4498b11f32086231fc4cc749fde966a))
* Enable time range rolling for DataFrame, DataFrameGroupBy and SeriesGroupBy ([#1605](https://github.com/googleapis/python-bigquery-dataframes/issues/1605)) ([b4b7073](https://github.com/googleapis/python-bigquery-dataframes/commit/b4b7073da8348b6597bd3d90d1a758cd29586533))
* Improve local data validation ([#1598](https://github.com/googleapis/python-bigquery-dataframes/issues/1598)) ([815e471](https://github.com/googleapis/python-bigquery-dataframes/commit/815e471b904d4bd708afc4bfbf1db945e76f75c9))
* Make `remote_function` default service account explicit ([#1537](https://github.com/googleapis/python-bigquery-dataframes/issues/1537)) ([9eb9089](https://github.com/googleapis/python-bigquery-dataframes/commit/9eb9089ce3f1dad39761ba8ebc2d6f76261bd243))
* Set `allow_large_results=False` by default ([#1541](https://github.com/googleapis/python-bigquery-dataframes/issues/1541)) ([e9fb712](https://github.com/googleapis/python-bigquery-dataframes/commit/e9fb7129a05e8ac7c938ffe30e86902950316f20))
* Support bigquery connection in managed function ([#1554](https://github.com/googleapis/python-bigquery-dataframes/issues/1554)) ([f6f697a](https://github.com/googleapis/python-bigquery-dataframes/commit/f6f697afc167e0fa7ea923c0aed85a9ef257d61f))
* Support bq connection path format ([#1550](https://github.com/googleapis/python-bigquery-dataframes/issues/1550)) ([e7eb918](https://github.com/googleapis/python-bigquery-dataframes/commit/e7eb918dd9df3569febe695f57c1a5909844fd3c))
* Support gemini-2.0-X models ([#1558](https://github.com/googleapis/python-bigquery-dataframes/issues/1558)) ([3104fab](https://github.com/googleapis/python-bigquery-dataframes/commit/3104fab019d20b0cbc06cd81d43b3f34fd1dd987))
* Support inlining small list, struct, json data ([#1589](https://github.com/googleapis/python-bigquery-dataframes/issues/1589)) ([2ce891f](https://github.com/googleapis/python-bigquery-dataframes/commit/2ce891fcd5bfd9f093fbcbb1ea35158d2bf9d8b9))
* Support time range rolling on Series. ([#1590](https://github.com/googleapis/python-bigquery-dataframes/issues/1590)) ([6e98a2c](https://github.com/googleapis/python-bigquery-dataframes/commit/6e98a2cf53dd130963a9c5ba07e21ce6c32b7c6d))
* Use session temp tables for all ephemeral storage ([#1569](https://github.com/googleapis/python-bigquery-dataframes/issues/1569)) ([9711b83](https://github.com/googleapis/python-bigquery-dataframes/commit/9711b830a7bdc6740f4ebeaaab6f37082ae5dfd9))
* Use validated local storage for data uploads ([#1612](https://github.com/googleapis/python-bigquery-dataframes/issues/1612)) ([aee4159](https://github.com/googleapis/python-bigquery-dataframes/commit/aee4159807401d7432bb8c0c41859ada3291599b))
* Warn the deprecated `max_download_size`, `random_state` and `sampling_method` parameters in `(DataFrame|Series).to_pandas()` ([#1573](https://github.com/googleapis/python-bigquery-dataframes/issues/1573)) ([b9623da](https://github.com/googleapis/python-bigquery-dataframes/commit/b9623daa847805abf420f0f11e173674fb147193))


### Bug Fixes

* `to_pandas_batches()` respects `page_size` and `max_results` again ([#1572](https://github.com/googleapis/python-bigquery-dataframes/issues/1572)) ([27c5905](https://github.com/googleapis/python-bigquery-dataframes/commit/27c59051549b83fdac954eaa3d257803c6f9133d))
* Ensure `page_size` works correctly in `to_pandas_batches` when `max_results` is not set ([#1588](https://github.com/googleapis/python-bigquery-dataframes/issues/1588)) ([570cff3](https://github.com/googleapis/python-bigquery-dataframes/commit/570cff3c2efe3a47535bb3c931a345856d256a19))
* Include role and service account in IAM exception ([#1564](https://github.com/googleapis/python-bigquery-dataframes/issues/1564)) ([8c50755](https://github.com/googleapis/python-bigquery-dataframes/commit/8c507556c5f61fab95c6389a8ad04d731df1df7b))
* Make `dataset` and `name` params mandatory in `udf` ([#1619](https://github.com/googleapis/python-bigquery-dataframes/issues/1619)) ([637e860](https://github.com/googleapis/python-bigquery-dataframes/commit/637e860d3cea0a36b1e58a45ec9b9ab0059fb3b1))
* Pandas.cut returns labels index for numeric breaks when labels=False ([#1548](https://github.com/googleapis/python-bigquery-dataframes/issues/1548)) ([b2375de](https://github.com/googleapis/python-bigquery-dataframes/commit/b2375decedbf1a793eedbbc9dc2efc2296f8cc6e))
* Prevent `KeyError` in `bpd.concat` with empty DF and struct/array types DF ([#1568](https://github.com/googleapis/python-bigquery-dataframes/issues/1568)) ([b4da1cf](https://github.com/googleapis/python-bigquery-dataframes/commit/b4da1cf3c0fb94a2bb21e6039896accab85742d4))
* Read_csv supports for tilde local paths and includes index for bigquery_stream write engine ([#1580](https://github.com/googleapis/python-bigquery-dataframes/issues/1580)) ([352e8e4](https://github.com/googleapis/python-bigquery-dataframes/commit/352e8e4b05cf19e970b47b017f958a1c6fc89bea))
* Use dictionaries to avoid problematic google.iam namespace ([#1611](https://github.com/googleapis/python-bigquery-dataframes/issues/1611)) ([b03e44f](https://github.com/googleapis/python-bigquery-dataframes/commit/b03e44f7fca429a6de41c42ec28504b688cd84f0))


### Performance Improvements

* Directly read gbq table for simple plans ([#1607](https://github.com/googleapis/python-bigquery-dataframes/issues/1607)) ([6ad38e8](https://github.com/googleapis/python-bigquery-dataframes/commit/6ad38e8287354f62b0c5cad1f3d5b897256860ca))


### Dependencies

* Remove jellyfish dependency ([#1604](https://github.com/googleapis/python-bigquery-dataframes/issues/1604)) ([1ac0e1e](https://github.com/googleapis/python-bigquery-dataframes/commit/1ac0e1e82c097717338a6816f27c01b67736f51c))
* Remove parsy dependency ([#1610](https://github.com/googleapis/python-bigquery-dataframes/issues/1610)) ([293f676](https://github.com/googleapis/python-bigquery-dataframes/commit/293f676e98446c417c12c345d5db875dd4c438df))
* Remove test dependency on pytest-mock package ([#1622](https://github.com/googleapis/python-bigquery-dataframes/issues/1622)) ([1ba72ea](https://github.com/googleapis/python-bigquery-dataframes/commit/1ba72ead256178afee6f1d3303b0556bec1c4a9b))
* Support a shapely versions 1.8.5+ ([#1621](https://github.com/googleapis/python-bigquery-dataframes/issues/1621)) ([e39ee3b](https://github.com/googleapis/python-bigquery-dataframes/commit/e39ee3bcf37f2a4f5e6ce981d248c24c6f5d770b))


### Documentation

* Add details for `bigquery_connection` in `[@bpd](https://github.com/bpd).udf` docstring ([#1609](https://github.com/googleapis/python-bigquery-dataframes/issues/1609)) ([ef63772](https://github.com/googleapis/python-bigquery-dataframes/commit/ef6377277bc9c354385c83ceba9e00094c0a6cc6))
* Add explain forecast snippet to multiple time series tutorial ([#1586](https://github.com/googleapis/python-bigquery-dataframes/issues/1586)) ([40c55a0](https://github.com/googleapis/python-bigquery-dataframes/commit/40c55a06a529ca49d203227ccf36c12427d0cd5b))
* Add message to remove default model for version 3.0 ([#1563](https://github.com/googleapis/python-bigquery-dataframes/issues/1563)) ([910be2b](https://github.com/googleapis/python-bigquery-dataframes/commit/910be2b5b2bfaf0e21cdc4fd775c1605a864c1aa))
* Add samples for ArimaPlus `time_series_id_col` feature ([#1577](https://github.com/googleapis/python-bigquery-dataframes/issues/1577)) ([1e4cd9c](https://github.com/googleapis/python-bigquery-dataframes/commit/1e4cd9cf69f98d4af6b2a70bd8189c619b19baaa))
* Add warning for bigframes 2.0 ([#1557](https://github.com/googleapis/python-bigquery-dataframes/issues/1557)) ([3f0eaa1](https://github.com/googleapis/python-bigquery-dataframes/commit/3f0eaa1c6b02d086270421f91dbb6aa2f117317d))
* Deprecate default model in `TextEmbedddingGenerator`, `GeminiTextGenerator`, and other `bigframes.ml.llm` classes ([#1570](https://github.com/googleapis/python-bigquery-dataframes/issues/1570)) ([89ab33e](https://github.com/googleapis/python-bigquery-dataframes/commit/89ab33e1179aef142415fd5c9073671903bf1d45))
* Include all licenses for vendored packages in the root LICENSE file ([#1626](https://github.com/googleapis/python-bigquery-dataframes/issues/1626)) ([8116ed0](https://github.com/googleapis/python-bigquery-dataframes/commit/8116ed0938634d301a153613f8a9cd8053ddf026))
* Remove gemini-1.5 deprecation warning for `GeminiTextGenerator` ([#1562](https://github.com/googleapis/python-bigquery-dataframes/issues/1562)) ([0cc6784](https://github.com/googleapis/python-bigquery-dataframes/commit/0cc678448fdec1eaa3acfbb563a018325a8c85bc))
* Use restructured text to allow publishing to PyPI ([#1565](https://github.com/googleapis/python-bigquery-dataframes/issues/1565)) ([d1e9ec2](https://github.com/googleapis/python-bigquery-dataframes/commit/d1e9ec2936d270ec4035014ea3ddd335a5747ade))


### Miscellaneous Chores

* Make `remote_function` params keyword only ([#1537](https://github.com/googleapis/python-bigquery-dataframes/issues/1537)) ([9eb9089](https://github.com/googleapis/python-bigquery-dataframes/commit/9eb9089ce3f1dad39761ba8ebc2d6f76261bd243))

## [1.42.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.41.0...v1.42.0) (2025-03-27)


### Features

* Add `closed` parameter in rolling() ([#1539](https://github.com/googleapis/python-bigquery-dataframes/issues/1539)) ([8bcc89b](https://github.com/googleapis/python-bigquery-dataframes/commit/8bcc89b30022f5ccf9ced80676a279c261c2f697))
* Add `GeoSeries.difference()` and `bigframes.bigquery.st_difference()` ([#1471](https://github.com/googleapis/python-bigquery-dataframes/issues/1471)) ([e9fe815](https://github.com/googleapis/python-bigquery-dataframes/commit/e9fe8154d83e2674a05d7b670e949368b175ec8b))
* Add `GeoSeries.intersection()` and `bigframes.bigquery.st_intersection()` ([#1529](https://github.com/googleapis/python-bigquery-dataframes/issues/1529)) ([8542bd4](https://github.com/googleapis/python-bigquery-dataframes/commit/8542bd469ff8775a9073f5a040b4117facfd8513))
* Add df.take and series.take ([#1509](https://github.com/googleapis/python-bigquery-dataframes/issues/1509)) ([7d00be6](https://github.com/googleapis/python-bigquery-dataframes/commit/7d00be67cf50fdf713c40912f207d14f0f65538f))
* Add Linear_Regression.global_explain() ([#1446](https://github.com/googleapis/python-bigquery-dataframes/issues/1446)) ([7e5b6a8](https://github.com/googleapis/python-bigquery-dataframes/commit/7e5b6a873d00162ffca3d254d3af276c5f06d866))
* Allow iloc to support lists of negative indices ([#1497](https://github.com/googleapis/python-bigquery-dataframes/issues/1497)) ([a9cf215](https://github.com/googleapis/python-bigquery-dataframes/commit/a9cf215fb1403fda4ab2b58252f5fedc33aba3e1))
* Support dry_run in `to_pandas()` ([#1436](https://github.com/googleapis/python-bigquery-dataframes/issues/1436)) ([75fc7e0](https://github.com/googleapis/python-bigquery-dataframes/commit/75fc7e0268dc5b10bdbc33dcf28db97dce62e41c))
* Support window partition by geo column ([#1512](https://github.com/googleapis/python-bigquery-dataframes/issues/1512)) ([bdcb1e7](https://github.com/googleapis/python-bigquery-dataframes/commit/bdcb1e7929dc2f24c642ddb052629da394f45876))
* Upgrade BQ managed `udf` to preview ([#1536](https://github.com/googleapis/python-bigquery-dataframes/issues/1536)) ([4a7fe4d](https://github.com/googleapis/python-bigquery-dataframes/commit/4a7fe4d75724e734634d41f18b4957e0877becc3))


### Bug Fixes

* Add deprecation warning to TextEmbeddingGenerator model, espeically gemini-1.0-X and gemini-1.5-X ([#1534](https://github.com/googleapis/python-bigquery-dataframes/issues/1534)) ([c93e720](https://github.com/googleapis/python-bigquery-dataframes/commit/c93e7204758435b0306699d3a1332aaf522f576b))
* Change the default value for pdf extract/chunk ([#1517](https://github.com/googleapis/python-bigquery-dataframes/issues/1517)) ([a70a607](https://github.com/googleapis/python-bigquery-dataframes/commit/a70a607512797463f70ed529f078fcb2d40c85a1))
* Local data always has sequential index ([#1514](https://github.com/googleapis/python-bigquery-dataframes/issues/1514)) ([014bd33](https://github.com/googleapis/python-bigquery-dataframes/commit/014bd33317966e15d05617c978e847de8c953453))
* Read_pandas inline returns None when exceeds limit ([#1525](https://github.com/googleapis/python-bigquery-dataframes/issues/1525)) ([578081e](https://github.com/googleapis/python-bigquery-dataframes/commit/578081e978f2cca21ddae8b3ee371972ba723777))
* Temporary fix for StreamingDataFrame not working backend bug ([#1533](https://github.com/googleapis/python-bigquery-dataframes/issues/1533)) ([6ab4ffd](https://github.com/googleapis/python-bigquery-dataframes/commit/6ab4ffd33d4900da833020ffa7ffc03a93a2b4b2))
* Tolerate BQ connection service account propagation delay ([#1505](https://github.com/googleapis/python-bigquery-dataframes/issues/1505)) ([6681f1f](https://github.com/googleapis/python-bigquery-dataframes/commit/6681f1f9e30ed2325b85668de8a0b1d3d0e2858b))


### Performance Improvements

* Update shape to use quer_and_wait ([#1519](https://github.com/googleapis/python-bigquery-dataframes/issues/1519)) ([34ab9b8](https://github.com/googleapis/python-bigquery-dataframes/commit/34ab9b8abd2c632c806afe69f00d9e7dddb6a8b5))


### Documentation

* Update `GeoSeries.difference()` and `bigframes.bigquery.st_difference()` docs ([#1526](https://github.com/googleapis/python-bigquery-dataframes/issues/1526)) ([d553fa2](https://github.com/googleapis/python-bigquery-dataframes/commit/d553fa25fe85b3590269ed2ce08d5dff3bd22dfc))

## [1.41.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.40.0...v1.41.0) (2025-03-19)


### Features

* Add support for the 'right' parameter in 'pandas.cut' ([#1496](https://github.com/googleapis/python-bigquery-dataframes/issues/1496)) ([8aff128](https://github.com/googleapis/python-bigquery-dataframes/commit/8aff1285b26754118cc8ee906c4ac3076456a791))
* Support BQ managed functions through `read_gbq_function` ([#1476](https://github.com/googleapis/python-bigquery-dataframes/issues/1476)) ([802183d](https://github.com/googleapis/python-bigquery-dataframes/commit/802183dc000ad2ce5559d14181dd3f7d036b3fed))
* Warn when the BigFrames version is more than a year old ([#1455](https://github.com/googleapis/python-bigquery-dataframes/issues/1455)) ([00e0750](https://github.com/googleapis/python-bigquery-dataframes/commit/00e07508cfb0d8798e079b86a14834b3b593aa54))


### Bug Fixes

* Fix pandas.cut errors with empty bins ([#1499](https://github.com/googleapis/python-bigquery-dataframes/issues/1499)) ([434fb5d](https://github.com/googleapis/python-bigquery-dataframes/commit/434fb5dd60d11f09b808ea656394790aba43fdde))
* Fix read_gbq with ORDER BY query and index_col set ([#963](https://github.com/googleapis/python-bigquery-dataframes/issues/963)) ([de46d2f](https://github.com/googleapis/python-bigquery-dataframes/commit/de46d2fdf7a1a30b2be07dbaa1cb127f10f5fe30))


### Performance Improvements

* Eliminate count queries in llm retry ([#1489](https://github.com/googleapis/python-bigquery-dataframes/issues/1489)) ([1c934c2](https://github.com/googleapis/python-bigquery-dataframes/commit/1c934c2fe2374c9abaaa79696f5e5f349248f3b7))


### Documentation

* Add a sample notebook for vector search ([#1500](https://github.com/googleapis/python-bigquery-dataframes/issues/1500)) ([f3bf139](https://github.com/googleapis/python-bigquery-dataframes/commit/f3bf139d33ed00ca3081e4e0315f409fdb2ad84d))

## [1.40.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.39.0...v1.40.0) (2025-03-11)


### ⚠ BREAKING CHANGES

* reading JSON data as a custom arrow extension type ([#1458](https://github.com/googleapis/python-bigquery-dataframes/issues/1458))

### Features

* Reading JSON data as a custom arrow extension type ([#1458](https://github.com/googleapis/python-bigquery-dataframes/issues/1458)) ([e720f41](https://github.com/googleapis/python-bigquery-dataframes/commit/e720f41ef643ac14ae94fa98de5ef4a3fd6dde93))
* Support list output for managed function ([#1457](https://github.com/googleapis/python-bigquery-dataframes/issues/1457)) ([461e9e0](https://github.com/googleapis/python-bigquery-dataframes/commit/461e9e017d513376fc623a5ee47f8b9dd002b452))


### Bug Fixes

* Fix list-like indexers in partial ordering mode ([#1456](https://github.com/googleapis/python-bigquery-dataframes/issues/1456)) ([fe72ada](https://github.com/googleapis/python-bigquery-dataframes/commit/fe72ada9cebb32947560c97567d7937c8b618f0d))
* Fix the merge issue between 1424 and 1373 ([#1461](https://github.com/googleapis/python-bigquery-dataframes/issues/1461)) ([7b6e361](https://github.com/googleapis/python-bigquery-dataframes/commit/7b6e3615f8d4531beb4b59ca1223927112e713da))
* Use `==` instead of `is` for timedelta type equality checks ([#1480](https://github.com/googleapis/python-bigquery-dataframes/issues/1480)) ([0db248b](https://github.com/googleapis/python-bigquery-dataframes/commit/0db248b5597a3966ac3dee1cca849509e48f4648))


### Performance Improvements

* Compilation no longer bounded by recursion ([#1464](https://github.com/googleapis/python-bigquery-dataframes/issues/1464)) ([27ab028](https://github.com/googleapis/python-bigquery-dataframes/commit/27ab028cdc45296923b12446c77b344af4208a3a))

## [1.39.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.38.0...v1.39.0) (2025-03-05)


### Features

* (Preview) Support `diff()` for date series ([#1423](https://github.com/googleapis/python-bigquery-dataframes/issues/1423)) ([521e987](https://github.com/googleapis/python-bigquery-dataframes/commit/521e9874f1c7dcd80e10bfd86f1b467b0f6d6d6e))
* (Preview) Support aggregations over timedeltas ([#1418](https://github.com/googleapis/python-bigquery-dataframes/issues/1418)) ([1251ded](https://github.com/googleapis/python-bigquery-dataframes/commit/1251dedac8faf383c931185a057a8bb26afb4b8f))
* (Preview) Support arithmetics between dates and timedeltas ([#1413](https://github.com/googleapis/python-bigquery-dataframes/issues/1413)) ([962b152](https://github.com/googleapis/python-bigquery-dataframes/commit/962b152ce5a368132d1ac14f6d8348b7ba285694))
* (Preview) Support automatic load of timedelta from BQ tables. ([#1429](https://github.com/googleapis/python-bigquery-dataframes/issues/1429)) ([b2917bb](https://github.com/googleapis/python-bigquery-dataframes/commit/b2917bb57212ac399c20356755c878d179454bfe))
* Add `allow_large_results` option to many I/O methods. Set to `False` to reduce latency ([#1428](https://github.com/googleapis/python-bigquery-dataframes/issues/1428)) ([dd2f488](https://github.com/googleapis/python-bigquery-dataframes/commit/dd2f48893eced458afecc93dc17b7e22735c39b9))
* Add `GeoSeries.boundary()` ([#1435](https://github.com/googleapis/python-bigquery-dataframes/issues/1435)) ([32cddfe](https://github.com/googleapis/python-bigquery-dataframes/commit/32cddfecd25ff4208473574df09a8010f8be0de9))
* Add allow_large_results to peek ([#1448](https://github.com/googleapis/python-bigquery-dataframes/issues/1448)) ([67487b9](https://github.com/googleapis/python-bigquery-dataframes/commit/67487b9a3bbe07f1b76e0332fab693b4c4022529))
* Add groupby.rank() ([#1433](https://github.com/googleapis/python-bigquery-dataframes/issues/1433)) ([3a633d5](https://github.com/googleapis/python-bigquery-dataframes/commit/3a633d5cc9c3e6a2bd8311c8834b406db5cb8699))
* Iloc multiple columns selection. ([#1437](https://github.com/googleapis/python-bigquery-dataframes/issues/1437)) ([ddfd02a](https://github.com/googleapis/python-bigquery-dataframes/commit/ddfd02a83040847f6d4642420d3bd32a4a855001))
* Support interface for BigQuery managed functions ([#1373](https://github.com/googleapis/python-bigquery-dataframes/issues/1373)) ([2bbf53f](https://github.com/googleapis/python-bigquery-dataframes/commit/2bbf53f0d92dc669e1d775fafc54199f582d9059))
* Warn if default ingress_settings is used in remote_functions ([#1419](https://github.com/googleapis/python-bigquery-dataframes/issues/1419)) ([dfd891a](https://github.com/googleapis/python-bigquery-dataframes/commit/dfd891a0102314e7542d0b0057442dcde3d9a4a1))


### Bug Fixes

* Do not compare schema description during schema validation ([#1452](https://github.com/googleapis/python-bigquery-dataframes/issues/1452)) ([03a3a56](https://github.com/googleapis/python-bigquery-dataframes/commit/03a3a5632ab187e1208cdc7133acfe0214243832))
* Remove warnings for null index and partial ordering mode in prep for GA ([#1431](https://github.com/googleapis/python-bigquery-dataframes/issues/1431)) ([6785aee](https://github.com/googleapis/python-bigquery-dataframes/commit/6785aee97f4ee0c122d83e78409f9d6cc361b6d8))
* Warn if default `cloud_function_service_account` is used in `remote_function` ([#1424](https://github.com/googleapis/python-bigquery-dataframes/issues/1424)) ([fe7463a](https://github.com/googleapis/python-bigquery-dataframes/commit/fe7463a69e616776df3f1b3bce4abdeaf7579f9b))
* Window operations over JSON columns ([#1451](https://github.com/googleapis/python-bigquery-dataframes/issues/1451)) ([0070e77](https://github.com/googleapis/python-bigquery-dataframes/commit/0070e77579d0d0535d9f9a6c12641128e8a6dfbc))
* Write chunked text instead of dummy text for pdf chunk ([#1444](https://github.com/googleapis/python-bigquery-dataframes/issues/1444)) ([96b0e8a](https://github.com/googleapis/python-bigquery-dataframes/commit/96b0e8a7a9d405c895ffd8ece56f4e3d04e0fbe5))


### Performance Improvements

* Speed up DataFrame corr, cov ([#1309](https://github.com/googleapis/python-bigquery-dataframes/issues/1309)) ([c598c0a](https://github.com/googleapis/python-bigquery-dataframes/commit/c598c0a1694ebc5a49bd92c837e4aaf1c311a899))


### Documentation

* Add snippet for explaining the linear regression model prediction ([#1427](https://github.com/googleapis/python-bigquery-dataframes/issues/1427)) ([7c37c7d](https://github.com/googleapis/python-bigquery-dataframes/commit/7c37c7d81c0cdc4647667daeebf13d47dabf3972))

## [1.38.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.37.0...v1.38.0) (2025-02-24)


### Features

* (Preview) Support diff aggregation for timestamp series. ([#1405](https://github.com/googleapis/python-bigquery-dataframes/issues/1405)) ([abe48d6](https://github.com/googleapis/python-bigquery-dataframes/commit/abe48d6f13a954534460fa14c9337e1085d9fbb3))
* Add `GeoSeries.from_wkt() `and `GeoSeries.to_wkt()` ([#1401](https://github.com/googleapis/python-bigquery-dataframes/issues/1401)) ([2993b28](https://github.com/googleapis/python-bigquery-dataframes/commit/2993b283966960430ad8482f40f177e276db2d64))
* Support DF.__array__(copy=True) ([#1403](https://github.com/googleapis/python-bigquery-dataframes/issues/1403)) ([693ed8c](https://github.com/googleapis/python-bigquery-dataframes/commit/693ed8cfb1ecc3af161801225d3e9cda489c29dd))
* Support routines with ARRAY return type in `read_gbq_function` ([#1412](https://github.com/googleapis/python-bigquery-dataframes/issues/1412)) ([4b60049](https://github.com/googleapis/python-bigquery-dataframes/commit/4b60049e8362bfb07c136d8b2eb02b984d71f084))


### Bug Fixes

* Calling to_timdelta() over timedeltas no longer changes their values ([#1411](https://github.com/googleapis/python-bigquery-dataframes/issues/1411)) ([650a190](https://github.com/googleapis/python-bigquery-dataframes/commit/650a1907fdf84897eb7aa288863ee27d938e0879))
* Replace empty dict with None to avoid mutable default arguments ([#1416](https://github.com/googleapis/python-bigquery-dataframes/issues/1416)) ([fa4e3ad](https://github.com/googleapis/python-bigquery-dataframes/commit/fa4e3ad8bcd5db56fa26b26609cc7e58b1edf498))


### Performance Improvements

* Avoid redundant SQL casts ([#1399](https://github.com/googleapis/python-bigquery-dataframes/issues/1399)) ([6ee48d5](https://github.com/googleapis/python-bigquery-dataframes/commit/6ee48d5c16870f1caa99c3f658c2c1a0e14be749))


### Dependencies

* Remove scikit-learn and sqlalchemy as required dependencies ([#1296](https://github.com/googleapis/python-bigquery-dataframes/issues/1296)) ([fd8bc89](https://github.com/googleapis/python-bigquery-dataframes/commit/fd8bc894bdbdf551ebbec1fb93832588371ae6af))


### Documentation

* Add samples using SQL methods via the `bigframes.bigquery` module ([#1358](https://github.com/googleapis/python-bigquery-dataframes/issues/1358)) ([f54e768](https://github.com/googleapis/python-bigquery-dataframes/commit/f54e7688fda6372c6decc9b61796b0272d803c79))
* Add snippets for visualizing a time series and creating a time series model for the Limit forecasted values in time series model tutorial ([#1310](https://github.com/googleapis/python-bigquery-dataframes/issues/1310)) ([c6c9120](https://github.com/googleapis/python-bigquery-dataframes/commit/c6c9120e839647e5b3cb97f04a8d90cc8690b8a3))

## [1.37.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.36.0...v1.37.0) (2025-02-19)


### Features

* (Preview) Support add, sub, mult, div, and more between timedeltas ([#1396](https://github.com/googleapis/python-bigquery-dataframes/issues/1396)) ([ffa63d4](https://github.com/googleapis/python-bigquery-dataframes/commit/ffa63d47ca1dd1a18617f44d9b3bc33419656a20))
* (Preview) Support comparison, ordering, and filtering for timedeltas ([#1387](https://github.com/googleapis/python-bigquery-dataframes/issues/1387)) ([34d01b2](https://github.com/googleapis/python-bigquery-dataframes/commit/34d01b27f867abf10bddffdf4f88fa7052cd237c))
* (Preview) Support subtraction in DATETIME/TIMESTAMP columns with timedelta columns ([#1390](https://github.com/googleapis/python-bigquery-dataframes/issues/1390)) ([50ad3a5](https://github.com/googleapis/python-bigquery-dataframes/commit/50ad3a56e9bd77bb77d60d7d5ec497e3335a7177))
* JSON dtype support for read_pandas and Series constructor ([#1391](https://github.com/googleapis/python-bigquery-dataframes/issues/1391)) ([44f4137](https://github.com/googleapis/python-bigquery-dataframes/commit/44f4137adb02790e07c696f0641bc58390857210))


### Bug Fixes

* Ensure binops with pandas objects returns bigquery dataframes ([#1404](https://github.com/googleapis/python-bigquery-dataframes/issues/1404)) ([3cee24b](https://github.com/googleapis/python-bigquery-dataframes/commit/3cee24bae1d352015a5b6a8c18d5c394293d08fd))


### Performance Improvements

* Prune projections more aggressively ([#1398](https://github.com/googleapis/python-bigquery-dataframes/issues/1398)) ([7990262](https://github.com/googleapis/python-bigquery-dataframes/commit/7990262cf09e97c0739be922ede151d616655726))
* Simplify sum aggregate SQL text ([#1395](https://github.com/googleapis/python-bigquery-dataframes/issues/1395)) ([0145656](https://github.com/googleapis/python-bigquery-dataframes/commit/0145656e5e378442f2f38f9f04e87e33ddf345f5))
* Use simple null constraints to simplify queries ([#1381](https://github.com/googleapis/python-bigquery-dataframes/issues/1381)) ([00611d4](https://github.com/googleapis/python-bigquery-dataframes/commit/00611d4d697a8b74451375f5a7700b92a4410295))


### Documentation

* Add DataFrame.struct docs ([#1348](https://github.com/googleapis/python-bigquery-dataframes/issues/1348)) ([7e9e93a](https://github.com/googleapis/python-bigquery-dataframes/commit/7e9e93aafd26cbfec9a1710caaf97937bcb6ee05))

## [1.36.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.35.0...v1.36.0) (2025-02-11)


### Features

* (Preview) Support addition between a timestamp and a timedelta ([#1369](https://github.com/googleapis/python-bigquery-dataframes/issues/1369)) ([b598aa8](https://github.com/googleapis/python-bigquery-dataframes/commit/b598aa8ef4f6dd0cbca7629d290c5e511cdc86fc))
* (Preview) Support casting floats and list-likes to timedelta series ([#1362](https://github.com/googleapis/python-bigquery-dataframes/issues/1362)) ([65933b6](https://github.com/googleapis/python-bigquery-dataframes/commit/65933b6b7608ec52717e818d8ec1732fb756b67b))
* (Preview) Support timestamp subtractions ([#1346](https://github.com/googleapis/python-bigquery-dataframes/issues/1346)) ([86b7e72](https://github.com/googleapis/python-bigquery-dataframes/commit/86b7e72097ce67d88b72cfe031080d5af22f65cd))
* Add `bigframes.bigquery.st_area` and suggest it from `GeoSeries.area` ([#1318](https://github.com/googleapis/python-bigquery-dataframes/issues/1318)) ([8b5ffa8](https://github.com/googleapis/python-bigquery-dataframes/commit/8b5ffa8893b51016c51794865c40def74ea6716b))
* Add `GeoSeries.from_xy()` ([#1364](https://github.com/googleapis/python-bigquery-dataframes/issues/1364)) ([3c3e14c](https://github.com/googleapis/python-bigquery-dataframes/commit/3c3e14c715f476ca44f254c0d53d639ea5988a8d))


### Bug Fixes

* Dtype parameter ineffective in Series/DataFrame construction ([#1354](https://github.com/googleapis/python-bigquery-dataframes/issues/1354)) ([b9bdca8](https://github.com/googleapis/python-bigquery-dataframes/commit/b9bdca8285ee54fecf3795fbf3cbea6f878ee8ca))
* Translate labels to col ids when copying dataframes ([#1372](https://github.com/googleapis/python-bigquery-dataframes/issues/1372)) ([0c55b07](https://github.com/googleapis/python-bigquery-dataframes/commit/0c55b07dc001b568875f06d578ca7d59409f2a11))


### Performance Improvements

* Prune unused operations from sql ([#1365](https://github.com/googleapis/python-bigquery-dataframes/issues/1365)) ([923da03](https://github.com/googleapis/python-bigquery-dataframes/commit/923da037ef6e4e7f8b54924ea5644c2c5ceb2234))
* Simplify merge join key coalescing ([#1361](https://github.com/googleapis/python-bigquery-dataframes/issues/1361)) ([7ae565d](https://github.com/googleapis/python-bigquery-dataframes/commit/7ae565d9e0e59fdf75c7659c0263562688ccc1e8))

## [1.35.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.34.0...v1.35.0) (2025-02-04)


### Features

* (Preview) Support timedeltas for read_pandas() ([#1349](https://github.com/googleapis/python-bigquery-dataframes/issues/1349)) ([866ba9e](https://github.com/googleapis/python-bigquery-dataframes/commit/866ba9efb54f11c1fc2ced0d7995fff86277b049))
* Add Series.keys() ([#1342](https://github.com/googleapis/python-bigquery-dataframes/issues/1342)) ([deb015d](https://github.com/googleapis/python-bigquery-dataframes/commit/deb015dc1276549519d51363501355272f8976d8))
* Allow `case_when` to change dtypes if case list contains the condition `(True, some_default_value)` ([#1311](https://github.com/googleapis/python-bigquery-dataframes/issues/1311)) ([5c2a2c6](https://github.com/googleapis/python-bigquery-dataframes/commit/5c2a2c6086be20cba7da08ecd37899699aab518f))
* Support python type as astype arg ([#1316](https://github.com/googleapis/python-bigquery-dataframes/issues/1316)) ([b26e135](https://github.com/googleapis/python-bigquery-dataframes/commit/b26e13570f198ec4d252590a8c07253624db667a))
* Support time_series_id_col in ARIMAPlus  ([#1282](https://github.com/googleapis/python-bigquery-dataframes/issues/1282)) ([97532c9](https://github.com/googleapis/python-bigquery-dataframes/commit/97532c9ba02cd709d69666dd0afca5c1df8b9faf))


### Bug Fixes

* Exclude `DataFrame` and `Series` `__call__` from unimplemented API metrics ([#1351](https://github.com/googleapis/python-bigquery-dataframes/issues/1351)) ([f2d5264](https://github.com/googleapis/python-bigquery-dataframes/commit/f2d526445da7dae29c49c8d6dacdfee7d2fa9d79))
* Make `DataFrame` `__getattr__` and `__setattr__` more robust to subclassing ([#1352](https://github.com/googleapis/python-bigquery-dataframes/issues/1352)) ([417de3a](https://github.com/googleapis/python-bigquery-dataframes/commit/417de3a449e5d0748831b502f4f5b9fb9ba38714))


### Performance Improvements

* Fall back to ordering by bq pk when possible ([#1350](https://github.com/googleapis/python-bigquery-dataframes/issues/1350)) ([3c4abf2](https://github.com/googleapis/python-bigquery-dataframes/commit/3c4abf24ea186e98f629b6f83c0f3e36dc0571c6))
* Improve isin performance ([#1203](https://github.com/googleapis/python-bigquery-dataframes/issues/1203)) ([db087b0](https://github.com/googleapis/python-bigquery-dataframes/commit/db087b0bfe4b3ba965682d620079c923e098e362))
* Prevent inlining of remote ops ([#1347](https://github.com/googleapis/python-bigquery-dataframes/issues/1347)) ([012081a](https://github.com/googleapis/python-bigquery-dataframes/commit/012081af9ef825ced96ec1e772b9646cbe09d9a1))


### Dependencies

* Add support for Python 3.13 for everything but remote functions ([#1307](https://github.com/googleapis/python-bigquery-dataframes/issues/1307)) ([533db96](https://github.com/googleapis/python-bigquery-dataframes/commit/533db9685d159de2bc76307b0e0add676bd679a0))


### Documentation

* Add `GeoSeries` docs ([#1327](https://github.com/googleapis/python-bigquery-dataframes/issues/1327)) ([05f83d1](https://github.com/googleapis/python-bigquery-dataframes/commit/05f83d18d276091a1549dbba1f2baf8c91c8c37e))
* Add link to DataFrames intro to improve SEO ([#1176](https://github.com/googleapis/python-bigquery-dataframes/issues/1176)) ([aafb5be](https://github.com/googleapis/python-bigquery-dataframes/commit/aafb5be3e9c50f477fca2a1ebb5338194672913f))
* Add snippet to explain the univariate model's forecast result in the Forecast a single time series with a univariate model tutorial ([#1272](https://github.com/googleapis/python-bigquery-dataframes/issues/1272)) ([c22126b](https://github.com/googleapis/python-bigquery-dataframes/commit/c22126b846db428d21c0f5cbd2d439ecc56365b2))

## [1.34.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.33.0...v1.34.0) (2025-01-27)


### ⚠ BREAKING CHANGES

* Enable reading JSON data with `dbjson` extension dtype ([#1139](https://github.com/googleapis/python-bigquery-dataframes/issues/1139))

### Features

* (df|s).hist(), (df|s).line(), (df|s).area(), (df|s).bar(), df.scatter() ([#1320](https://github.com/googleapis/python-bigquery-dataframes/issues/1320)) ([bd3f584](https://github.com/googleapis/python-bigquery-dataframes/commit/bd3f584a7eab5d01dedebb7ca2485942ef5b5ebe))
* (Preview) Define timedelta type and to_timedelta function ([#1317](https://github.com/googleapis/python-bigquery-dataframes/issues/1317)) ([3901951](https://github.com/googleapis/python-bigquery-dataframes/commit/39019510d0c2758096589ecd0d83175f313a8cf5))
* Add DataFrame.corrwith method ([#1315](https://github.com/googleapis/python-bigquery-dataframes/issues/1315)) ([b503355](https://github.com/googleapis/python-bigquery-dataframes/commit/b5033559a77a9bc5ffb7dc1e44e02aaaaf1e051e))
* Add DataFrame.mask method ([#1302](https://github.com/googleapis/python-bigquery-dataframes/issues/1302)) ([8b8155f](https://github.com/googleapis/python-bigquery-dataframes/commit/8b8155fef9c5cd36cfabf728ccebf6a14a1cbbda))
* Enable reading JSON data with `dbjson` extension dtype ([#1139](https://github.com/googleapis/python-bigquery-dataframes/issues/1139)) ([f672262](https://github.com/googleapis/python-bigquery-dataframes/commit/f6722629fb47eed5befb0ecae2e6b5ec9042d669))

## [1.33.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.32.0...v1.33.0) (2025-01-22)


### Features

* Add `bigframes.bigquery.sql_scalar()` to apply SQL syntax on Series objects ([#1293](https://github.com/googleapis/python-bigquery-dataframes/issues/1293)) ([aa2f73a](https://github.com/googleapis/python-bigquery-dataframes/commit/aa2f73ad86e42c37d85ac867a3702eb6f2724b11))
* Add unix_seconds, unix_millis and unix_micros for timestamp series. ([#1297](https://github.com/googleapis/python-bigquery-dataframes/issues/1297)) ([e4b0c8d](https://github.com/googleapis/python-bigquery-dataframes/commit/e4b0c8dd9edda48e07c433b99f44db82e1ea2054))
* DataFrame.join supports Series other ([#1303](https://github.com/googleapis/python-bigquery-dataframes/issues/1303)) ([ee37a0a](https://github.com/googleapis/python-bigquery-dataframes/commit/ee37a0ab84e9415046e0e15955c14a1965b3a904))
* Support array output in `remote_function` ([#1057](https://github.com/googleapis/python-bigquery-dataframes/issues/1057)) ([bdee173](https://github.com/googleapis/python-bigquery-dataframes/commit/bdee1734809589e5a7a3c23ee9cd2f967adf346f))


### Bug Fixes

* Dataframe sort_values Series input keyerror. ([#1285](https://github.com/googleapis/python-bigquery-dataframes/issues/1285)) ([5a2731b](https://github.com/googleapis/python-bigquery-dataframes/commit/5a2731bda8b2e9ea54bf582f823acdb6153dbb8f))
* Fix read_gbq_function issue in dataframe apply method ([#1174](https://github.com/googleapis/python-bigquery-dataframes/issues/1174)) ([0318764](https://github.com/googleapis/python-bigquery-dataframes/commit/0318764030f6753a4e925c62612aabbb8e192fdf))
* Series sort_index and sort_values now raises when axis!=0 ([#1294](https://github.com/googleapis/python-bigquery-dataframes/issues/1294)) ([94bc2f2](https://github.com/googleapis/python-bigquery-dataframes/commit/94bc2f2dc3514fffeac625592ec4b28c32957723))


### Documentation

* Add snippet to forecast future time series in the Forecast a single time series with a univariate model tutorial ([#1271](https://github.com/googleapis/python-bigquery-dataframes/issues/1271)) ([a687050](https://github.com/googleapis/python-bigquery-dataframes/commit/a687050b2a92bed1af9cb86a812b62f9a69cf959))
* Update `bigframes.pandas.Series` docs ([#1273](https://github.com/googleapis/python-bigquery-dataframes/issues/1273)) ([0cac64f](https://github.com/googleapis/python-bigquery-dataframes/commit/0cac64f5ba3f3c9e8495fc5acb09d81c39d36de0))

## [1.32.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.31.0...v1.32.0) (2025-01-13)


### Features

* Add max_retries to TextEmbeddingGenerator and Claude3TextGenerator ([#1259](https://github.com/googleapis/python-bigquery-dataframes/issues/1259)) ([8077ff4](https://github.com/googleapis/python-bigquery-dataframes/commit/8077ff49426b103dc5a52eeb86a2c6a869c99825))
* Bigframes.bigquery.parse_json ([#1265](https://github.com/googleapis/python-bigquery-dataframes/issues/1265)) ([27bbd80](https://github.com/googleapis/python-bigquery-dataframes/commit/27bbd8085ccac175f113afbd6c94b52c034a3d97))
* Support DataFrame.astype(dict) ([#1262](https://github.com/googleapis/python-bigquery-dataframes/issues/1262)) ([5934f8e](https://github.com/googleapis/python-bigquery-dataframes/commit/5934f8ee0a1c950a820d1911d73a46f6891a40bb))


### Bug Fixes

* Avoid global mutation in `BigQueryOptions.client_endpoints_override` ([#1280](https://github.com/googleapis/python-bigquery-dataframes/issues/1280)) ([788f6e9](https://github.com/googleapis/python-bigquery-dataframes/commit/788f6e94a1e80f0ba8741a53a05a467e7b18e902))
* Fix erroneous window bounds removal during compilation ([#1163](https://github.com/googleapis/python-bigquery-dataframes/issues/1163)) ([f91756a](https://github.com/googleapis/python-bigquery-dataframes/commit/f91756a4413b10f1072c0ae96301fe854bb1ba4e))


### Dependencies

* Relax sqlglot upper bound ([#1278](https://github.com/googleapis/python-bigquery-dataframes/issues/1278)) ([c71ec09](https://github.com/googleapis/python-bigquery-dataframes/commit/c71ec093314409cd4c7a52a713dbd6164fbbd792))


### Documentation

* Add bq studio links that allows users to generate Jupiter notebooks in bq studio with github contents ([#1266](https://github.com/googleapis/python-bigquery-dataframes/issues/1266)) ([58f13cb](https://github.com/googleapis/python-bigquery-dataframes/commit/58f13cb9ef8bac3222e5013d8ae77dd20f886e30))
* Add snippet to evaluate ARIMA plus model in the Forecast a single time series with a univariate model tutorial ([#1267](https://github.com/googleapis/python-bigquery-dataframes/issues/1267)) ([3dcae2d](https://github.com/googleapis/python-bigquery-dataframes/commit/3dcae2dca45efdd4493cf3f367bf025ea291f4df))
* Add snippet to see the ARIMA coefficients in the Forecast a single time series with a univariate model tutorial ([#1268](https://github.com/googleapis/python-bigquery-dataframes/issues/1268)) ([059a564](https://github.com/googleapis/python-bigquery-dataframes/commit/059a564095dfea0518982f13c8118d3807861ccf))
* Update `bigframes.pandas.pandas` docstrings ([#1247](https://github.com/googleapis/python-bigquery-dataframes/issues/1247)) ([c4bffc3](https://github.com/googleapis/python-bigquery-dataframes/commit/c4bffc3e8ec630a362c94f9d269a66073a14ad04))
* Use 002 model for better scalability in text generation ([#1270](https://github.com/googleapis/python-bigquery-dataframes/issues/1270)) ([bb7a850](https://github.com/googleapis/python-bigquery-dataframes/commit/bb7a85005ebebfbcb0d2a4d5c4c27b354f38d3d1))

## [1.31.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.30.0...v1.31.0) (2025-01-05)


### Features

* Implement confirmation threshold for semantic operators ([#1251](https://github.com/googleapis/python-bigquery-dataframes/issues/1251)) ([5ba4511](https://github.com/googleapis/python-bigquery-dataframes/commit/5ba4511ad85cf02f0e5ad4e33ea3826b19527293))


### Bug Fixes

* Raise if trying to change `ordering_mode` after session has started ([#1252](https://github.com/googleapis/python-bigquery-dataframes/issues/1252)) ([8cfaae8](https://github.com/googleapis/python-bigquery-dataframes/commit/8cfaae8718f3c4c6739b7155a02ef13dbed73425))
* Reduce the number of labels added to query jobs ([#1245](https://github.com/googleapis/python-bigquery-dataframes/issues/1245)) ([fdcdc18](https://github.com/googleapis/python-bigquery-dataframes/commit/fdcdc189e5fcae9de68bf8fb3872136f55be36cb))


### Documentation

* Remove bq studio link ([#1258](https://github.com/googleapis/python-bigquery-dataframes/issues/1258)) ([dd4fd2e](https://github.com/googleapis/python-bigquery-dataframes/commit/dd4fd2e8bafa73b4b5d99f095943bd9a757cd5b5))
* Update bigframes.pandas.DatetimeMethods docstrings ([#1246](https://github.com/googleapis/python-bigquery-dataframes/issues/1246)) ([10f08da](https://github.com/googleapis/python-bigquery-dataframes/commit/10f08daec6034aafe48096be56683c953accc79a))
* Update semantic_operators.ipynb ([#1260](https://github.com/googleapis/python-bigquery-dataframes/issues/1260)) ([a2ed989](https://github.com/googleapis/python-bigquery-dataframes/commit/a2ed989fac789b0debacc0ec8a044b473cc6112c))

## [1.30.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.29.0...v1.30.0) (2024-12-30)


### Features

* Add `GeoSeries.x` and `GeoSeries.y` ([#1126](https://github.com/googleapis/python-bigquery-dataframes/issues/1126)) ([4c3548f](https://github.com/googleapis/python-bigquery-dataframes/commit/4c3548f060ba7ce649aa368fa9367dfc769ae0c3))
* Add `LinearRegression.predict_explain()` to generate `ML.EXPLAIN_PREDICT`  columns ([#1190](https://github.com/googleapis/python-bigquery-dataframes/issues/1190)) ([e13eca2](https://github.com/googleapis/python-bigquery-dataframes/commit/e13eca2128b2bf8a914a5ce781b82dffb95563a8))
* Add `LogisticRegression.predict_explain()` to generate `ML.EXPLAIN_PREDICT` columns ([#1222](https://github.com/googleapis/python-bigquery-dataframes/issues/1222)) ([bcbc732](https://github.com/googleapis/python-bigquery-dataframes/commit/bcbc732f321ab31f8fb6b995aeb908ac87750587))
* Add `write_engine` parameter to `read_FORMATNAME` methods to control how data is written to BigQuery ([#371](https://github.com/googleapis/python-bigquery-dataframes/issues/371)) ([ed47ef1](https://github.com/googleapis/python-bigquery-dataframes/commit/ed47ef16ba6f4ae67a128712fd67113aefe08467))
* Add client side retry to GeminiTextGenerator ([#1242](https://github.com/googleapis/python-bigquery-dataframes/issues/1242)) ([8193abe](https://github.com/googleapis/python-bigquery-dataframes/commit/8193abe395c5648db8169818eca29aee76c46478))
* Add Gemini-pro-1.5 to GeminiTextGenerator Tuning and Support score() method in Gemini-pro-1.5 ([#1208](https://github.com/googleapis/python-bigquery-dataframes/issues/1208)) ([298fc73](https://github.com/googleapis/python-bigquery-dataframes/commit/298fc73985daf565033347dcf40afd0d5560c717))
* Add support for `LinearRegression.predict_explain` and `LogisticRegression.predict_explain` parameter, `top_k_features` ([#1228](https://github.com/googleapis/python-bigquery-dataframes/issues/1228)) ([3068e19](https://github.com/googleapis/python-bigquery-dataframes/commit/3068e19495f99d2d7c39c67672350d0b411f79b7))
* Support dataframe where method ([#1166](https://github.com/googleapis/python-bigquery-dataframes/issues/1166)) ([71b4053](https://github.com/googleapis/python-bigquery-dataframes/commit/71b4053f855239cc3b2f659a6bfa776e38a1d4d3))


### Bug Fixes

* Arima model series input. ([#1237](https://github.com/googleapis/python-bigquery-dataframes/issues/1237)) ([f7d52d9](https://github.com/googleapis/python-bigquery-dataframes/commit/f7d52d916e8fb6362abc56b3a27cdd994e994214))
* Json in struct destination type ([#1187](https://github.com/googleapis/python-bigquery-dataframes/issues/1187)) ([200c9bb](https://github.com/googleapis/python-bigquery-dataframes/commit/200c9bbcf020913710de86822e2e2917484932fa))
* Throw an error message when setting is_row_processor=True to read a multi param function ([#1160](https://github.com/googleapis/python-bigquery-dataframes/issues/1160)) ([b2816a5](https://github.com/googleapis/python-bigquery-dataframes/commit/b2816a5df2d03b97757b46a004ac54d86d1e26a1))


### Documentation

* Add an "open in BQ Studio" link to all BigFrames sample notebooks ([#1223](https://github.com/googleapis/python-bigquery-dataframes/issues/1223)) ([e0a8288](https://github.com/googleapis/python-bigquery-dataframes/commit/e0a82888cd34fa2404ac68229dc38496cb22c67b))
* Add bq studio link for a new ipynb file called "bq_dataframes_template.ipynb" ([#1239](https://github.com/googleapis/python-bigquery-dataframes/issues/1239)) ([840aaff](https://github.com/googleapis/python-bigquery-dataframes/commit/840aaff6d5895ef0594a4f02bde03143c36e7d82))
* Add example for logistic regression ([#1240](https://github.com/googleapis/python-bigquery-dataframes/issues/1240)) ([4d854fd](https://github.com/googleapis/python-bigquery-dataframes/commit/4d854fd6c7b6b7c2322032d720befc773cc56412))
* Add examples for ml PCA and SimpleImputer ([#1236](https://github.com/googleapis/python-bigquery-dataframes/issues/1236)) ([0d84459](https://github.com/googleapis/python-bigquery-dataframes/commit/0d84459a083bbad2cb694da0256c4ff4a2438d4e))
* Add KMeans example ([#1234](https://github.com/googleapis/python-bigquery-dataframes/issues/1234)) ([d87ab97](https://github.com/googleapis/python-bigquery-dataframes/commit/d87ab97011d09784ab528ec1ab1df7f3591502a6))
* Add linear model example ([#1235](https://github.com/googleapis/python-bigquery-dataframes/issues/1235)) ([2c3e1fd](https://github.com/googleapis/python-bigquery-dataframes/commit/2c3e1fde7614057ac3deb637993134e7a9661c3d))
* Add ml.model_selection examples ([#1238](https://github.com/googleapis/python-bigquery-dataframes/issues/1238)) ([50648e4](https://github.com/googleapis/python-bigquery-dataframes/commit/50648e4d5d7c0b8b41d9a9605a9923ead73a7831))
* Add python snippet for "Create the time series model" section of the Forecast a single time series with a univariate model tutorial ([#1227](https://github.com/googleapis/python-bigquery-dataframes/issues/1227)) ([20f3190](https://github.com/googleapis/python-bigquery-dataframes/commit/20f3190d2fc26846f55328a7481de70e9fe3f84b))

## [1.29.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.28.0...v1.29.0) (2024-12-12)


### Features

* Add Gemini 2.0 preview text model support ([#1209](https://github.com/googleapis/python-bigquery-dataframes/issues/1209)) ([1021d57](https://github.com/googleapis/python-bigquery-dataframes/commit/1021d5761a291f2327fc10216e938826e53dbcc4))


### Documentation

* Add Gemini 2.0 text gen sample notebook ([#1211](https://github.com/googleapis/python-bigquery-dataframes/issues/1211)) ([9596b66](https://github.com/googleapis/python-bigquery-dataframes/commit/9596b66a8a41f5e5db6fa5f87b01c5363ffa89c4))
* Update bigframes.pandas.index docs return types ([#1191](https://github.com/googleapis/python-bigquery-dataframes/issues/1191)) ([c63e7da](https://github.com/googleapis/python-bigquery-dataframes/commit/c63e7dad6fe67f5769ddcdd1730666580a7e7a05))

## [1.28.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.27.0...v1.28.0) (2024-12-11)


### Features

* (Series | DataFrame).plot.bar ([#1152](https://github.com/googleapis/python-bigquery-dataframes/issues/1152)) ([0fae2e0](https://github.com/googleapis/python-bigquery-dataframes/commit/0fae2e0291ec8d22341b5b543e8f1b384f83cd3c))
* `bigframes.bigquery.vector_search` supports `use_brute_force` and `fraction_lists_to_search` parameters ([#1158](https://github.com/googleapis/python-bigquery-dataframes/issues/1158)) ([131edc3](https://github.com/googleapis/python-bigquery-dataframes/commit/131edc3d79f46d35a25422f0db7f150e63e8f561))
* Add `ARIMAPlus.predict_explain()` to generate forecasts with explanation columns  ([#1177](https://github.com/googleapis/python-bigquery-dataframes/issues/1177)) ([05f8b4d](https://github.com/googleapis/python-bigquery-dataframes/commit/05f8b4d2b2b5f624097228e65a3c42364fc40d36))
* Add client_endpoints_override to bq options ([#1167](https://github.com/googleapis/python-bigquery-dataframes/issues/1167)) ([be74b99](https://github.com/googleapis/python-bigquery-dataframes/commit/be74b99977cfbd513def5b7e439de6b7706c0712))
* Add support for temporal types in dataframe's describe() method ([#1189](https://github.com/googleapis/python-bigquery-dataframes/issues/1189)) ([2d564a6](https://github.com/googleapis/python-bigquery-dataframes/commit/2d564a6a9925b69c7e9a15b532fb66ad68c3e264))
* Allow join-free alignment of analytic expressions ([#1168](https://github.com/googleapis/python-bigquery-dataframes/issues/1168)) ([daef4f0](https://github.com/googleapis/python-bigquery-dataframes/commit/daef4f0c7c5ff2d0a4e9a6ffefeb81f43780ac8b))
* Series.isin supports bigframes.Series arg ([#1195](https://github.com/googleapis/python-bigquery-dataframes/issues/1195)) ([0d8a16b](https://github.com/googleapis/python-bigquery-dataframes/commit/0d8a16ba77a66dce544d0a7cf411fca0adc2a694))
* Update llm.TextEmbeddingGenerator to 005 ([#1186](https://github.com/googleapis/python-bigquery-dataframes/issues/1186)) ([3072d38](https://github.com/googleapis/python-bigquery-dataframes/commit/3072d382c6ff57bdb37d7e080c794c67dbf6e701))


### Bug Fixes

* Fix error loading local dataframes into bigquery ([#1165](https://github.com/googleapis/python-bigquery-dataframes/issues/1165)) ([5b355ef](https://github.com/googleapis/python-bigquery-dataframes/commit/5b355efde122ed76b1cff39900ab8f94f5a13a30))
* Fix null index join with 'on' arg ([#1153](https://github.com/googleapis/python-bigquery-dataframes/issues/1153)) ([9015c33](https://github.com/googleapis/python-bigquery-dataframes/commit/9015c33e73675ebb2299487dce3295732ea0527e))
* Fix series.isin using local path always ([#1202](https://github.com/googleapis/python-bigquery-dataframes/issues/1202)) ([a44eafd](https://github.com/googleapis/python-bigquery-dataframes/commit/a44eafdd95eb1b994dc82411640b61fd0a78a492))


### Performance Improvements

* Update df.corr, df.cov to be used with more than 30 columns case. ([#1161](https://github.com/googleapis/python-bigquery-dataframes/issues/1161)) ([9dcf1aa](https://github.com/googleapis/python-bigquery-dataframes/commit/9dcf1aa918919704dcf4d12b05935b22fb502fc6))


### Dependencies

* Remove `ibis-framework` by vendoring a fork of the package to `bigframes_vendored`. ([#1170](https://github.com/googleapis/python-bigquery-dataframes/pull/1170)) ([421d24d](https://github.com/googleapis/python-bigquery-dataframes/commit/421d24d6e61d557aa696fc701c08c84389f72ed2))


### Documentation

* Add a code sample using `bpd.options.bigquery.ordering_mode = "partial"` ([#909](https://github.com/googleapis/python-bigquery-dataframes/issues/909)) ([f80d705](https://github.com/googleapis/python-bigquery-dataframes/commit/f80d70503b80559a0b1fe64434383aa3e028bf9b))
* Add snippet for creating boosted tree model ([#1142](https://github.com/googleapis/python-bigquery-dataframes/issues/1142)) ([a972668](https://github.com/googleapis/python-bigquery-dataframes/commit/a972668833a454fb18e6cb148697165edd46e8cc))
* Add snippet for evaluating a boosted tree model ([#1154](https://github.com/googleapis/python-bigquery-dataframes/issues/1154)) ([9d8970a](https://github.com/googleapis/python-bigquery-dataframes/commit/9d8970ac1f18b2520a061ac743e767ca8593cc8c))
* Add snippet for predicting classifications using a boosted tree model ([#1156](https://github.com/googleapis/python-bigquery-dataframes/issues/1156)) ([e7b83f1](https://github.com/googleapis/python-bigquery-dataframes/commit/e7b83f166ef56e631120050103c2f43f454fce44))
* Add third party `pandas.Index methods` and docstrings ([#1171](https://github.com/googleapis/python-bigquery-dataframes/issues/1171)) ([a970294](https://github.com/googleapis/python-bigquery-dataframes/commit/a9702945286fbe500ade4d0f0c14cc60a8aa00eb))
* Fix Bigframes.Pandas.General_Function missing docs ([#1164](https://github.com/googleapis/python-bigquery-dataframes/issues/1164)) ([de923d0](https://github.com/googleapis/python-bigquery-dataframes/commit/de923d01b904b96cc51dfd526b6a412f28ff10c4))
* Update `bigframes.pandas.Index` docstrings ([#1144](https://github.com/googleapis/python-bigquery-dataframes/issues/1144)) ([557ab8d](https://github.com/googleapis/python-bigquery-dataframes/commit/557ab8df526fcf743af0a609ec7ec636b00d0c0b))

## [1.27.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.26.0...v1.27.0) (2024-11-16)


### Features

* Add astype(type, errors='null') to cast safely ([#1122](https://github.com/googleapis/python-bigquery-dataframes/issues/1122)) ([b4d17ff](https://github.com/googleapis/python-bigquery-dataframes/commit/b4d17ffdd891da266ad9765a087d3512c0e056fc))


### Bug Fixes

* Dataframe fillna with scalar. ([#1132](https://github.com/googleapis/python-bigquery-dataframes/issues/1132)) ([37f8c32](https://github.com/googleapis/python-bigquery-dataframes/commit/37f8c32a541565208602f3f6ed37dded13e16b9b))
* Exclude index columns from model fitting processes. ([#1138](https://github.com/googleapis/python-bigquery-dataframes/issues/1138)) ([8d4da15](https://github.com/googleapis/python-bigquery-dataframes/commit/8d4da1582a5965e6a1f9732ec0ce592ea47ce5fa))
* Unordered mode too many labels issue. ([#1148](https://github.com/googleapis/python-bigquery-dataframes/issues/1148)) ([7216b21](https://github.com/googleapis/python-bigquery-dataframes/commit/7216b21abd01bc61878bb5686f83ee13ef297912))


### Documentation

* Document groupby.head and groupby.size methods ([#1111](https://github.com/googleapis/python-bigquery-dataframes/issues/1111)) ([a61eb4d](https://github.com/googleapis/python-bigquery-dataframes/commit/a61eb4d6e323e5001715d402e0e67054df6e62af))

## [1.26.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.25.0...v1.26.0) (2024-11-12)


### Features

* Add basic geopandas functionality ([#962](https://github.com/googleapis/python-bigquery-dataframes/issues/962)) ([3759c63](https://github.com/googleapis/python-bigquery-dataframes/commit/3759c6397eaa3c46c4142aa51ca22be3dc8e4971))
* Support `json_extract_string_array` in the `bigquery` module ([#1131](https://github.com/googleapis/python-bigquery-dataframes/issues/1131)) ([4ef8bac](https://github.com/googleapis/python-bigquery-dataframes/commit/4ef8bacdcc5447ba53c0f354526346f4dec7c5a1))


### Bug Fixes

* Fix Series.to_frame generating string label instead of int where name is None ([#1118](https://github.com/googleapis/python-bigquery-dataframes/issues/1118)) ([14e32b5](https://github.com/googleapis/python-bigquery-dataframes/commit/14e32b51c11c1718128f49ef94e754afc0ac0618))
* Update the API documentation with newly added rep ([#1120](https://github.com/googleapis/python-bigquery-dataframes/issues/1120)) ([72c228b](https://github.com/googleapis/python-bigquery-dataframes/commit/72c228b15627e6047d60ae42740563a6dfea73da))


### Performance Improvements

* Reduce CURRENT_TIMESTAMP queries ([#1114](https://github.com/googleapis/python-bigquery-dataframes/issues/1114)) ([32274b1](https://github.com/googleapis/python-bigquery-dataframes/commit/32274b130849b37d7e587643cf7b6d109455ff38))
* Reduce dry runs from read_gbq with table ([#1129](https://github.com/googleapis/python-bigquery-dataframes/issues/1129)) ([f7e4354](https://github.com/googleapis/python-bigquery-dataframes/commit/f7e435488d630cf4cf493c89ecdde94a95a7a0d7))


### Documentation

* Add file for Classification with a Boosted Treed Model and snippet for preparing sample data ([#1135](https://github.com/googleapis/python-bigquery-dataframes/issues/1135)) ([7ac6639](https://github.com/googleapis/python-bigquery-dataframes/commit/7ac6639fb0e8baf5fb3adf5785dffd8cf9b06702))
* Add snippet for Linear Regression tutorial Predict Outcomes section ([#1101](https://github.com/googleapis/python-bigquery-dataframes/issues/1101)) ([108f4a9](https://github.com/googleapis/python-bigquery-dataframes/commit/108f4a98463596d8df6d381b3580eb72eab41b6e))
* Update `DataFrame` docstrings to include the errors section ([#1127](https://github.com/googleapis/python-bigquery-dataframes/issues/1127)) ([a38d4c4](https://github.com/googleapis/python-bigquery-dataframes/commit/a38d4c422b6b312f6a54d7b1dd105a474ec2e91a))
* Update GroupBy docstrings ([#1103](https://github.com/googleapis/python-bigquery-dataframes/issues/1103)) ([9867a78](https://github.com/googleapis/python-bigquery-dataframes/commit/9867a788e7c46bf0850cacbe7cd41a11fea32d6b))
* Update Session doctrings to include exceptions ([#1130](https://github.com/googleapis/python-bigquery-dataframes/issues/1130)) ([a870421](https://github.com/googleapis/python-bigquery-dataframes/commit/a87042158b181dceee31124fe208926a3bb1071f))

## [1.25.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.24.0...v1.25.0) (2024-10-29)


### Features

* Add the `ground_with_google_search` option for GeminiTextGenerator predict ([#1119](https://github.com/googleapis/python-bigquery-dataframes/issues/1119)) ([ca02cd4](https://github.com/googleapis/python-bigquery-dataframes/commit/ca02cd4b87d354c1e01c670cd9d4e36fa74896f5))
* Add warning when user tries to access struct series fields with `__getitem__` ([#1082](https://github.com/googleapis/python-bigquery-dataframes/issues/1082)) ([20e5c58](https://github.com/googleapis/python-bigquery-dataframes/commit/20e5c58868af8b18595d5635cb7722da4f622eb5))
* Allow `fit` to take additional eval data in linear and ensemble models ([#1096](https://github.com/googleapis/python-bigquery-dataframes/issues/1096)) ([254875c](https://github.com/googleapis/python-bigquery-dataframes/commit/254875c25f39df4bc477e1ed7339ecb30b395ab6))
* Support context manager for bigframes session ([#1107](https://github.com/googleapis/python-bigquery-dataframes/issues/1107)) ([5f7b8b1](https://github.com/googleapis/python-bigquery-dataframes/commit/5f7b8b189c093629d176ffc99364767dc766397a))


### Performance Improvements

* Improve series.unique performance and replace drop_duplicates i… ([#1108](https://github.com/googleapis/python-bigquery-dataframes/issues/1108)) ([499f24a](https://github.com/googleapis/python-bigquery-dataframes/commit/499f24a5f22ce484db96eb09cd3a0ce972398d81))

## [1.24.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.23.0...v1.24.0) (2024-10-24)


### Features

* Support series items method ([#1089](https://github.com/googleapis/python-bigquery-dataframes/issues/1089)) ([245a89c](https://github.com/googleapis/python-bigquery-dataframes/commit/245a89c36544faf2bcecb5735abbc00c0b4dd687))


### Documentation

* Update docstrings of DataFrame and related files ([#1092](https://github.com/googleapis/python-bigquery-dataframes/issues/1092)) ([15e9fd5](https://github.com/googleapis/python-bigquery-dataframes/commit/15e9fd547a01572cbda3d21de04d5548c7a4a82c))

## [1.23.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.22.0...v1.23.0) (2024-10-23)


### Features

* Add `bigframes.bigquery.create_vector_index` to assist in creating vector index on `ARRAY<FLOAT64>` columns ([#1024](https://github.com/googleapis/python-bigquery-dataframes/issues/1024)) ([863d694](https://github.com/googleapis/python-bigquery-dataframes/commit/863d6942eaf0cc435c3b76dc5d579c68fd478aa4))
* Add gemini-1.5-pro-002 and gemini-1.5-flash-002 to known Gemini model list. ([#1105](https://github.com/googleapis/python-bigquery-dataframes/issues/1105)) ([7094c85](https://github.com/googleapis/python-bigquery-dataframes/commit/7094c85945efeb57067640404f7b98969401191b))
* Add support for pandas series & data frames as inputs for ml models.  ([#1088](https://github.com/googleapis/python-bigquery-dataframes/issues/1088)) ([30c8883](https://github.com/googleapis/python-bigquery-dataframes/commit/30c8883ff19db2c223d84c099c7b822467e9eb9a))
* Cleanup temp resources with session deletion ([#1068](https://github.com/googleapis/python-bigquery-dataframes/issues/1068)) ([1d5373d](https://github.com/googleapis/python-bigquery-dataframes/commit/1d5373dd531c95b4a6a4132ef9b0ead0ecab14b4))
* Show possible correct key(s) in `.__getitem__` KeyError message ([#1097](https://github.com/googleapis/python-bigquery-dataframes/issues/1097)) ([32fab96](https://github.com/googleapis/python-bigquery-dataframes/commit/32fab9626b9278e20c70c2ada8702e28e167a539))
* Support uploading local geo data ([#1036](https://github.com/googleapis/python-bigquery-dataframes/issues/1036)) ([51cdd33](https://github.com/googleapis/python-bigquery-dataframes/commit/51cdd33e9f8377b3b992e0392eeb212aed499e3b))


### Bug Fixes

* Escape ids more consistently in ml module ([#1074](https://github.com/googleapis/python-bigquery-dataframes/issues/1074)) ([103e998](https://github.com/googleapis/python-bigquery-dataframes/commit/103e99823d442a36b2aaa5113950b988f6d3ba1e))
* Model.fit metric not collected issue. ([#1085](https://github.com/googleapis/python-bigquery-dataframes/issues/1085)) ([06cec00](https://github.com/googleapis/python-bigquery-dataframes/commit/06cec00c51ba4b8df591e0988379db75b20c450b))
* Remove index requirement from some dataframe APIs ([#1073](https://github.com/googleapis/python-bigquery-dataframes/issues/1073)) ([2d16f6d](https://github.com/googleapis/python-bigquery-dataframes/commit/2d16f6d1e9519e228533a67084000568a61c086e))
* Update session metrics in `read_gbq_query` ([#1084](https://github.com/googleapis/python-bigquery-dataframes/issues/1084)) ([dced460](https://github.com/googleapis/python-bigquery-dataframes/commit/dced46070ee4212b5585a1eb53ae341dc0bf63ba))


### Performance Improvements

* Speed up tree transforms during sql compile ([#1071](https://github.com/googleapis/python-bigquery-dataframes/issues/1071)) ([d73fe9d](https://github.com/googleapis/python-bigquery-dataframes/commit/d73fe9d5fd2907aeaaa892a329221c10bb390da0))
* Utilize ORDER BY LIMIT over ROW_NUMBER where possible ([#1077](https://github.com/googleapis/python-bigquery-dataframes/issues/1077)) ([7003d1a](https://github.com/googleapis/python-bigquery-dataframes/commit/7003d1ae6fddd535f6c206081e85f82bb6006f17))


### Documentation

* Add ml tutorial for Evaluate the model ([#1038](https://github.com/googleapis/python-bigquery-dataframes/issues/1038)) ([a120bae](https://github.com/googleapis/python-bigquery-dataframes/commit/a120bae2a8039d6115369b1f4a9047d4f0586120))
* Show best practice of closing the session to cleanup resources in sample notebooks ([#1095](https://github.com/googleapis/python-bigquery-dataframes/issues/1095)) ([62a88e8](https://github.com/googleapis/python-bigquery-dataframes/commit/62a88e87f55f9cc109aa38f4b7ac10dd45ca41fd))
* Update docstrings of Session and related files ([#1087](https://github.com/googleapis/python-bigquery-dataframes/issues/1087)) ([bf93e80](https://github.com/googleapis/python-bigquery-dataframes/commit/bf93e808daad2454e5c1aa933e0d2164d63084e7))

## [1.22.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.21.0...v1.22.0) (2024-10-09)


### Features

* Support regional endpoints for more bigquery locations ([#1061](https://github.com/googleapis/python-bigquery-dataframes/issues/1061)) ([45b672a](https://github.com/googleapis/python-bigquery-dataframes/commit/45b672a9a6359ec8c4755d94e63e5ae77a39754b))
* Update LLM generators to warn user about model name instead of raising error. ([#1048](https://github.com/googleapis/python-bigquery-dataframes/issues/1048)) ([650d80d](https://github.com/googleapis/python-bigquery-dataframes/commit/650d80d1ad90927068cdb71efbfc548b416641a6))


### Bug Fixes

* Access MATERIALIZED_VIEW with read_gbq ([#1070](https://github.com/googleapis/python-bigquery-dataframes/issues/1070)) ([601e984](https://github.com/googleapis/python-bigquery-dataframes/commit/601e984aeb3ebf1dcf9cb3f1c34b7f0e4ec7cd16))
* Correct zero row count in DataFrame from table view ([#1062](https://github.com/googleapis/python-bigquery-dataframes/issues/1062)) ([b536070](https://github.com/googleapis/python-bigquery-dataframes/commit/b53607015abb79be0aa5666681f1c53b5b1bc2b5))
* Fix generic error message when entering an incorrect column name ([#1031](https://github.com/googleapis/python-bigquery-dataframes/issues/1031)) ([5ac217d](https://github.com/googleapis/python-bigquery-dataframes/commit/5ac217d650bc4f5576ba2b6595a3c0b1d88813ad))
* Make `explode` respect the index labels ([#1064](https://github.com/googleapis/python-bigquery-dataframes/issues/1064)) ([99ca0df](https://github.com/googleapis/python-bigquery-dataframes/commit/99ca0df90acbbd81197c9b6718b7de7e4dfb86cc))
* Make invalid location warning case-insensitive ([#1044](https://github.com/googleapis/python-bigquery-dataframes/issues/1044)) ([b6cd55a](https://github.com/googleapis/python-bigquery-dataframes/commit/b6cd55afc49b522904a13a7fd34d40201d176588))
* Remove palm2 test case from llm load test ([#1063](https://github.com/googleapis/python-bigquery-dataframes/issues/1063)) ([575a10a](https://github.com/googleapis/python-bigquery-dataframes/commit/575a10a7ba0fbac76867f02da1dd65355f00d7aa))
* Show warning for unknown location set through .ctor ([#1052](https://github.com/googleapis/python-bigquery-dataframes/issues/1052)) ([02c2da7](https://github.com/googleapis/python-bigquery-dataframes/commit/02c2da733b834b99d8044f3c5cac3ac9a85802a6))


### Performance Improvements

* Reduce schema tracking overhead ([#1056](https://github.com/googleapis/python-bigquery-dataframes/issues/1056)) ([1c3879d](https://github.com/googleapis/python-bigquery-dataframes/commit/1c3879df2d6925e17e2cdca827db8ec919471f72))
* Repr generates fewer queries ([#1046](https://github.com/googleapis/python-bigquery-dataframes/issues/1046)) ([d204603](https://github.com/googleapis/python-bigquery-dataframes/commit/d204603fdc024823421397dbe514f1f7ced1bc2c))
* Speedup internal tree comparisons ([#1060](https://github.com/googleapis/python-bigquery-dataframes/issues/1060)) ([4379438](https://github.com/googleapis/python-bigquery-dataframes/commit/4379438fc4f44ea847fd2c00a82af544265a30d2))


### Documentation

* Add docstring return type section to BigQueryOptions class ([#964](https://github.com/googleapis/python-bigquery-dataframes/issues/964)) ([307385f](https://github.com/googleapis/python-bigquery-dataframes/commit/307385f5295ae6918e7d42dcca2c0e0c32e82446))

## [1.21.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.20.0...v1.21.0) (2024-10-02)


### Features

* Add deprecation warning to PaLM2TextGenerator model ([#1035](https://github.com/googleapis/python-bigquery-dataframes/issues/1035)) ([1183b0f](https://github.com/googleapis/python-bigquery-dataframes/commit/1183b0fb2be7af7386e4bd0d0d1312433db60454))
* Add DeprecationWarning for PaLM2TextEmbeddingGenerator ([#1018](https://github.com/googleapis/python-bigquery-dataframes/issues/1018)) ([4af5bbb](https://github.com/googleapis/python-bigquery-dataframes/commit/4af5bbb9e42fdb0add17308475c7881d7035fbfd))
* Add ml.model_selection.cross_validate support ([#1020](https://github.com/googleapis/python-bigquery-dataframes/issues/1020)) ([1a38063](https://github.com/googleapis/python-bigquery-dataframes/commit/1a380631f793f82637cd384601956ee4457dc58a))
* Allow access of struct fields with dot operators on `Series` ([#1019](https://github.com/googleapis/python-bigquery-dataframes/issues/1019)) ([ef76f13](https://github.com/googleapis/python-bigquery-dataframes/commit/ef76f137fbbf9e8f8c5a63023554d22059ab4fbd))


### Bug Fixes

* Ensure no double execution for to_pandas ([#1032](https://github.com/googleapis/python-bigquery-dataframes/issues/1032)) ([4992cc2](https://github.com/googleapis/python-bigquery-dataframes/commit/4992cc27e46bc2b0a908c7d521785989735186f4))
* Remove pre-caching of remote function results ([#1028](https://github.com/googleapis/python-bigquery-dataframes/issues/1028)) ([0359bc8](https://github.com/googleapis/python-bigquery-dataframes/commit/0359bc85839c37b5cd10c0c418b275ac0dc29c4a))


### Documentation

* Add ml cross-validation notebook ([#1037](https://github.com/googleapis/python-bigquery-dataframes/issues/1037)) ([057f3f0](https://github.com/googleapis/python-bigquery-dataframes/commit/057f3f0d694ddffe8745443a85b4fb43081893bb))

## [1.20.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.19.0...v1.20.0) (2024-09-25)


### Features

* Add bigframes.bigquery.approx_top_count ([#1010](https://github.com/googleapis/python-bigquery-dataframes/issues/1010)) ([3263bd7](https://github.com/googleapis/python-bigquery-dataframes/commit/3263bd70cff01bc18f1ae4ac3d5aa7f9d70fd4b7))
* Add bigframes.ml.compose.SQLScalarColumnTransformer to create custom SQL-based transformations ([#955](https://github.com/googleapis/python-bigquery-dataframes/issues/955)) ([1930b4e](https://github.com/googleapis/python-bigquery-dataframes/commit/1930b4efe60295751ceef89c2a824923a35b19af))
* Allow multiple columns input for llm models ([#998](https://github.com/googleapis/python-bigquery-dataframes/issues/998)) ([2fe5e48](https://github.com/googleapis/python-bigquery-dataframes/commit/2fe5e48c56bbc359d3769824c83745d65a001dd7))


### Bug Fixes

* Fix __repr__ caching with partial ordering ([#1016](https://github.com/googleapis/python-bigquery-dataframes/issues/1016)) ([208a984](https://github.com/googleapis/python-bigquery-dataframes/commit/208a98475389f59d4e32e0cfbcc46824cac278a6))


### Documentation

* Limit pypi notebook to 7 days and add more info about differences with partial ordering mode ([#1013](https://github.com/googleapis/python-bigquery-dataframes/issues/1013)) ([3c54399](https://github.com/googleapis/python-bigquery-dataframes/commit/3c543990297ec3be0e30425ee841546217e26d2a))
* Move and edit existing linear-regression tutorial snippet ([#991](https://github.com/googleapis/python-bigquery-dataframes/issues/991)) ([4cb62fd](https://github.com/googleapis/python-bigquery-dataframes/commit/4cb62fd74fc1ac3bb21da23b8639464a9ae3525d))

## [1.19.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.18.0...v1.19.0) (2024-09-24)


### Features

* Add ml.model_selection.KFold class ([#1001](https://github.com/googleapis/python-bigquery-dataframes/issues/1001)) ([952cab9](https://github.com/googleapis/python-bigquery-dataframes/commit/952cab92e548b70d077b20bf10f5307751d2ae76))
* Support bool and bytes types in `describe(include='all')` ([#994](https://github.com/googleapis/python-bigquery-dataframes/issues/994)) ([cc48f58](https://github.com/googleapis/python-bigquery-dataframes/commit/cc48f58cbd94f8110ee863eb57d3fe8dc5a17778))
* Support ingress settings in `remote_function` ([#1011](https://github.com/googleapis/python-bigquery-dataframes/issues/1011)) ([8e9919b](https://github.com/googleapis/python-bigquery-dataframes/commit/8e9919b53899b6951a10d02643d1d0e53e15665f))


### Bug Fixes

* Fix miscasting issues with case_when ([#1003](https://github.com/googleapis/python-bigquery-dataframes/issues/1003)) ([038139d](https://github.com/googleapis/python-bigquery-dataframes/commit/038139dfa4fa89167c52c1cb559c2eb5fe2f0411))


### Performance Improvements

* Join op discards child ordering in unordered mode ([#923](https://github.com/googleapis/python-bigquery-dataframes/issues/923)) ([1b5b0ee](https://github.com/googleapis/python-bigquery-dataframes/commit/1b5b0eea92631b7dd1b688cf1da617fc7ce862dc))


### Dependencies

* Update ibis version in prerelease tests ([#1012](https://github.com/googleapis/python-bigquery-dataframes/issues/1012)) ([f89785f](https://github.com/googleapis/python-bigquery-dataframes/commit/f89785fcfc51c541253ca8c1e8baf80fbfaea3b6))

## [1.18.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.17.0...v1.18.0) (2024-09-18)


### Features

* Add "include" param to describe for string types ([#973](https://github.com/googleapis/python-bigquery-dataframes/issues/973)) ([deac6d2](https://github.com/googleapis/python-bigquery-dataframes/commit/deac6d2d6e459b26c05f6e5ff328ea03a3cff45f))
* Add `subset` parameter to `DataFrame.dropna` to select which columns to consider ([#981](https://github.com/googleapis/python-bigquery-dataframes/issues/981)) ([f7c03dc](https://github.com/googleapis/python-bigquery-dataframes/commit/f7c03dcaf7ee4d62497f6653851e390795fc60a2))


### Bug Fixes

* DataFrameGroupby.agg now works with unnamed tuples ([#985](https://github.com/googleapis/python-bigquery-dataframes/issues/985)) ([0f047b4](https://github.com/googleapis/python-bigquery-dataframes/commit/0f047b4fae2a10b2a465c506bea561f8bb8d4262))
* Fix a bug that raises exception when re-indexing columns with their original order ([#988](https://github.com/googleapis/python-bigquery-dataframes/issues/988)) ([596b03b](https://github.com/googleapis/python-bigquery-dataframes/commit/596b03bb3ea27cead9b90200b9ef3cdcd99ca184))
* Make the `Series.apply` outcome `assign`able to the original dataframe in partial ordering mode ([#874](https://github.com/googleapis/python-bigquery-dataframes/issues/874)) ([c94ead9](https://github.com/googleapis/python-bigquery-dataframes/commit/c94ead996e3bfa98edd51ff678a3d43a10ee980f))


### Dependencies

* Limit ibis-framework version to 9.2.0 ([#989](https://github.com/googleapis/python-bigquery-dataframes/issues/989)) ([06c1b33](https://github.com/googleapis/python-bigquery-dataframes/commit/06c1b3396d77d1de4f927328bae70cd7b3eb0b0b))
* Update to ibis-framework 9.x and newer sqlglot ([#827](https://github.com/googleapis/python-bigquery-dataframes/issues/827)) ([89ea44f](https://github.com/googleapis/python-bigquery-dataframes/commit/89ea44fb66314b134fc0a10d816c1659978d4182))

## [1.17.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.16.0...v1.17.0) (2024-09-11)


### Features

* Add `__version__` alias to bigframes.pandas ([#967](https://github.com/googleapis/python-bigquery-dataframes/issues/967)) ([9ce10b4](https://github.com/googleapis/python-bigquery-dataframes/commit/9ce10b4248f106ac9e09fc0fe686cece86827337))
* Add Gemini 1.5 stable models support ([#945](https://github.com/googleapis/python-bigquery-dataframes/issues/945)) ([c1cde19](https://github.com/googleapis/python-bigquery-dataframes/commit/c1cde19769c169b962b58b25f0be61c8c41edb95))
* Allow setting table labels in `to_gbq` ([#941](https://github.com/googleapis/python-bigquery-dataframes/issues/941)) ([cccc6ca](https://github.com/googleapis/python-bigquery-dataframes/commit/cccc6ca8c1271097bbe15e3d9ccdcfd7c633227a))
* Define list accessor for bigframes Series ([#946](https://github.com/googleapis/python-bigquery-dataframes/issues/946)) ([8e8279d](https://github.com/googleapis/python-bigquery-dataframes/commit/8e8279d4da90feb5766f266b49cb417f8cbec6c9))
* Enable read_csv() to process other files ([#940](https://github.com/googleapis/python-bigquery-dataframes/issues/940)) ([3b35860](https://github.com/googleapis/python-bigquery-dataframes/commit/3b35860776033fc8e71e471422c6d2b9366a7c9f))
* Include the bigframes package version alongside the feedback link in error messages ([#936](https://github.com/googleapis/python-bigquery-dataframes/issues/936)) ([7b59b6d](https://github.com/googleapis/python-bigquery-dataframes/commit/7b59b6dc6f0cedfee713b5b273d46fa84b70bfa4))


### Bug Fixes

* Astype Decimal to Int64 conversion. ([#957](https://github.com/googleapis/python-bigquery-dataframes/issues/957)) ([27764a6](https://github.com/googleapis/python-bigquery-dataframes/commit/27764a64f90092374458fafbe393bc6c30c85681))
* Make `read_gbq_function` work for multi-param functions ([#947](https://github.com/googleapis/python-bigquery-dataframes/issues/947)) ([c750be6](https://github.com/googleapis/python-bigquery-dataframes/commit/c750be6093941677572a10c36a92984e954de32c))
* Support `read_gbq_function` for axis=1 application ([#950](https://github.com/googleapis/python-bigquery-dataframes/issues/950)) ([86e54b1](https://github.com/googleapis/python-bigquery-dataframes/commit/86e54b13d2b91517b1df2d9c1f852a8e1925309a))


### Documentation

* Add docstring returns section to Options ([#937](https://github.com/googleapis/python-bigquery-dataframes/issues/937)) ([a2640a2](https://github.com/googleapis/python-bigquery-dataframes/commit/a2640a2d731c8d0aba1307311092f5e85b8ba077))
* Update title of pypi notebook example to reflect use of the PyPI public dataset ([#952](https://github.com/googleapis/python-bigquery-dataframes/issues/952)) ([cd62e60](https://github.com/googleapis/python-bigquery-dataframes/commit/cd62e604967adac0c2f8600408bd9ce7886f2f98))

## [1.16.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.15.0...v1.16.0) (2024-09-04)


### Features

* Add `DataFrame.struct.explode` to add struct subfields to a DataFrame ([#916](https://github.com/googleapis/python-bigquery-dataframes/issues/916)) ([ad2f75e](https://github.com/googleapis/python-bigquery-dataframes/commit/ad2f75ecbc3660459814716eec7d1f88d1188942))
* Implement `bigframes.bigquery.json_extract_array` ([#910](https://github.com/googleapis/python-bigquery-dataframes/issues/910)) ([575a29e](https://github.com/googleapis/python-bigquery-dataframes/commit/575a29e77d50d60d7e9a84ebb87abcdb993adef1))
* Recover struct column from exploded Series ([#904](https://github.com/googleapis/python-bigquery-dataframes/issues/904)) ([7dd304c](https://github.com/googleapis/python-bigquery-dataframes/commit/7dd304cc7168fac222fa1330f868677818d10903))


### Bug Fixes

* Fix issue with iterating on &gt;10gb dataframes ([#949](https://github.com/googleapis/python-bigquery-dataframes/issues/949)) ([2b0f0fa](https://github.com/googleapis/python-bigquery-dataframes/commit/2b0f0faf840a1ec43d007827bbbf908df62ce9d3))
* Improve `Series.replace` for dict input ([#907](https://github.com/googleapis/python-bigquery-dataframes/issues/907)) ([4208044](https://github.com/googleapis/python-bigquery-dataframes/commit/4208044222c6a8494004ec6f511a3b85f4eb4180))
* NullIndex in ML model.predict error ([#917](https://github.com/googleapis/python-bigquery-dataframes/issues/917)) ([612271d](https://github.com/googleapis/python-bigquery-dataframes/commit/612271d35675353effa465a797d6e3a1285d4d37))
* Struct field non-nullable type issue. ([#914](https://github.com/googleapis/python-bigquery-dataframes/issues/914)) ([149d5ff](https://github.com/googleapis/python-bigquery-dataframes/commit/149d5ff822da3d7fda18dbed4814e0406708cf07))
* Unordered mode errors in ml train_test_split ([#925](https://github.com/googleapis/python-bigquery-dataframes/issues/925)) ([85d7c21](https://github.com/googleapis/python-bigquery-dataframes/commit/85d7c21b4bd5dc669098342fc60d66d89ef06b2b))


### Performance Improvements

* Improve repr performance ([#918](https://github.com/googleapis/python-bigquery-dataframes/issues/918)) ([46f2dd7](https://github.com/googleapis/python-bigquery-dataframes/commit/46f2dd79f59131bbb98fe4ae3780b98cb4d50646))


### Dependencies

* Re-introduce support for numpy 1.24.x ([#931](https://github.com/googleapis/python-bigquery-dataframes/issues/931)) ([3d71913](https://github.com/googleapis/python-bigquery-dataframes/commit/3d71913b3cf357fc9e94304ca0c94070e0a16f92))
* Update minimum support to Pandas 1.5.3 and Pyarrow 10.0.1 ([#903](https://github.com/googleapis/python-bigquery-dataframes/issues/903)) ([7ed3962](https://github.com/googleapis/python-bigquery-dataframes/commit/7ed39629c638874d8e9cc3c7a9b3ec92ad480eca))


### Documentation

* Add Claude3 ML and RemoteFunc notebooks ([#930](https://github.com/googleapis/python-bigquery-dataframes/issues/930)) ([cfd16c1](https://github.com/googleapis/python-bigquery-dataframes/commit/cfd16c1278023bd2c3dce9c0cb378615aa00e58d))
* Create sample notebook to manipulate struct and array data ([#883](https://github.com/googleapis/python-bigquery-dataframes/issues/883)) ([3031903](https://github.com/googleapis/python-bigquery-dataframes/commit/303190331d3194562c5ed44fefc2c9fd1d73bedd))
* Update struct examples. ([#953](https://github.com/googleapis/python-bigquery-dataframes/issues/953)) ([d632cd0](https://github.com/googleapis/python-bigquery-dataframes/commit/d632cd03e3e3ea6dfa7c56dd459c422e95be906e))
* Use unstack() from BigQuery DataFrames instead of pandas in the PyPI sample notebook ([#890](https://github.com/googleapis/python-bigquery-dataframes/issues/890)) ([d1883cc](https://github.com/googleapis/python-bigquery-dataframes/commit/d1883cc04ce5b2944d87a00c79b99a406001ba8f))

## [1.15.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.14.0...v1.15.0) (2024-08-20)


### Features

* Add llm.TextEmbeddingGenerator to support new embedding models ([#905](https://github.com/googleapis/python-bigquery-dataframes/issues/905)) ([6bc6a41](https://github.com/googleapis/python-bigquery-dataframes/commit/6bc6a41426fbbb60e77cd77f80860f88a1751a4b))
* Add ml.llm.Claude3TextGenerator model ([#901](https://github.com/googleapis/python-bigquery-dataframes/issues/901)) ([7050038](https://github.com/googleapis/python-bigquery-dataframes/commit/7050038eeee258452860941aa6b01d6a8ae10c6f))


### Documentation

* Add columns for "requires ordering/index" to supported APIs summary ([#892](https://github.com/googleapis/python-bigquery-dataframes/issues/892)) ([d2fc51a](https://github.com/googleapis/python-bigquery-dataframes/commit/d2fc51a30c4fff6fe0b98df61eec70ddb28b37ec))
* Remove duplicate description for `kms_key_name` ([#898](https://github.com/googleapis/python-bigquery-dataframes/issues/898)) ([1053d56](https://github.com/googleapis/python-bigquery-dataframes/commit/1053d56260eef1cff6e7c419f6c86be8f7e74373))
* Update embedding model notebooks ([#906](https://github.com/googleapis/python-bigquery-dataframes/issues/906)) ([d9b8ef5](https://github.com/googleapis/python-bigquery-dataframes/commit/d9b8ef56deb0c776edeeb0112bd9d35d5ed1b70e))

## [1.14.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.13.0...v1.14.0) (2024-08-14)


### Features

* Implement `bigframes.bigquery.json_extract` ([#868](https://github.com/googleapis/python-bigquery-dataframes/issues/868)) ([3dbf84b](https://github.com/googleapis/python-bigquery-dataframes/commit/3dbf84bd1531c1f8d41ba57c2c38b3ba6abfb812))
* Implement `Series.str.__getitem__` ([#897](https://github.com/googleapis/python-bigquery-dataframes/issues/897)) ([e027b7e](https://github.com/googleapis/python-bigquery-dataframes/commit/e027b7e9d29f628d058611106014a1790459958c))


### Bug Fixes

* Fix caching from generating row numbers in partial ordering mode ([#872](https://github.com/googleapis/python-bigquery-dataframes/issues/872)) ([52b7786](https://github.com/googleapis/python-bigquery-dataframes/commit/52b7786c3a28da6c29e3ddf12629802215194ad9))


### Performance Improvements

* Generate SQL with fewer CTEs ([#877](https://github.com/googleapis/python-bigquery-dataframes/issues/877)) ([eb60804](https://github.com/googleapis/python-bigquery-dataframes/commit/eb6080460344aff2fabb7864536ea4fe24c5fbef))
* Speed up compilation by reducing redundant type normalization ([#896](https://github.com/googleapis/python-bigquery-dataframes/issues/896)) ([e0b11bc](https://github.com/googleapis/python-bigquery-dataframes/commit/e0b11bc8c038db7b950b1653ed4cd44a6246c713))


### Documentation

* Add streaming html docs ([#884](https://github.com/googleapis/python-bigquery-dataframes/issues/884)) ([171da6c](https://github.com/googleapis/python-bigquery-dataframes/commit/171da6cb33165b49d46ea6528038342abd89e9fa))
* Fix the `DisplayOptions` doc rendering ([#893](https://github.com/googleapis/python-bigquery-dataframes/issues/893)) ([3eb6a17](https://github.com/googleapis/python-bigquery-dataframes/commit/3eb6a17a5823faf5ecba92cb9a554df74477871d))
* Update streaming notebook ([#887](https://github.com/googleapis/python-bigquery-dataframes/issues/887)) ([6e6f9df](https://github.com/googleapis/python-bigquery-dataframes/commit/6e6f9df55d435afe0b3ade728ca06826e92a6ee6))

## [1.13.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.12.0...v1.13.0) (2024-08-05)


### Features

* `df.apply(axis=1)` to support remote function with mutiple params ([#851](https://github.com/googleapis/python-bigquery-dataframes/issues/851)) ([2158818](https://github.com/googleapis/python-bigquery-dataframes/commit/2158818e53e09e55c87ffd574e3ebc2e201285fb))
* Allow windowing in 'partial' ordering mode ([#861](https://github.com/googleapis/python-bigquery-dataframes/issues/861)) ([ca26fe5](https://github.com/googleapis/python-bigquery-dataframes/commit/ca26fe5f9edec519788c276a09eaff33ecd87434))
* Create a separate OrderingModePartialPreviewWarning for more fine-grained warning filters ([#879](https://github.com/googleapis/python-bigquery-dataframes/issues/879)) ([8753bdd](https://github.com/googleapis/python-bigquery-dataframes/commit/8753bdd1e44701e56eae914ebc0e91d9b1a6adf1))


### Bug Fixes

* Fix issue with invalid sql generated by ml distance functions ([#865](https://github.com/googleapis/python-bigquery-dataframes/issues/865)) ([9959fc8](https://github.com/googleapis/python-bigquery-dataframes/commit/9959fc8fcba93441fdd3d9c17e8fdbe6e6a7b504))


### Documentation

* Create sample notebook using `ordering_mode="partial"` ([#880](https://github.com/googleapis/python-bigquery-dataframes/issues/880)) ([c415eb9](https://github.com/googleapis/python-bigquery-dataframes/commit/c415eb91eb71dea53d245ba2bce416062e3f02f8))
* Update streaming notebook ([#875](https://github.com/googleapis/python-bigquery-dataframes/issues/875)) ([e9b0557](https://github.com/googleapis/python-bigquery-dataframes/commit/e9b05571123cf13079772856317ca3cd3d564c5a))

## [1.12.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.11.1...v1.12.0) (2024-07-31)


### Features

* Add bigframes-mode label to query jobs ([#832](https://github.com/googleapis/python-bigquery-dataframes/issues/832)) ([c9eaff0](https://github.com/googleapis/python-bigquery-dataframes/commit/c9eaff0a1a0731b28f4c67bca5606db12a47c8c0))
* Add config option to set partial ordering mode ([#855](https://github.com/googleapis/python-bigquery-dataframes/issues/855)) ([823c0ce](https://github.com/googleapis/python-bigquery-dataframes/commit/823c0ce57611c0918a9e9999638d7393337fe9af))
* Add stratify param support to ml.model_selection.train_test_split method ([#815](https://github.com/googleapis/python-bigquery-dataframes/issues/815)) ([27f8631](https://github.com/googleapis/python-bigquery-dataframes/commit/27f8631be81a3e136cfeb8904558bb4f3f5caa05))
* Add streaming.StreamingDataFrame class ([#864](https://github.com/googleapis/python-bigquery-dataframes/issues/864)) ([a7d7197](https://github.com/googleapis/python-bigquery-dataframes/commit/a7d7197a32c55b989ae4ea8f6cf6e1c0f7184cd4))
* Allow DataFrame.join for self-join on Null index ([#860](https://github.com/googleapis/python-bigquery-dataframes/issues/860)) ([e950533](https://github.com/googleapis/python-bigquery-dataframes/commit/e95053372c36ea5a91a2d7295c1a3a3671181670))
* Support remote function cleanup with `session.close` ([#818](https://github.com/googleapis/python-bigquery-dataframes/issues/818)) ([ed06436](https://github.com/googleapis/python-bigquery-dataframes/commit/ed06436612c0d46f190f79721416d473bde7e2f4))
* Support to_csv/parquet/json to local files/objects ([#858](https://github.com/googleapis/python-bigquery-dataframes/issues/858)) ([d0ab9cc](https://github.com/googleapis/python-bigquery-dataframes/commit/d0ab9cc47298bdde638299baecac9dffd7841ede))


### Bug Fixes

* Fewer relation joins from df self-operations ([#823](https://github.com/googleapis/python-bigquery-dataframes/issues/823)) ([0d24f73](https://github.com/googleapis/python-bigquery-dataframes/commit/0d24f737041c7dd70253ebb4baa8d8ef67bd4f1d))
* Fix 'sql' property for null index ([#844](https://github.com/googleapis/python-bigquery-dataframes/issues/844)) ([1b6a556](https://github.com/googleapis/python-bigquery-dataframes/commit/1b6a556206a7a66283339d827ab12db2753521e2))
* Fix unordered mode using ordered path to print frame ([#839](https://github.com/googleapis/python-bigquery-dataframes/issues/839)) ([93785cb](https://github.com/googleapis/python-bigquery-dataframes/commit/93785cb48be4a2eb8770129148bd0b897fed4ee7))
* Reduce redundant `remote_function` deployments ([#856](https://github.com/googleapis/python-bigquery-dataframes/issues/856)) ([cbf2d42](https://github.com/googleapis/python-bigquery-dataframes/commit/cbf2d42e4d961a7537381a9c3b28a8b463ad8f74))


### Documentation

* Add partner attribution steps to integrations sample notebook ([#835](https://github.com/googleapis/python-bigquery-dataframes/issues/835)) ([d7b333f](https://github.com/googleapis/python-bigquery-dataframes/commit/d7b333fa26acddaeb5ccca4f81b1d624dff03ba2))
* Make `get_global_session`/`close_session`/`reset_session` appears in the docs ([#847](https://github.com/googleapis/python-bigquery-dataframes/issues/847)) ([01d6bbb](https://github.com/googleapis/python-bigquery-dataframes/commit/01d6bbb7479da706dc62bb5e7d51dc28a4042812))

## [1.11.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.11.0...v1.11.1) (2024-07-08)


### Documentation

* Remove session and connection in llm notebook ([#821](https://github.com/googleapis/python-bigquery-dataframes/issues/821)) ([74170da](https://github.com/googleapis/python-bigquery-dataframes/commit/74170dabd323f1b08ad76241e37ff9f2a5b67ab5))
* Remove the experimental flask icon from the public docs ([#820](https://github.com/googleapis/python-bigquery-dataframes/issues/820)) ([067ff17](https://github.com/googleapis/python-bigquery-dataframes/commit/067ff173f0abfcf5bf06d3fbdb6d12e0fa5283c3))

## [1.11.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.10.0...v1.11.0) (2024-07-01)


### Features

* Add .agg support for size ([#792](https://github.com/googleapis/python-bigquery-dataframes/issues/792)) ([87e6018](https://github.com/googleapis/python-bigquery-dataframes/commit/87e60182c964c369079165e87ce73dd0c0481a5a))
* Add `bigframes.bigquery.json_set` ([#782](https://github.com/googleapis/python-bigquery-dataframes/issues/782)) ([1b613e0](https://github.com/googleapis/python-bigquery-dataframes/commit/1b613e00eddf18fa40ed1d08ff19c4ebeeac2197))
* Add `bigframes.streaming.to_pubsub` method to create continuous query that writes to Pub/Sub ([#801](https://github.com/googleapis/python-bigquery-dataframes/issues/801)) ([b47f32d](https://github.com/googleapis/python-bigquery-dataframes/commit/b47f32d74a0c9eb908be690b2dd56b0f5579b133))
* Add `DataFrame.to_arrow` to create Arrow Table from DataFrame ([#807](https://github.com/googleapis/python-bigquery-dataframes/issues/807)) ([1e3feda](https://github.com/googleapis/python-bigquery-dataframes/commit/1e3feda9e8fe9d08a0e3838066f6414f8015197d))
* Add `PolynomialFeatures` support to `to_gbq` and pipelines ([#805](https://github.com/googleapis/python-bigquery-dataframes/issues/805)) ([57d98b9](https://github.com/googleapis/python-bigquery-dataframes/commit/57d98b9e3298583ec40c04665ab84e6ad2b948fb))
* Add Series.peek to preview data efficiently ([#727](https://github.com/googleapis/python-bigquery-dataframes/issues/727)) ([580e1b9](https://github.com/googleapis/python-bigquery-dataframes/commit/580e1b9e965d883a67f91a6db8311c2416ca8fe5))
* Expose gcf memory param in `remote_function` ([#803](https://github.com/googleapis/python-bigquery-dataframes/issues/803)) ([014765c](https://github.com/googleapis/python-bigquery-dataframes/commit/014765c22410a0b4559896d163c440f46f7ce98f))
* More informative error when query plan too complex ([#811](https://github.com/googleapis/python-bigquery-dataframes/issues/811)) ([136dc24](https://github.com/googleapis/python-bigquery-dataframes/commit/136dc24e160339d27f6335e7b28f08cd95d2c67d))


### Bug Fixes

* Include internally required packages in `remote_function` hash ([#799](https://github.com/googleapis/python-bigquery-dataframes/issues/799)) ([4b8fc15](https://github.com/googleapis/python-bigquery-dataframes/commit/4b8fc15ec2c126566269f84d75289198fee2c655))


### Documentation

* Document dtype limitation on row processing `remote_function` ([#800](https://github.com/googleapis/python-bigquery-dataframes/issues/800)) ([487dff6](https://github.com/googleapis/python-bigquery-dataframes/commit/487dff6ac147683aef529e1ff8c197dce3fb437c))

## [1.10.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.9.0...v1.10.0) (2024-06-21)


### Features

* Add dataframe.insert ([#770](https://github.com/googleapis/python-bigquery-dataframes/issues/770)) ([e8bab68](https://github.com/googleapis/python-bigquery-dataframes/commit/e8bab681a2d07636e5809e804f4fd81b0d582685))
* Add groupby head API ([#791](https://github.com/googleapis/python-bigquery-dataframes/issues/791)) ([44202bc](https://github.com/googleapis/python-bigquery-dataframes/commit/44202bc3541df03154ea0b2cca8eac18094a91a9))
* Add ml.preprocessing.PolynomialFeatures class ([#793](https://github.com/googleapis/python-bigquery-dataframes/issues/793)) ([b4fbb51](https://github.com/googleapis/python-bigquery-dataframes/commit/b4fbb518711922c09ac6f55f3b8f6ab57c89114b))
* Bigframes.streaming module for continuous queries ([#703](https://github.com/googleapis/python-bigquery-dataframes/issues/703)) ([0433a1c](https://github.com/googleapis/python-bigquery-dataframes/commit/0433a1cff57fddda26b2c57adc0ea71f3fdd3201))
* Include index columns in DataFrame.sql if they are named ([#788](https://github.com/googleapis/python-bigquery-dataframes/issues/788)) ([c8d16c0](https://github.com/googleapis/python-bigquery-dataframes/commit/c8d16c0f72a25bce854b80be517114e1603c947e))


### Bug Fixes

* Allow `__repr__` to work with uninitialed DataFrame/Series/Index ([#778](https://github.com/googleapis/python-bigquery-dataframes/issues/778)) ([e14c7a9](https://github.com/googleapis/python-bigquery-dataframes/commit/e14c7a9e7a9cb8847e0382b135fc06c7b82b872a))
* Df.loc with the 2nd input as bigframes boolean Series ([#789](https://github.com/googleapis/python-bigquery-dataframes/issues/789)) ([a4ac82e](https://github.com/googleapis/python-bigquery-dataframes/commit/a4ac82e06221581ddfcfc1246a3e3cd65a8bb00e))
* Ensure numpy version matches in `remote_function` deployment ([#798](https://github.com/googleapis/python-bigquery-dataframes/issues/798)) ([324d93c](https://github.com/googleapis/python-bigquery-dataframes/commit/324d93cb31191520b790bbbc501468b8d1d8467d))
* Fix temp table creation retries by now throwing if table already exists. ([#787](https://github.com/googleapis/python-bigquery-dataframes/issues/787)) ([0e57d1f](https://github.com/googleapis/python-bigquery-dataframes/commit/0e57d1f1f8a150ba6faac5f667bb5b4c78f4c0a3))
* Self-join optimization doesn't needlessly invalidate caching ([#797](https://github.com/googleapis/python-bigquery-dataframes/issues/797)) ([1b96b80](https://github.com/googleapis/python-bigquery-dataframes/commit/1b96b8027a550e1601a5360f2af35d24a8806da9))

## [1.9.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.8.0...v1.9.0) (2024-06-10)


### Features

* Allow functions returned from `bpd.read_gbq_function` to execute outside of `apply` ([#706](https://github.com/googleapis/python-bigquery-dataframes/issues/706)) ([ad7d8ac](https://github.com/googleapis/python-bigquery-dataframes/commit/ad7d8ac1247ec3b9532dd5375265c36907f50da2))
* Support `bigquery.vector_search()` ([#736](https://github.com/googleapis/python-bigquery-dataframes/issues/736)) ([dad66fd](https://github.com/googleapis/python-bigquery-dataframes/commit/dad66fdd22bb2d507e7f366c970d971554598cf3))
* Support `score()` in GeminiTextGenerator ([#740](https://github.com/googleapis/python-bigquery-dataframes/issues/740)) ([b2c7d8b](https://github.com/googleapis/python-bigquery-dataframes/commit/b2c7d8b28e235c839370818137fba71796c9f02a))
* Support bytes type in `remote_function` ([#761](https://github.com/googleapis/python-bigquery-dataframes/issues/761)) ([4915424](https://github.com/googleapis/python-bigquery-dataframes/commit/4915424a68f36542e901a0ac27946f1ecb2d05ab))
* Support fit() in GeminiTextGenerator ([#758](https://github.com/googleapis/python-bigquery-dataframes/issues/758)) ([d751f5c](https://github.com/googleapis/python-bigquery-dataframes/commit/d751f5cd1cf578618eabbb992cfb6b0a3c36608c))


### Bug Fixes

* ARIMAPlus loads auto_arima_min_order param ([#752](https://github.com/googleapis/python-bigquery-dataframes/issues/752)) ([39d7013](https://github.com/googleapis/python-bigquery-dataframes/commit/39d7013a8a8d2908f20bfe54a7dc8de166323b90))
* Improve to_pandas_batches for large results ([#746](https://github.com/googleapis/python-bigquery-dataframes/issues/746)) ([61f18cb](https://github.com/googleapis/python-bigquery-dataframes/commit/61f18cb63f2785c03dc612a34c030079fc8f4172))
* Resolve issue with unset thread-local options ([#741](https://github.com/googleapis/python-bigquery-dataframes/issues/741)) ([d93dbaf](https://github.com/googleapis/python-bigquery-dataframes/commit/d93dbafe2bb405c60f7141d9ae4135db4ffdb702))


### Documentation

* Fix ML.EVALUATE spelling ([#749](https://github.com/googleapis/python-bigquery-dataframes/issues/749)) ([7899749](https://github.com/googleapis/python-bigquery-dataframes/commit/7899749505a75ed89c68e9df64124a153644de96))
* Remove LogisticRegression normal_equation strategy ([#753](https://github.com/googleapis/python-bigquery-dataframes/issues/753)) ([ea5d367](https://github.com/googleapis/python-bigquery-dataframes/commit/ea5d367d5ecc6826d30082e75c957af8362c9e61))

## [1.8.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.7.0...v1.8.0) (2024-05-31)


### Features

* `merge` only generates a default index if both inputs already have an index ([#733](https://github.com/googleapis/python-bigquery-dataframes/issues/733)) ([25d049c](https://github.com/googleapis/python-bigquery-dataframes/commit/25d049c078693466905a19cc0954fafcac6c414c))
* Add `+`, `-` as unary ops, `^` binary op ([#724](https://github.com/googleapis/python-bigquery-dataframes/issues/724)) ([968d825](https://github.com/googleapis/python-bigquery-dataframes/commit/968d8257edbfcb6d437c6203c7c0078ba782cfed))
* Add `GroupBy.size()` to get number of rows in each group ([#479](https://github.com/googleapis/python-bigquery-dataframes/issues/479)) ([1fca588](https://github.com/googleapis/python-bigquery-dataframes/commit/1fca588e4398baa0dae61bdea0d3bff17e3971b5))
* Add DataFrame `~` operator ([#721](https://github.com/googleapis/python-bigquery-dataframes/issues/721)) ([354abc1](https://github.com/googleapis/python-bigquery-dataframes/commit/354abc17b5bd55d70d47f893cfccd7cd0ac9794a))
* Add GeminiText 1.5 Preview models ([#737](https://github.com/googleapis/python-bigquery-dataframes/issues/737)) ([56cbd3b](https://github.com/googleapis/python-bigquery-dataframes/commit/56cbd3b6f17c5ac22572e872b270ac7e3636675a))
* Add slot_millis and add stats to session object ([#725](https://github.com/googleapis/python-bigquery-dataframes/issues/725)) ([72e9583](https://github.com/googleapis/python-bigquery-dataframes/commit/72e95834f8755760f3529d38f340703f3b971f0a))
* Adds bigframes.bigquery.array_to_string to convert array elements to delimited strings ([#731](https://github.com/googleapis/python-bigquery-dataframes/issues/731)) ([f12c906](https://github.com/googleapis/python-bigquery-dataframes/commit/f12c90611adb4741069ec32840ebbf2aea83a9f3))
* Allow functions decorated with `bpd.remote_function()` to execute locally ([#704](https://github.com/googleapis/python-bigquery-dataframes/issues/704)) ([d850da6](https://github.com/googleapis/python-bigquery-dataframes/commit/d850da6364b98c4e01120725e1e609ad8f6c1263))
* Ensure `"bigframes-api"` label is always set on jobs, even if the API is unknown ([#722](https://github.com/googleapis/python-bigquery-dataframes/issues/722)) ([1832778](https://github.com/googleapis/python-bigquery-dataframes/commit/1832778cfc4f29fdab1b22380f03b192eb8aebb9))
* Support `ml.SimpleImputer` in bigframes ([#708](https://github.com/googleapis/python-bigquery-dataframes/issues/708)) ([4c4415f](https://github.com/googleapis/python-bigquery-dataframes/commit/4c4415fb137e3baedc4b2d77ec146827b003557e))
* Support type annotations to supply input and output types to `bpd.remote_function()` decorator ([#717](https://github.com/googleapis/python-bigquery-dataframes/issues/717)) ([4a12e3c](https://github.com/googleapis/python-bigquery-dataframes/commit/4a12e3c6d49d78fc2b51d783cc8de5d09e7c9995))
* Support type annotations with `bpd.remote_function()` and `axis=1` (a preview feature) ([#730](https://github.com/googleapis/python-bigquery-dataframes/issues/730)) ([e5a2992](https://github.com/googleapis/python-bigquery-dataframes/commit/e5a299271e3bcf94c66fb6ef70393071c1b7dc69))


### Bug Fixes

* Correct index labels in multiple aggregations for DataFrameGroupBy ([#723](https://github.com/googleapis/python-bigquery-dataframes/issues/723)) ([6a78c89](https://github.com/googleapis/python-bigquery-dataframes/commit/6a78c89a3a766b747b03c8a739760db1c79f533f))
* Fix Null index assign series to column ([#711](https://github.com/googleapis/python-bigquery-dataframes/issues/711)) ([ffb4b57](https://github.com/googleapis/python-bigquery-dataframes/commit/ffb4b5712a1a07c703ea88f66ba3f43dd2f98197))
* Set `bpd.remote_function()`s `input_types` and `output_types` default to `None` to allow omitting them when type annotations are present ([#729](https://github.com/googleapis/python-bigquery-dataframes/issues/729)) ([0e25a3b](https://github.com/googleapis/python-bigquery-dataframes/commit/0e25a3b3ae704bf75b752c57f613e778af58bac3))
* Warn and disable time travel for linked datasets ([#712](https://github.com/googleapis/python-bigquery-dataframes/issues/712)) ([085fa9d](https://github.com/googleapis/python-bigquery-dataframes/commit/085fa9d8fe1ea4cd02a3d25d443beaa697e10784))


### Performance Improvements

* Optimize dataframe-series alignment on axis=1 ([#732](https://github.com/googleapis/python-bigquery-dataframes/issues/732)) ([3d39221](https://github.com/googleapis/python-bigquery-dataframes/commit/3d39221526df82617a8560fd2ab7ea13bc3c03d9))


### Documentation

* Add examples to DataFrameGroupBy and SeriesGroupBy ([#701](https://github.com/googleapis/python-bigquery-dataframes/issues/701)) ([e7da0f0](https://github.com/googleapis/python-bigquery-dataframes/commit/e7da0f085eb9b9cec06e5de972f07d9c1d545ac7))

## [1.7.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.6.0...v1.7.0) (2024-05-20)


### Features

* `read_gbq_query` supports `filters` ([9386373](https://github.com/googleapis/python-bigquery-dataframes/commit/9386373538c1e7827e2210c4fd9946312821b54d))
* `read_gbq` suggests a correct column name when one is not found ([9386373](https://github.com/googleapis/python-bigquery-dataframes/commit/9386373538c1e7827e2210c4fd9946312821b54d))
* Add `DefaultIndexKind.NULL` to use as `index_col` in `read_gbq*`, creating an indexless DataFrame/Series ([#662](https://github.com/googleapis/python-bigquery-dataframes/issues/662)) ([29e4886](https://github.com/googleapis/python-bigquery-dataframes/commit/29e4886d41e3d615bc493cf3a104ef1b0698ece8))
* Bigframes.bigquery.array_agg(SeriesGroupBy|DataFrameGroupby) ([#663](https://github.com/googleapis/python-bigquery-dataframes/issues/663)) ([412f28b](https://github.com/googleapis/python-bigquery-dataframes/commit/412f28bf7551430473690160a2a1c4c2f133539e))
* To_datetime supports utc=False for string inputs ([#579](https://github.com/googleapis/python-bigquery-dataframes/issues/579)) ([adf9889](https://github.com/googleapis/python-bigquery-dataframes/commit/adf98892e499f4a9c85162c38f56ca5634a1ba6d))


### Bug Fixes

* `read_gbq_table` respects primary keys even when `filters` are set ([#689](https://github.com/googleapis/python-bigquery-dataframes/issues/689)) ([9386373](https://github.com/googleapis/python-bigquery-dataframes/commit/9386373538c1e7827e2210c4fd9946312821b54d))
* Fix type error in test_cluster ([#698](https://github.com/googleapis/python-bigquery-dataframes/issues/698)) ([14d81c1](https://github.com/googleapis/python-bigquery-dataframes/commit/14d81c17505f9a09439a874ff855aec6f95fc0d1))
* Improve escaping of literals and identifiers ([#682](https://github.com/googleapis/python-bigquery-dataframes/issues/682)) ([da9b136](https://github.com/googleapis/python-bigquery-dataframes/commit/da9b136df08b243c8515946f7c0d7b591b8fcbdc))
* Properly identify non-unique index in tables without primary keys ([#699](https://github.com/googleapis/python-bigquery-dataframes/issues/699)) ([6e0f4d8](https://github.com/googleapis/python-bigquery-dataframes/commit/6e0f4d8c76f78dc26f4aa1880dd67ebdb638bb5e))
* Remove a usage of the `resource` package when not available, such as on Windows ([#681](https://github.com/googleapis/python-bigquery-dataframes/issues/681)) ([96243f2](https://github.com/googleapis/python-bigquery-dataframes/commit/96243f23a1571001509d0d01c16c1e72e47e0d23))
* The imported samples error and use peek() ([#688](https://github.com/googleapis/python-bigquery-dataframes/issues/688)) ([1a0b744](https://github.com/googleapis/python-bigquery-dataframes/commit/1a0b744c5aacdd8ba4eececf7b0a374808e8672c))


### Performance Improvements

* Don't run query immediately from `read_gbq_table` if `filters` is set ([9386373](https://github.com/googleapis/python-bigquery-dataframes/commit/9386373538c1e7827e2210c4fd9946312821b54d))
* Use a `LIMIT` clause when `max_results` is set ([9386373](https://github.com/googleapis/python-bigquery-dataframes/commit/9386373538c1e7827e2210c4fd9946312821b54d))


### Documentation

* Add code snippets for imported onnx tutorials ([#684](https://github.com/googleapis/python-bigquery-dataframes/issues/684)) ([cb36e46](https://github.com/googleapis/python-bigquery-dataframes/commit/cb36e468d1c2a34c2231638124f3c8d9052f032b))
* Add code snippets for imported tensorflow model ([#679](https://github.com/googleapis/python-bigquery-dataframes/issues/679)) ([b02c401](https://github.com/googleapis/python-bigquery-dataframes/commit/b02c401614eeab9cbf2e9a7c648b3d0a4e741b97))
* Use `class_weight="balanced"` in the  logistic regression prediction tutorial ([#678](https://github.com/googleapis/python-bigquery-dataframes/issues/678)) ([b951549](https://github.com/googleapis/python-bigquery-dataframes/commit/b95154908fd7838e499a2af0fc3760c5ab33358f))

## [1.6.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.5.0...v1.6.0) (2024-05-13)


### Features

* Add `DataFrame.__delitem__` ([#673](https://github.com/googleapis/python-bigquery-dataframes/issues/673)) ([2218c21](https://github.com/googleapis/python-bigquery-dataframes/commit/2218c21b5bb0f9e54a365ba1ada0203cbc4c9efc))
* Add `Series.case_when()` ([#673](https://github.com/googleapis/python-bigquery-dataframes/issues/673)) ([2218c21](https://github.com/googleapis/python-bigquery-dataframes/commit/2218c21b5bb0f9e54a365ba1ada0203cbc4c9efc))
* Add `strategy="quantile"` in KBinsDiscretizer ([#654](https://github.com/googleapis/python-bigquery-dataframes/issues/654)) ([c6c487f](https://github.com/googleapis/python-bigquery-dataframes/commit/c6c487fb3e39a980a05ff2dab5fb2b528d44016a))
* Add Series.combine ([#680](https://github.com/googleapis/python-bigquery-dataframes/issues/680)) ([2fd1b81](https://github.com/googleapis/python-bigquery-dataframes/commit/2fd1b8117bda0dee5d8fc0924c80ce257fa9e3f1))
* Series.str.split ([#675](https://github.com/googleapis/python-bigquery-dataframes/issues/675)) ([6eb19a7](https://github.com/googleapis/python-bigquery-dataframes/commit/6eb19a7288155b093aa7cc9bcbc710b31e7dc87a))
* Suggest correct options in bpd.options.bigquery.location ([#666](https://github.com/googleapis/python-bigquery-dataframes/issues/666)) ([57ccabc](https://github.com/googleapis/python-bigquery-dataframes/commit/57ccabcd1402b7938e2c7068e5b4880ef018f39c))
* Support `axis=1` in `df.apply` for scalar outputs ([#629](https://github.com/googleapis/python-bigquery-dataframes/issues/629)) ([f6bdc4a](https://github.com/googleapis/python-bigquery-dataframes/commit/f6bdc4aeb3f81a1e0b955521c04ac0dd22981c76))
* Support gcf vpc connector in `remote_function` ([#677](https://github.com/googleapis/python-bigquery-dataframes/issues/677)) ([9ca92d0](https://github.com/googleapis/python-bigquery-dataframes/commit/9ca92d09e9c56db408350b35ec698152c13954ed))
* Warn with a more specific `DefaultLocationWarning` category when no location can be detected ([#648](https://github.com/googleapis/python-bigquery-dataframes/issues/648)) ([e084e54](https://github.com/googleapis/python-bigquery-dataframes/commit/e084e54557addff78522bbd710637ecb4b46d23e))


### Bug Fixes

* Include `index_col` when selecting `columns` and `filters` in `read_gbq_table` ([#648](https://github.com/googleapis/python-bigquery-dataframes/issues/648)) ([e084e54](https://github.com/googleapis/python-bigquery-dataframes/commit/e084e54557addff78522bbd710637ecb4b46d23e))


### Dependencies

* Add jellyfish as a dependency for spelling correction ([57ccabc](https://github.com/googleapis/python-bigquery-dataframes/commit/57ccabcd1402b7938e2c7068e5b4880ef018f39c))


### Documentation

* Add code snippets for llm text generatiion ([#669](https://github.com/googleapis/python-bigquery-dataframes/issues/669)) ([93416ed](https://github.com/googleapis/python-bigquery-dataframes/commit/93416ed2f8353c12eb162e21e9bf155312b0ed8c))
* Add logistic regression samples ([#673](https://github.com/googleapis/python-bigquery-dataframes/issues/673)) ([2218c21](https://github.com/googleapis/python-bigquery-dataframes/commit/2218c21b5bb0f9e54a365ba1ada0203cbc4c9efc))
* Address lint errors in code samples ([#665](https://github.com/googleapis/python-bigquery-dataframes/issues/665)) ([4fc8964](https://github.com/googleapis/python-bigquery-dataframes/commit/4fc89644e47a6da9367b54826b25c6abbe97327b))
* Document inlining of small data in `read_*` APIs ([#670](https://github.com/googleapis/python-bigquery-dataframes/issues/670)) ([306953a](https://github.com/googleapis/python-bigquery-dataframes/commit/306953aaae69e57c7c2f5eefb88d55a35bdcca9d))

## [1.5.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.4.0...v1.5.0) (2024-05-07)


### Features

* `bigframes.options` and  `bigframes.option_context` now uses thread-local variables to prevent context managers in separate threads from affecting each other ([#652](https://github.com/googleapis/python-bigquery-dataframes/issues/652)) ([651fd7d](https://github.com/googleapis/python-bigquery-dataframes/commit/651fd7daf14273f172c6c55e5d6c374eb590a22d))
* Add `ARIMAPlus.coef_` property exposing `ML.ARIMA_COEFFICIENTS` functionality ([#585](https://github.com/googleapis/python-bigquery-dataframes/issues/585)) ([81d1262](https://github.com/googleapis/python-bigquery-dataframes/commit/81d1262a40c133017c6debe89506d66aab7bb0c5))
* Add a unique session_id to Session and allow cleaning up sessions ([#553](https://github.com/googleapis/python-bigquery-dataframes/issues/553)) ([c8d4e23](https://github.com/googleapis/python-bigquery-dataframes/commit/c8d4e231fe8263f5b10fae9b879ff82df58da534))
* Add the `bigframes.bigquery` sub-package with a `bigframes.bigquery.array_length` function ([#630](https://github.com/googleapis/python-bigquery-dataframes/issues/630)) ([9963f85](https://github.com/googleapis/python-bigquery-dataframes/commit/9963f85b84c3b3c681447ab79e22ac93ac48349c))
* Always do a query dry run when `option.repr_mode == "deferred"` ([#652](https://github.com/googleapis/python-bigquery-dataframes/issues/652)) ([651fd7d](https://github.com/googleapis/python-bigquery-dataframes/commit/651fd7daf14273f172c6c55e5d6c374eb590a22d))
* Custom query labels for compute options ([#638](https://github.com/googleapis/python-bigquery-dataframes/issues/638)) ([f561799](https://github.com/googleapis/python-bigquery-dataframes/commit/f5617994bc136de5caa72719b8c3c297c512cb36))
* Warn with `DefaultIndexWarning` from `read_gbq` on clustered/partitioned tables with no `index_col` or `filters` set ([#631](https://github.com/googleapis/python-bigquery-dataframes/issues/631), [#658](https://github.com/googleapis/python-bigquery-dataframes/issues/658)) ([2715d2b](https://github.com/googleapis/python-bigquery-dataframes/commit/2715d2b4a353710175a66a4f6149356f583f2c45), [73064dd](https://github.com/googleapis/python-bigquery-dataframes/commit/73064dd2aa1ece5de8f5849a0fd337d0ba677404))
* Support `index_col=False` in `read_csv` and `engine="bigquery"` ([73064dd](https://github.com/googleapis/python-bigquery-dataframes/commit/73064dd2aa1ece5de8f5849a0fd337d0ba677404))
* Support gcf max instance count in `remote_function` ([#657](https://github.com/googleapis/python-bigquery-dataframes/issues/657)) ([36578ab](https://github.com/googleapis/python-bigquery-dataframes/commit/36578ab431119f71dda746de415d0c6417bb4de2))


### Bug Fixes

* Don't raise UnknownLocationWarning for US or EU multi-regions ([#653](https://github.com/googleapis/python-bigquery-dataframes/issues/653)) ([8e4616b](https://github.com/googleapis/python-bigquery-dataframes/commit/8e4616b896f4e0d13d8bb0424c89335d3a1fe697))
* Fix bug with na in the column labels in stack ([#659](https://github.com/googleapis/python-bigquery-dataframes/issues/659)) ([4a34293](https://github.com/googleapis/python-bigquery-dataframes/commit/4a342933559fba417fe42e2bd386838defdb2778))
* Use explicit session in `PaLM2TextGenerator` ([#651](https://github.com/googleapis/python-bigquery-dataframes/issues/651)) ([e4f13c3](https://github.com/googleapis/python-bigquery-dataframes/commit/e4f13c3633b90e32d3171976d8b27ed10049882f))


### Documentation

* Add python code sample for multiple forecasting time series ([#531](https://github.com/googleapis/python-bigquery-dataframes/issues/531)) ([16866d2](https://github.com/googleapis/python-bigquery-dataframes/commit/16866d2bbd4901b1bf57f7e8cfbdb444d63fee6c))
* Fix the Palm2TextGenerator output token size ([#649](https://github.com/googleapis/python-bigquery-dataframes/issues/649)) ([c67e501](https://github.com/googleapis/python-bigquery-dataframes/commit/c67e501a4958ac097216cc1c0a9d5c1530c87ae5))

## [1.4.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.3.0...v1.4.0) (2024-04-29)


### Features

* Add .cache() method to persist intermediate dataframe ([#626](https://github.com/googleapis/python-bigquery-dataframes/issues/626)) ([a5c94ec](https://github.com/googleapis/python-bigquery-dataframes/commit/a5c94ec90dcf2c541d7d4b9558a629f935649dd2))
* Add transpose support for small homogeneously typed DataFrames. ([#621](https://github.com/googleapis/python-bigquery-dataframes/issues/621)) ([054075d](https://github.com/googleapis/python-bigquery-dataframes/commit/054075d448f7de1b3bc1a4631b4e2340643de4ef))
* Allow single input type in `remote_function` ([#641](https://github.com/googleapis/python-bigquery-dataframes/issues/641)) ([3aa643f](https://github.com/googleapis/python-bigquery-dataframes/commit/3aa643f7ab6dd0ff826ca2aafbeef29035d7c912))
* Expose gcf max timeout in `remote_function` ([#639](https://github.com/googleapis/python-bigquery-dataframes/issues/639)) ([dfeaad0](https://github.com/googleapis/python-bigquery-dataframes/commit/dfeaad0ae3b3557a9e8ccb21ddbdc55cfd611e0f))
* Series binary ops compatible with more types ([#618](https://github.com/googleapis/python-bigquery-dataframes/issues/618)) ([518d315](https://github.com/googleapis/python-bigquery-dataframes/commit/518d315487f351c227070c0127382d11381c5e88))
* Support the `score` method for `PaLM2TextGenerator` ([#634](https://github.com/googleapis/python-bigquery-dataframes/issues/634)) ([3ffc1d2](https://github.com/googleapis/python-bigquery-dataframes/commit/3ffc1d275ae110bffea2f08e63ef75b053764a0c))


### Bug Fixes

* Allow to_pandas to download more than 10GB ([#637](https://github.com/googleapis/python-bigquery-dataframes/issues/637)) ([ce56495](https://github.com/googleapis/python-bigquery-dataframes/commit/ce5649513b66c5191a56fc1fd29240b5dbe02394))
* Extend row hash to 128 bits to guarantee unique row id ([#632](https://github.com/googleapis/python-bigquery-dataframes/issues/632)) ([9005c6e](https://github.com/googleapis/python-bigquery-dataframes/commit/9005c6e79297d7130e93a0e632eb3936aa145efe))
* Llm fine tuning tests ([#627](https://github.com/googleapis/python-bigquery-dataframes/issues/627)) ([4724a1a](https://github.com/googleapis/python-bigquery-dataframes/commit/4724a1a456076d003613d2e964a8dd2d80a09ad9))
* Llm palm score tests ([#643](https://github.com/googleapis/python-bigquery-dataframes/issues/643)) ([cf4ec3a](https://github.com/googleapis/python-bigquery-dataframes/commit/cf4ec3af96c28d42e76868c6230a38511052c44e))


### Performance Improvements

* Automatically condense internal expression representation ([#516](https://github.com/googleapis/python-bigquery-dataframes/issues/516)) ([03c1b0d](https://github.com/googleapis/python-bigquery-dataframes/commit/03c1b0d8122afe9e56b480100d6207d1228ca576))
* Cache transpose to allow performant retranspose ([#635](https://github.com/googleapis/python-bigquery-dataframes/issues/635)) ([44b738d](https://github.com/googleapis/python-bigquery-dataframes/commit/44b738df07d0ee9d9ae2ced339a123f31139f887))


### Documentation

* Add supported pandas apis on the main page ([#628](https://github.com/googleapis/python-bigquery-dataframes/issues/628)) ([8d2a51c](https://github.com/googleapis/python-bigquery-dataframes/commit/8d2a51c4079844daba20f414b6c0c0ca030ba1f9))
* Add the first sample for the Single time-series forecasting from Google Analytics data tutorial ([#623](https://github.com/googleapis/python-bigquery-dataframes/issues/623)) ([2b84c4f](https://github.com/googleapis/python-bigquery-dataframes/commit/2b84c4f173e956ba2c7fcc0ad92785ae95161d8e))
* Address more technical writers' feedback ([#640](https://github.com/googleapis/python-bigquery-dataframes/issues/640)) ([1e7793c](https://github.com/googleapis/python-bigquery-dataframes/commit/1e7793cdcb56b8c0bcccc1c1ab356bac44454592))

## [1.3.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.2.0...v1.3.0) (2024-04-22)


### Features

* Add `Series.struct.dtypes` property ([#599](https://github.com/googleapis/python-bigquery-dataframes/issues/599)) ([d924ec2](https://github.com/googleapis/python-bigquery-dataframes/commit/d924ec2937c158644b5d1bbae4f82476de2c1655))
* Add fine tuning `fit()` for Palm2TextGenerator ([#616](https://github.com/googleapis/python-bigquery-dataframes/issues/616)) ([9c106bd](https://github.com/googleapis/python-bigquery-dataframes/commit/9c106bd24482620ef5ff3c85f94be9da76c49716))
* Add quantile statistic ([#613](https://github.com/googleapis/python-bigquery-dataframes/issues/613)) ([bc82804](https://github.com/googleapis/python-bigquery-dataframes/commit/bc82804da43c03c2311cd56f47a2316d3aae93d2))
* Expose `max_batching_rows` in `remote_function` ([#622](https://github.com/googleapis/python-bigquery-dataframes/issues/622)) ([240a1ac](https://github.com/googleapis/python-bigquery-dataframes/commit/240a1ac6fa914550bb6216cd5d179a36009f2657))
* Support primary key(s) in `read_gbq` by using as the `index_col` by default ([#625](https://github.com/googleapis/python-bigquery-dataframes/issues/625)) ([75bb240](https://github.com/googleapis/python-bigquery-dataframes/commit/75bb2409532e80de742030d05ffcbacacf5ffba2))
* Warn if location is set to unknown location ([#609](https://github.com/googleapis/python-bigquery-dataframes/issues/609)) ([3706b4f](https://github.com/googleapis/python-bigquery-dataframes/commit/3706b4f9dde65788b5e6343a6428fb1866499461))


### Bug Fixes

* Address technical writers fb ([#611](https://github.com/googleapis/python-bigquery-dataframes/issues/611)) ([9f8f181](https://github.com/googleapis/python-bigquery-dataframes/commit/9f8f181279133abdb7da3aa045df6fa278587013))
* Infer narrowest numeric type when combining numeric columns ([#602](https://github.com/googleapis/python-bigquery-dataframes/issues/602)) ([8f9ece6](https://github.com/googleapis/python-bigquery-dataframes/commit/8f9ece6d13f57f02d677bf0e3fea97dea94ae240))
* Use exact median implementation by default ([#619](https://github.com/googleapis/python-bigquery-dataframes/issues/619)) ([9d205ae](https://github.com/googleapis/python-bigquery-dataframes/commit/9d205aecb77f35baeec82a8f6e1b72c2d852ca46))


### Documentation

* Fix rendering of examples for multiple apis ([#620](https://github.com/googleapis/python-bigquery-dataframes/issues/620)) ([9665e39](https://github.com/googleapis/python-bigquery-dataframes/commit/9665e39ef288841f03a9d823bd2210ef58394ad3))
* Set `index_cols` in `read_gbq` as a best practice ([#624](https://github.com/googleapis/python-bigquery-dataframes/issues/624)) ([70015b7](https://github.com/googleapis/python-bigquery-dataframes/commit/70015b79e8cff16ff1b36c5e3f019fe099750a9d))

## [1.2.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.1.0...v1.2.0) (2024-04-15)


### Features

* Add hasnans, combine_first, update to Series ([#600](https://github.com/googleapis/python-bigquery-dataframes/issues/600)) ([86e0f38](https://github.com/googleapis/python-bigquery-dataframes/commit/86e0f38adc71d76e09dd832e5e33cb7c1aab02ac))
* Add MultiIndex subclass. ([#596](https://github.com/googleapis/python-bigquery-dataframes/issues/596)) ([5d0f149](https://github.com/googleapis/python-bigquery-dataframes/commit/5d0f149dce5425098fcd154d96a302c1661ce5d3))
* Add pivot_table for DataFrame. ([#473](https://github.com/googleapis/python-bigquery-dataframes/issues/473)) ([5f1d670](https://github.com/googleapis/python-bigquery-dataframes/commit/5f1d670e6b839a30acdb495a05011c2ce4e0c7a4))
* Add Series.autocorr ([#605](https://github.com/googleapis/python-bigquery-dataframes/issues/605)) ([4ec8034](https://github.com/googleapis/python-bigquery-dataframes/commit/4ec80340459e675b82b437f6c48b2872d362bafe))
* Support list of numerics in pandas.cut ([#580](https://github.com/googleapis/python-bigquery-dataframes/issues/580)) ([290f95d](https://github.com/googleapis/python-bigquery-dataframes/commit/290f95dc5198f9ab7cd9d726d40af704250c0449))


### Bug Fixes

* Address more technical writers feedback ([#581](https://github.com/googleapis/python-bigquery-dataframes/issues/581)) ([4b08d92](https://github.com/googleapis/python-bigquery-dataframes/commit/4b08d9243272229f71688152dbeb69d0ab7c68b4))
* Error for object dtype on read_pandas ([#570](https://github.com/googleapis/python-bigquery-dataframes/issues/570)) ([8702dcf](https://github.com/googleapis/python-bigquery-dataframes/commit/8702dcf54c0f2073e21df42eaef51927481da421))
* Inverting int now does bitwise inversion rather than sign flip ([#574](https://github.com/googleapis/python-bigquery-dataframes/issues/574)) ([5f1db8b](https://github.com/googleapis/python-bigquery-dataframes/commit/5f1db8b270b32ab366be3690761da137d9fe65f5))
* Loc setitem dtype issue. ([#603](https://github.com/googleapis/python-bigquery-dataframes/issues/603)) ([b94bae9](https://github.com/googleapis/python-bigquery-dataframes/commit/b94bae9892e0fa79dc4bde0f4f1427d00accda6d))
* Toc menu missing plotting name ([#591](https://github.com/googleapis/python-bigquery-dataframes/issues/591)) ([eed12c1](https://github.com/googleapis/python-bigquery-dataframes/commit/eed12c181ff8724333b1c426a0eb442c627528b8))


### Documentation

* (Series|Dataframe).dtypes ([#598](https://github.com/googleapis/python-bigquery-dataframes/issues/598)) ([edef48f](https://github.com/googleapis/python-bigquery-dataframes/commit/edef48f7a93e19bc1f6d37fb041dfd6314d881d5))
* Add code samples for `str` accessor methdos ([#594](https://github.com/googleapis/python-bigquery-dataframes/issues/594)) ([a557ea2](https://github.com/googleapis/python-bigquery-dataframes/commit/a557ea2b64633932f730b56688f76806da6195fb))
* Add docs for `DataFrame` and `Series` dunder methods ([#562](https://github.com/googleapis/python-bigquery-dataframes/issues/562)) ([8fc26c4](https://github.com/googleapis/python-bigquery-dataframes/commit/8fc26c424b29a8b78542372e402fcc4e8fface7b))
* Add examples for at/iat ([#582](https://github.com/googleapis/python-bigquery-dataframes/issues/582)) ([3be4a2e](https://github.com/googleapis/python-bigquery-dataframes/commit/3be4a2e784e046ca9a1fac8d386d072537b6c4de))

## [1.1.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v1.0.0...v1.1.0) (2024-04-04)


### Features

* (Series|DataFrame).explode ([#556](https://github.com/googleapis/python-bigquery-dataframes/issues/556)) ([9e32f57](https://github.com/googleapis/python-bigquery-dataframes/commit/9e32f570b42c8ddae0c9b281b25beff91f0c922c))
* Add `DataFrame.eval` and `DataFrame.query` ([#361](https://github.com/googleapis/python-bigquery-dataframes/issues/361)) ([5e28ebd](https://github.com/googleapis/python-bigquery-dataframes/commit/5e28ebd1ba3a5559e093c2ea676c0714c1434ba9))
* Add ColumnTransformer save/load ([#541](https://github.com/googleapis/python-bigquery-dataframes/issues/541)) ([9d8cf67](https://github.com/googleapis/python-bigquery-dataframes/commit/9d8cf6792a8dbe03e03b102c454d15fcde7986af))
* Add ml.metrics.mean_squared_error ([#559](https://github.com/googleapis/python-bigquery-dataframes/issues/559)) ([853c25e](https://github.com/googleapis/python-bigquery-dataframes/commit/853c25e8023bf877f28cda4dade0694d0299a83e))
* Add support for numpy expm1, log1p, floor, ceil, arctan2 ops ([#505](https://github.com/googleapis/python-bigquery-dataframes/issues/505)) ([e8e66cf](https://github.com/googleapis/python-bigquery-dataframes/commit/e8e66cf25887f64d2a7cb26081c2ef3cea10827d))
* Add transformers save/load ([#552](https://github.com/googleapis/python-bigquery-dataframes/issues/552)) ([d805241](https://github.com/googleapis/python-bigquery-dataframes/commit/d805241b7ec99fcb7579dce778d4b04778a72002))
* Allow DataFrame binary ops to align on either axis and with loc… ([#544](https://github.com/googleapis/python-bigquery-dataframes/issues/544)) ([6d8f3af](https://github.com/googleapis/python-bigquery-dataframes/commit/6d8f3afe28d39eb15b969f50d37c58a2c3ff1967))
* Expose `DataFrame.bqclient` to assist in integrations ([#519](https://github.com/googleapis/python-bigquery-dataframes/issues/519)) ([0be8911](https://github.com/googleapis/python-bigquery-dataframes/commit/0be891191ed89be77494e4dcda30fb37836842ac))
* Read_pandas accepts pandas Series and Index objects ([#573](https://github.com/googleapis/python-bigquery-dataframes/issues/573)) ([f8821fe](https://github.com/googleapis/python-bigquery-dataframes/commit/f8821fe7ecf8a80532a6aab98044fad601ff939c))
* Support `ML.GENERATE_EMBEDDING` in `PaLM2TextEmbeddingGenerator` ([#539](https://github.com/googleapis/python-bigquery-dataframes/issues/539)) ([1156c1e](https://github.com/googleapis/python-bigquery-dataframes/commit/1156c1e3ce8c1e62898dbe68ccd6c5ab3cd4068f))
* Support max_columns in repr and make repr more efficient ([#515](https://github.com/googleapis/python-bigquery-dataframes/issues/515)) ([54e49cf](https://github.com/googleapis/python-bigquery-dataframes/commit/54e49cff89bd329852a823cd5cf5c5b41b7f9e32))


### Bug Fixes

* Assign NaN scalar to column error. ([#513](https://github.com/googleapis/python-bigquery-dataframes/issues/513)) ([0a4153c](https://github.com/googleapis/python-bigquery-dataframes/commit/0a4153cc71a44c09b8d691897f1e5afa58c69f25))
* Don't download 100gb onto local python machine in load test ([#537](https://github.com/googleapis/python-bigquery-dataframes/issues/537)) ([082c58b](https://github.com/googleapis/python-bigquery-dataframes/commit/082c58bbe76821b90337dc5af0ab5fa7515682c2))
* Exclude list-like s parameter in plot.scatter ([#568](https://github.com/googleapis/python-bigquery-dataframes/issues/568)) ([1caac27](https://github.com/googleapis/python-bigquery-dataframes/commit/1caac27fe95ef3eb36bad2ac351090891922858c))
* Fix case where df.peek would fail to execute even with force=True ([#511](https://github.com/googleapis/python-bigquery-dataframes/issues/511)) ([8eca99a](https://github.com/googleapis/python-bigquery-dataframes/commit/8eca99a03bc4bdaccf15a979b5382f3659f2aac5))
* Fix error in `Series.drop(0)` ([#575](https://github.com/googleapis/python-bigquery-dataframes/issues/575)) ([75dd786](https://github.com/googleapis/python-bigquery-dataframes/commit/75dd7862e60502c97f7defe5dfefb044ea74bae8))
* Include all names in MultiIndex repr ([#564](https://github.com/googleapis/python-bigquery-dataframes/issues/564)) ([b188146](https://github.com/googleapis/python-bigquery-dataframes/commit/b188146466780e6f7a041f51f5be51a7d60719c9))
* Plot.scatter s parameter cannot accept float-like column ([#563](https://github.com/googleapis/python-bigquery-dataframes/issues/563)) ([8d39187](https://github.com/googleapis/python-bigquery-dataframes/commit/8d3918761a17649180aa806d7b01aa103f69b4fe))
* Product operation produces float result for all input types ([#501](https://github.com/googleapis/python-bigquery-dataframes/issues/501)) ([6873b30](https://github.com/googleapis/python-bigquery-dataframes/commit/6873b30b691a11a368308825a72013d8ec1408ed))
* Reloaded transformer .transform error ([#569](https://github.com/googleapis/python-bigquery-dataframes/issues/569)) ([39fe474](https://github.com/googleapis/python-bigquery-dataframes/commit/39fe47451d24a8cf55d7dbb15c6d3b176d25ab18))
* Rename PaLM2TextEmbeddingGenerator.predict output columns to be backward compatible ([#561](https://github.com/googleapis/python-bigquery-dataframes/issues/561)) ([4995c00](https://github.com/googleapis/python-bigquery-dataframes/commit/4995c0046265463bc5c502cbeb34c7632d5a255e))
* Respect hard stack size limit and swallow limit change exception. ([#558](https://github.com/googleapis/python-bigquery-dataframes/issues/558)) ([4833908](https://github.com/googleapis/python-bigquery-dataframes/commit/483390830ae0ee2fe0fb47dc7d2aea143b2dc7d8))
* Restore string to date/time type coercion ([#565](https://github.com/googleapis/python-bigquery-dataframes/issues/565)) ([4ae0262](https://github.com/googleapis/python-bigquery-dataframes/commit/4ae0262a2b1dfc35c1e4c3392b9e21456d6e964e))
* Sync the notebook with embedding changes ([#550](https://github.com/googleapis/python-bigquery-dataframes/issues/550)) ([347f2dd](https://github.com/googleapis/python-bigquery-dataframes/commit/347f2dda2298e17cd44a298f04a723f2d20c080a))
* Use bytes limit on frame inlining rather than element count ([#576](https://github.com/googleapis/python-bigquery-dataframes/issues/576)) ([659a161](https://github.com/googleapis/python-bigquery-dataframes/commit/659a161a53e93f66334cd04d1c3dc1f1f47ecc16))


### Performance Improvements

* Add multi-query execution capability for complex dataframes ([#427](https://github.com/googleapis/python-bigquery-dataframes/issues/427)) ([d2d7e33](https://github.com/googleapis/python-bigquery-dataframes/commit/d2d7e33b1f8b4e184ef3e76eedbd673a8fcee60e))


### Dependencies

* Include `pyarrow` as a dependency ([#529](https://github.com/googleapis/python-bigquery-dataframes/issues/529)) ([9b1525a](https://github.com/googleapis/python-bigquery-dataframes/commit/9b1525a0c359455160bfbc0dc1366e37982ad01f))


### Documentation

* `bigframes.options.bigquery.project` and `location` are optional in some circumstances ([#548](https://github.com/googleapis/python-bigquery-dataframes/issues/548)) ([90bcec5](https://github.com/googleapis/python-bigquery-dataframes/commit/90bcec5c73f7eefeff14bbd8bdcad3a4c9d91d8f))
* Add "Supported pandas APIs" reference to the documentation ([#542](https://github.com/googleapis/python-bigquery-dataframes/issues/542)) ([74c3915](https://github.com/googleapis/python-bigquery-dataframes/commit/74c391586280b55c35d66c697167122d72c13386))
* Add General Availability banner to README ([#507](https://github.com/googleapis/python-bigquery-dataframes/issues/507)) ([262ff59](https://github.com/googleapis/python-bigquery-dataframes/commit/262ff5922643039e037bd9b6c0a91b5bd20a4e08))
* Add opeartions in API docs ([#557](https://github.com/googleapis/python-bigquery-dataframes/issues/557)) ([ea95761](https://github.com/googleapis/python-bigquery-dataframes/commit/ea9576125d46f3912372f75ebe51196ba83e96db))
* Add progress_bar code sample ([#508](https://github.com/googleapis/python-bigquery-dataframes/issues/508)) ([92a1af3](https://github.com/googleapis/python-bigquery-dataframes/commit/92a1af35b8de4afb6cdb5b5e89facdceb5c151d2))
* Add the code samples for metrics{auc, roc_auc_score, roc_curve} ([#520](https://github.com/googleapis/python-bigquery-dataframes/issues/520)) ([5f37b09](https://github.com/googleapis/python-bigquery-dataframes/commit/5f37b0902fae2c099207acf3ce2e251c09ac889d))
* Address more comments from technical writers to meet legal purposes ([#571](https://github.com/googleapis/python-bigquery-dataframes/issues/571)) ([9084df3](https://github.com/googleapis/python-bigquery-dataframes/commit/9084df369bc6819edf5f57ceba85667a14371ac5))
* Fix docs of ARIMAPlus.predict ([#512](https://github.com/googleapis/python-bigquery-dataframes/issues/512)) ([3b80f95](https://github.com/googleapis/python-bigquery-dataframes/commit/3b80f956755c9d7043138aab6e5687cba50be8cb))
* Include Index in table-of-contents ([#564](https://github.com/googleapis/python-bigquery-dataframes/issues/564)) ([b188146](https://github.com/googleapis/python-bigquery-dataframes/commit/b188146466780e6f7a041f51f5be51a7d60719c9))
* Mark Gemini model as Pre-GA ([#543](https://github.com/googleapis/python-bigquery-dataframes/issues/543)) ([769868b](https://github.com/googleapis/python-bigquery-dataframes/commit/769868b9fc7dfff2e7b1ed5cec52a5dd3dfd6ff2))
* Migrate the overview page to Bigframes official landing page ([#536](https://github.com/googleapis/python-bigquery-dataframes/issues/536)) ([a0fb8bb](https://github.com/googleapis/python-bigquery-dataframes/commit/a0fb8bbfddd07f1e0ef03eeb4be653d1e9f06772))

## [1.0.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.26.0...v1.0.0) (2024-03-25)


### ⚠ BREAKING CHANGES

* rename model parameter `min_rel_progress` to `tol`
* `early_stop` setting no longer supported, always uses `True`
* rename model parameter `n_parallell_trees` to `n_estimators`
* rename `class_weights` to `class_weight`
* rename `learn_rate` to `learning_rate`
* PCA `n_components` supports float value and `None`, default to `None`
* rename various ml model parameters for consistency with sklearn (https://github.com/googleapis/python-bigquery-dataframes/pull/491)

### Features

* Add configuration option to read_gbq ([#401](https://github.com/googleapis/python-bigquery-dataframes/issues/401)) ([85cede2](https://github.com/googleapis/python-bigquery-dataframes/commit/85cede22587a9fe1dae888721492f9390dc46d70))
* Add ml ARIMAPlus model params ([#488](https://github.com/googleapis/python-bigquery-dataframes/issues/488)) ([352cb85](https://github.com/googleapis/python-bigquery-dataframes/commit/352cb850d23e41a2278edf0df584b89ee9619aab))
* Add ml KMeans model params ([#477](https://github.com/googleapis/python-bigquery-dataframes/issues/477)) ([23a8d9a](https://github.com/googleapis/python-bigquery-dataframes/commit/23a8d9a32e1619aff92c8dfabb7bcdd54c314bd5))
* Add ml LogisticRegression model params ([#481](https://github.com/googleapis/python-bigquery-dataframes/issues/481)) ([f959b65](https://github.com/googleapis/python-bigquery-dataframes/commit/f959b653a0e82b5bfd21f9e994031cf6d25c281a))
* Add ml PCA model params ([#474](https://github.com/googleapis/python-bigquery-dataframes/issues/474)) ([fb5d83b](https://github.com/googleapis/python-bigquery-dataframes/commit/fb5d83b1e35c465cff486e6cf7862e5b32e3c65a))
* Add params for LinearRegression model ([#464](https://github.com/googleapis/python-bigquery-dataframes/issues/464)) ([21b2188](https://github.com/googleapis/python-bigquery-dataframes/commit/21b2188cd0ca85485b5171ee9e46da4c924e2ff8))
* Add support for Python 3.12 ([#231](https://github.com/googleapis/python-bigquery-dataframes/issues/231)) ([df2976f](https://github.com/googleapis/python-bigquery-dataframes/commit/df2976fa9fd0319b824128d0ccf2ebb20f381caa))
* Allow assigning directly to Series.name property ([#495](https://github.com/googleapis/python-bigquery-dataframes/issues/495)) ([ad0e99e](https://github.com/googleapis/python-bigquery-dataframes/commit/ad0e99eddb1dddd3d439cea7db1e4f222b45c6b9))
* Ensure `Series.str.len()` can get length of array columns ([#497](https://github.com/googleapis/python-bigquery-dataframes/issues/497)) ([10c0446](https://github.com/googleapis/python-bigquery-dataframes/commit/10c044686228e5c6f3868c1eb10454f6a086ac8b))
* Option to use bq connection without check ([#460](https://github.com/googleapis/python-bigquery-dataframes/issues/460)) ([0b3f8e5](https://github.com/googleapis/python-bigquery-dataframes/commit/0b3f8e5ce63f75ba99ee8cf29226a0fd38bef99f))
* PCA `n_components` supports float value and `None`, default to `None` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Rename `class_weights` to `class_weight` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Rename `learn_rate` to `learning_rate` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Rename model parameter `min_rel_progress` to `tol` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Rename model parameter `n_parallell_trees` to `n_estimators` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Rename various ml model parameters for consistency with sklearn (https://github.com/googleapis/python-bigquery-dataframes/pull/491) ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Support BQ regional endpoints for europe-west9, europe-west3, us-east4, and us-west1 ([#504](https://github.com/googleapis/python-bigquery-dataframes/issues/504)) ([fbada4a](https://github.com/googleapis/python-bigquery-dataframes/commit/fbada4a70688c5d13fa35d1843b0c4252c5ced72))
* Support dataframe.cov ([#498](https://github.com/googleapis/python-bigquery-dataframes/issues/498)) ([c4beafd](https://github.com/googleapis/python-bigquery-dataframes/commit/c4beafdf0c1ba88b306ca96fa3ca46b86debaa4c))
* Support Series.dt.floor ([#493](https://github.com/googleapis/python-bigquery-dataframes/issues/493)) ([2dd01c2](https://github.com/googleapis/python-bigquery-dataframes/commit/2dd01c25e9f01c03979c61e71d3c5cd9f0bd4c96))
* Support Series.dt.normalize ([#483](https://github.com/googleapis/python-bigquery-dataframes/issues/483)) ([0bf1e91](https://github.com/googleapis/python-bigquery-dataframes/commit/0bf1e916c2b636ec02ac010190e89d38e88fce4b))
* Update plot sample to 1000 rows ([#458](https://github.com/googleapis/python-bigquery-dataframes/issues/458)) ([60d4a7b](https://github.com/googleapis/python-bigquery-dataframes/commit/60d4a7bbac867256f8bbfd3053c7dd2645c1b062))


### Bug Fixes

* `early_stop` setting no longer supported, always uses `True` ([65c6f47](https://github.com/googleapis/python-bigquery-dataframes/commit/65c6f4736d1a5552835e4cec8b777b2c0f3dd8da))
* Fix -1 offset lookups failing ([#463](https://github.com/googleapis/python-bigquery-dataframes/issues/463)) ([2dfb9c2](https://github.com/googleapis/python-bigquery-dataframes/commit/2dfb9c24d07841d785e41b33573c5f3a218efeea))
* Plot.scatter `c` argument functionalities ([#494](https://github.com/googleapis/python-bigquery-dataframes/issues/494)) ([d6ee994](https://github.com/googleapis/python-bigquery-dataframes/commit/d6ee994c17e0b1dd6768b09ee81d2c902f601b76))
* Properly support format param for numerical input. ([#486](https://github.com/googleapis/python-bigquery-dataframes/issues/486)) ([ae20c35](https://github.com/googleapis/python-bigquery-dataframes/commit/ae20c3583d5526777548b5d594ecca6034bb49ec))
* Renable to_csv and to_json related tests ([#468](https://github.com/googleapis/python-bigquery-dataframes/issues/468)) ([2b9a01d](https://github.com/googleapis/python-bigquery-dataframes/commit/2b9a01de0adb8d41fbe73ce94b1acc8d22f507b5))
* Sampling plot cannot preserve ordering if index is not ordered ([#475](https://github.com/googleapis/python-bigquery-dataframes/issues/475)) ([a5345fe](https://github.com/googleapis/python-bigquery-dataframes/commit/a5345fe8943667a89fcba48ce31aa8ecfc283f92))
* Use actual BigQuery types rather than ibis types in to_pandas ([#500](https://github.com/googleapis/python-bigquery-dataframes/issues/500)) ([82b4f91](https://github.com/googleapis/python-bigquery-dataframes/commit/82b4f91db365fe06d8bd0bf938f880a48091104e))


### Dependencies

* Support pandas 2.2 ([#492](https://github.com/googleapis/python-bigquery-dataframes/issues/492)) ([e2cf50e](https://github.com/googleapis/python-bigquery-dataframes/commit/e2cf50e053f7163d1654c4b5621cc93e922d5148))


### Documentation

* Add code samples for metrics.{accuracy_score, confusion_matrix} ([#478](https://github.com/googleapis/python-bigquery-dataframes/issues/478)) ([3e3329a](https://github.com/googleapis/python-bigquery-dataframes/commit/3e3329a37c1020bd3e6d4d5e980103c63ab0c337))
* Add code samples for metrics.{recall_score, precision_score, f11_score} ([#502](https://github.com/googleapis/python-bigquery-dataframes/issues/502)) ([370fe90](https://github.com/googleapis/python-bigquery-dataframes/commit/370fe9087848862d02f0e5a333fcb4cd37cf5ca0))
* Improve API documentation ([#489](https://github.com/googleapis/python-bigquery-dataframes/issues/489)) ([751266e](https://github.com/googleapis/python-bigquery-dataframes/commit/751266e056ac566ef5b6e40fbbca84ed95e7a7a9))
* Update bigquery connection documentation ([#499](https://github.com/googleapis/python-bigquery-dataframes/issues/499)) ([4bfe094](https://github.com/googleapis/python-bigquery-dataframes/commit/4bfe094fdf2f7e1af72cc939558713a499760129))
* Update LLM + K-means notebook to handle partial failures ([#496](https://github.com/googleapis/python-bigquery-dataframes/issues/496)) ([97afad9](https://github.com/googleapis/python-bigquery-dataframes/commit/97afad96f80c1815db8ad34f0ff62095631036c2))

## [0.26.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.25.0...v0.26.0) (2024-03-20)


### ⚠ BREAKING CHANGES

* exclude remote models for .register() ([#465](https://github.com/googleapis/python-bigquery-dataframes/issues/465))

### Features

* (Series|DataFrame).plot ([#438](https://github.com/googleapis/python-bigquery-dataframes/issues/438)) ([1c3e668](https://github.com/googleapis/python-bigquery-dataframes/commit/1c3e668ceb26fd0f1377acbf6b95e8f4bcef40d6))
* `read_gbq_table` supports `LIKE` as a operator in `filters` ([#454](https://github.com/googleapis/python-bigquery-dataframes/issues/454)) ([d2d425a](https://github.com/googleapis/python-bigquery-dataframes/commit/d2d425a93aa9e96f3b71c3ca3b185f4b5eaf32ef))
* Add DataFrame.pipe() method ([#421](https://github.com/googleapis/python-bigquery-dataframes/issues/421)) ([95f5a6e](https://github.com/googleapis/python-bigquery-dataframes/commit/95f5a6e749468743af65062e559bc35ac56f3c24))
* Set `force=True` by default in `DataFrame.peek()` ([#469](https://github.com/googleapis/python-bigquery-dataframes/issues/469)) ([4e8e97d](https://github.com/googleapis/python-bigquery-dataframes/commit/4e8e97d661078ed38d77be93b0bc1ad0fd52949c))
* Support datetime related casting in (Series|DataFrame|Index).astype ([#442](https://github.com/googleapis/python-bigquery-dataframes/issues/442)) ([fde339b](https://github.com/googleapis/python-bigquery-dataframes/commit/fde339b71c754e617c61052940215b77890b59e4))
* Support Series.dt.strftime ([#453](https://github.com/googleapis/python-bigquery-dataframes/issues/453)) ([8f6e955](https://github.com/googleapis/python-bigquery-dataframes/commit/8f6e955fc946db97c95ea012659432355b0cd12c))


### Bug Fixes

* Any() on empty set now correctly returns False ([#471](https://github.com/googleapis/python-bigquery-dataframes/issues/471)) ([f55680c](https://github.com/googleapis/python-bigquery-dataframes/commit/f55680cd0eed46ee06cd9baf658de792f4a27f31))
* Df.drop_na preserves columns dtype ([#457](https://github.com/googleapis/python-bigquery-dataframes/issues/457)) ([3bab1a9](https://github.com/googleapis/python-bigquery-dataframes/commit/3bab1a917a5833bd58b20071a229ee95cf86a251))
* Disable to_json and to_csv related tests ([#462](https://github.com/googleapis/python-bigquery-dataframes/issues/462)) ([874026d](https://github.com/googleapis/python-bigquery-dataframes/commit/874026da612bf08fbaf6d7dbfaa3325dc8a61500))
* Exclude remote models for .register() ([#465](https://github.com/googleapis/python-bigquery-dataframes/issues/465)) ([73fe0f8](https://github.com/googleapis/python-bigquery-dataframes/commit/73fe0f89a96557afc4225521654978b96a2291b3))
* Fix broken link in covid notebook ([#450](https://github.com/googleapis/python-bigquery-dataframes/issues/450)) ([adadb06](https://github.com/googleapis/python-bigquery-dataframes/commit/adadb0658c35142fed228abbd9baa42f9372f44b))
* Fix broken multiindex loc cases ([#467](https://github.com/googleapis/python-bigquery-dataframes/issues/467)) ([b519197](https://github.com/googleapis/python-bigquery-dataframes/commit/b519197d51cc098ac4981a9a57a9d6988ba07d03))
* Fix grouping series on multiple other series ([#455](https://github.com/googleapis/python-bigquery-dataframes/issues/455)) ([3971bd2](https://github.com/googleapis/python-bigquery-dataframes/commit/3971bd27c96b68b859399564dbb6abdb93de5f14))
* Groupby aggregates no longer check if grouping keys are numeric ([#472](https://github.com/googleapis/python-bigquery-dataframes/issues/472)) ([4fbf938](https://github.com/googleapis/python-bigquery-dataframes/commit/4fbf938c200a3e0e6b592aa4a4e18b59f2f34082))
* Raise `ValueError` when `read_pandas()` receives a bigframes `DataFrame` ([#447](https://github.com/googleapis/python-bigquery-dataframes/issues/447)) ([b28f9fd](https://github.com/googleapis/python-bigquery-dataframes/commit/b28f9fdd9681b3c9783a6e52322b70093e0283ec))
* Series.(to_csv|to_json) leverages bq export ([#452](https://github.com/googleapis/python-bigquery-dataframes/issues/452)) ([718a00c](https://github.com/googleapis/python-bigquery-dataframes/commit/718a00c1fa8ac44b0d3a79a2217e5b12690785fb))
* Warn when `read_gbq` / `read_gbq_table` uses the snapshot time cache ([#441](https://github.com/googleapis/python-bigquery-dataframes/issues/441)) ([e16a8c0](https://github.com/googleapis/python-bigquery-dataframes/commit/e16a8c0a6fb46cf1a7be12eec9471ae95d6f2c44))


### Documentation

* Add code samples for `ml.metrics.r2_score` ([#459](https://github.com/googleapis/python-bigquery-dataframes/issues/459)) ([85fefa2](https://github.com/googleapis/python-bigquery-dataframes/commit/85fefa2f1d4dbe3e0c9d4ab8124cea88eb5df38f))
* Add the docs for loc and iloc indexers ([#446](https://github.com/googleapis/python-bigquery-dataframes/issues/446)) ([14ab8d8](https://github.com/googleapis/python-bigquery-dataframes/commit/14ab8d834d793ac7644f066145912e6d50966881))
* Add the pages for at and iat indexers ([#456](https://github.com/googleapis/python-bigquery-dataframes/issues/456)) ([340f0b5](https://github.com/googleapis/python-bigquery-dataframes/commit/340f0b5b41fc5150d73890c7f27ae68dc308e160))
* Add version information to bug template ([#437](https://github.com/googleapis/python-bigquery-dataframes/issues/437)) ([91bd39e](https://github.com/googleapis/python-bigquery-dataframes/commit/91bd39e8b194ddad09d53fca96201eee58063bb9))
* Indicate that project and location are optional in example notebooks ([#451](https://github.com/googleapis/python-bigquery-dataframes/issues/451)) ([1df0140](https://github.com/googleapis/python-bigquery-dataframes/commit/1df014010652e7827a2720a906d0afe482a30ca9))

## [0.25.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.24.0...v0.25.0) (2024-03-14)


### Features

* (Series|DataFrame).plot.(line|area|scatter) ([#431](https://github.com/googleapis/python-bigquery-dataframes/issues/431)) ([0772510](https://github.com/googleapis/python-bigquery-dataframes/commit/077251084e3121019c56e5d6c16aebab16be8dc7))
* Support CMEK for `remote_function` cloud functions ([#430](https://github.com/googleapis/python-bigquery-dataframes/issues/430)) ([2fd69f4](https://github.com/googleapis/python-bigquery-dataframes/commit/2fd69f4bed143fc8c040dac1c55288c1cb660f6e))

## [0.24.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.23.0...v0.24.0) (2024-03-12)


### ⚠ BREAKING CHANGES

* `read_parquet` uses a "pandas" engine to parse files by default. Use `engine="bigquery"` for the previous behavior

### Features

* (Series|Dataframe).plot.hist() ([#420](https://github.com/googleapis/python-bigquery-dataframes/issues/420)) ([4aadff4](https://github.com/googleapis/python-bigquery-dataframes/commit/4aadff4db59243b4510a874fef2bdb17402d1674))
* Add detect_anomalies to ml ARIMAPlus and KMeans models ([#426](https://github.com/googleapis/python-bigquery-dataframes/issues/426)) ([6df28ed](https://github.com/googleapis/python-bigquery-dataframes/commit/6df28ed704552ebec7869e1f2034614cb6407098))
* Add engine parameter to `read_parquet` ([#413](https://github.com/googleapis/python-bigquery-dataframes/issues/413)) ([31325a1](https://github.com/googleapis/python-bigquery-dataframes/commit/31325a190320bf01ced53d9f4cdb94462daaa06b))
* Add ml PCA.detect_anomalies method ([#422](https://github.com/googleapis/python-bigquery-dataframes/issues/422)) ([8d82945](https://github.com/googleapis/python-bigquery-dataframes/commit/8d8294544ac7fedaca753c5473e3ca2a27868420))
* Support BYOSA in `remote_function` ([#407](https://github.com/googleapis/python-bigquery-dataframes/issues/407)) ([d92ced2](https://github.com/googleapis/python-bigquery-dataframes/commit/d92ced2adaa30a0405ace9ca6cd70a8e217f13d0))
* Support CMEK for BQ tables ([#403](https://github.com/googleapis/python-bigquery-dataframes/issues/403)) ([9a678e3](https://github.com/googleapis/python-bigquery-dataframes/commit/9a678e35201d935e1d93875429005033cfe7cff6))


### Bug Fixes

* Move `third_party.bigframes_vendored` to `bigframes_vendored` ([#424](https://github.com/googleapis/python-bigquery-dataframes/issues/424)) ([763edeb](https://github.com/googleapis/python-bigquery-dataframes/commit/763edeb4f4e8bc4b8bb05a992dae80c49c245e25))
* Only do row identity based joins when joining by index ([#356](https://github.com/googleapis/python-bigquery-dataframes/issues/356)) ([76b252f](https://github.com/googleapis/python-bigquery-dataframes/commit/76b252f907055d72556e3e95f6cb5ee41de5b1c2))
* Read_pandas inline respects location ([#412](https://github.com/googleapis/python-bigquery-dataframes/issues/412)) ([ae0e3ea](https://github.com/googleapis/python-bigquery-dataframes/commit/ae0e3eaca49171fd449de4d43ddc3e3ce9fdc2ce))


### Documentation

* Add predict sample to samples/snippets/bqml_getting_started_test.py ([#388](https://github.com/googleapis/python-bigquery-dataframes/issues/388)) ([6a3b0cc](https://github.com/googleapis/python-bigquery-dataframes/commit/6a3b0cc7f84120fc5978ce11b6b7c55e89654304))
* Document minimum IAM requirement ([#416](https://github.com/googleapis/python-bigquery-dataframes/issues/416)) ([36173b0](https://github.com/googleapis/python-bigquery-dataframes/commit/36173b0c14747fb52909bbedd93249024bae9ac1))
* Fix the note rendering for DataFrames methods: nlargest, nsmallest ([#417](https://github.com/googleapis/python-bigquery-dataframes/issues/417)) ([38bd2ba](https://github.com/googleapis/python-bigquery-dataframes/commit/38bd2ba21bc1a3222635de22eecd97930bf5b1de))

## [0.23.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.22.0...v0.23.0) (2024-03-05)


### Features

* Add ml.metrics.pairwise.euclidean_distance ([#397](https://github.com/googleapis/python-bigquery-dataframes/issues/397)) ([1726588](https://github.com/googleapis/python-bigquery-dataframes/commit/1726588beb8894bc08c272d718ca8e3a9451d0c2))
* Add TextEmbedding model version support ([#394](https://github.com/googleapis/python-bigquery-dataframes/issues/394)) ([e0f1ab0](https://github.com/googleapis/python-bigquery-dataframes/commit/e0f1ab07cbc81034e24767baff54560561950e67))


### Bug Fixes

* Code exception in `remote_function` now prevents retry and surfaces in the client ([#387](https://github.com/googleapis/python-bigquery-dataframes/issues/387)) ([dd3643d](https://github.com/googleapis/python-bigquery-dataframes/commit/dd3643d3733ca1c2a18352bafac7d32fbdfa2a25))
* Docs link for metrics.pairwise ([#400](https://github.com/googleapis/python-bigquery-dataframes/issues/400)) ([a60aba7](https://github.com/googleapis/python-bigquery-dataframes/commit/a60aba712576e2e4e14cfcfffe9349d6972716a5))


### Dependencies

* Update ibis to version 8.0.0 and refactor `remote_function` to use ibis UDF method ([#277](https://github.com/googleapis/python-bigquery-dataframes/issues/277)) ([350499b](https://github.com/googleapis/python-bigquery-dataframes/commit/350499bccb62e22169ab2f2e1400175b2179ef85))


### Documentation

* Update README to point to new summary pages ([#402](https://github.com/googleapis/python-bigquery-dataframes/issues/402)) ([bfe2b23](https://github.com/googleapis/python-bigquery-dataframes/commit/bfe2b23e2dea0cdf1e1b6ff5b17f6759d73c3e24))

## [0.22.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.21.0...v0.22.0) (2024-02-27)


### ⚠ BREAKING CHANGES

* rename cosine_similarity to paired_cosine_distances ([#393](https://github.com/googleapis/python-bigquery-dataframes/issues/393))
* move model optional args to kwargs ([#381](https://github.com/googleapis/python-bigquery-dataframes/issues/381))

### Features

* Add `DataFrames.corr()` method ([#379](https://github.com/googleapis/python-bigquery-dataframes/issues/379)) ([67fd434](https://github.com/googleapis/python-bigquery-dataframes/commit/67fd434bbb1c73f9013f65252d1ecc8da79542f6))
* Add ml.metrics.pairwise.manhattan_distance ([#392](https://github.com/googleapis/python-bigquery-dataframes/issues/392)) ([9d31865](https://github.com/googleapis/python-bigquery-dataframes/commit/9d318653c001287bcc8ae9d8e09d0187413cbed6))
* Enable regional endpoints for me-central2 ([#386](https://github.com/googleapis/python-bigquery-dataframes/issues/386)) ([469674d](https://github.com/googleapis/python-bigquery-dataframes/commit/469674d64f6ad5dac0f24ad450a7b8b6998fdf68))


### Bug Fixes

* Avoid ibis warning for "database" table() method argument ([#390](https://github.com/googleapis/python-bigquery-dataframes/issues/390)) ([a0490a4](https://github.com/googleapis/python-bigquery-dataframes/commit/a0490a492a43db24a314b3f42bfac61da7683151))
* Correct the numeric literal dtype ([#365](https://github.com/googleapis/python-bigquery-dataframes/issues/365)) ([93b02cd](https://github.com/googleapis/python-bigquery-dataframes/commit/93b02cd8bc620823563f8214b43bc5f2f35c155b))
* Rename cosine_similarity to paired_cosine_distances ([#393](https://github.com/googleapis/python-bigquery-dataframes/issues/393)) ([81ece46](https://github.com/googleapis/python-bigquery-dataframes/commit/81ece463b69765b0f93585d6b866fb642ddc65dc))


### Performance Improvements

* Inline read_pandas for small data ([#383](https://github.com/googleapis/python-bigquery-dataframes/issues/383)) ([59b446b](https://github.com/googleapis/python-bigquery-dataframes/commit/59b446bad8d2c5fca791c384616cfa7e54d54c09))


### Dependencies

* Add minimum version constraint for sqlglot to 19.9.0 ([#389](https://github.com/googleapis/python-bigquery-dataframes/issues/389)) ([8b62d77](https://github.com/googleapis/python-bigquery-dataframes/commit/8b62d77d8274cff2842c98b032bf98d69c483482))


### Documentation

* Add a code sample for creating a kmeans model ([#267](https://github.com/googleapis/python-bigquery-dataframes/issues/267)) ([4291d65](https://github.com/googleapis/python-bigquery-dataframes/commit/4291d656f30dc50b8ffcdd10ccbfa7f327711100))
* Fix `bigframes.pandas.concat` documentation ([#382](https://github.com/googleapis/python-bigquery-dataframes/issues/382)) ([234b61c](https://github.com/googleapis/python-bigquery-dataframes/commit/234b61cdfe75b402adf1b56f53b5f06934777f95))


### Miscellaneous Chores

* Release 0.22.0 ([#396](https://github.com/googleapis/python-bigquery-dataframes/issues/396)) ([8f73d9e](https://github.com/googleapis/python-bigquery-dataframes/commit/8f73d9e37827ecdc90683313000364922ae61dab))


### Code Refactoring

* Move model optional args to kwargs ([#381](https://github.com/googleapis/python-bigquery-dataframes/issues/381)) ([4037992](https://github.com/googleapis/python-bigquery-dataframes/commit/4037992b61ff352320d5dfb87dcf5f274791ace1))

## [0.21.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.20.1...v0.21.0) (2024-02-13)


### Features

* Add `Series.cov` method ([#368](https://github.com/googleapis/python-bigquery-dataframes/issues/368)) ([443db22](https://github.com/googleapis/python-bigquery-dataframes/commit/443db228375da9b232376140c9d5b0db14895eae))
* Add ml.llm.GeminiTextGenerator model ([#370](https://github.com/googleapis/python-bigquery-dataframes/issues/370)) ([de1e0a4](https://github.com/googleapis/python-bigquery-dataframes/commit/de1e0a451785e679f37b083be6d58c267319f56a))
* Add ml.metrics.pairwise.cosine_similarity function ([#374](https://github.com/googleapis/python-bigquery-dataframes/issues/374)) ([126f566](https://github.com/googleapis/python-bigquery-dataframes/commit/126f5660bd61bd8998e5f17ca0cbd39959590367))
* Add XGBoostModel ([#363](https://github.com/googleapis/python-bigquery-dataframes/issues/363)) ([d5518b2](https://github.com/googleapis/python-bigquery-dataframes/commit/d5518b28509be0ce070b22d9134a6a662412010a))
* Limited support of lambdas in `Series.apply` ([#345](https://github.com/googleapis/python-bigquery-dataframes/issues/345)) ([208e081](https://github.com/googleapis/python-bigquery-dataframes/commit/208e081fa99e17b8085e83c111c07eb6fc5c4730))
* Support bigframes.pandas.to_datetime for scalars, iterables and series. ([#372](https://github.com/googleapis/python-bigquery-dataframes/issues/372)) ([ffb0d15](https://github.com/googleapis/python-bigquery-dataframes/commit/ffb0d15602fe4d86e7a1aad72bba0a7049193a14))
* Support read_gbq wildcard table path ([#377](https://github.com/googleapis/python-bigquery-dataframes/issues/377)) ([90caf86](https://github.com/googleapis/python-bigquery-dataframes/commit/90caf865efc940f94e16643bda7ba261c2f2e473))


### Bug Fixes

* Error message fix. ([#375](https://github.com/googleapis/python-bigquery-dataframes/issues/375)) ([930cf6b](https://github.com/googleapis/python-bigquery-dataframes/commit/930cf6b9ae8a48f422586dbd21b52e15c9ef9492))


### Documentation

* Clarify ADC pre-auth in a non-interactive environment ([#348](https://github.com/googleapis/python-bigquery-dataframes/issues/348)) ([99a9e6e](https://github.com/googleapis/python-bigquery-dataframes/commit/99a9e6e15c6eef4297035ce89bb619f8e4ca54ff))

## [0.20.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.20.0...v0.20.1) (2024-02-06)


### Performance Improvements

* Make repr cache the block where appropriate ([#350](https://github.com/googleapis/python-bigquery-dataframes/issues/350)) ([068879f](https://github.com/googleapis/python-bigquery-dataframes/commit/068879f97fb1626aca081106150803f832a0cf81))


### Documentation

* Add a sample to demonstrate the evaluation results ([#364](https://github.com/googleapis/python-bigquery-dataframes/issues/364)) ([cff0919](https://github.com/googleapis/python-bigquery-dataframes/commit/cff09194b2c3a96a1f50e86a38ee59783c2a343b))
* Fix the `DataFrame.apply` code sample ([#366](https://github.com/googleapis/python-bigquery-dataframes/issues/366)) ([1866a26](https://github.com/googleapis/python-bigquery-dataframes/commit/1866a266f0fa40882b589579654c1ad428b036d8))

## [0.20.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.19.2...v0.20.0) (2024-01-30)


### Features

* Add `DataFrame.peek()` as an efficient alternative to `head()` results preview ([#318](https://github.com/googleapis/python-bigquery-dataframes/issues/318)) ([9c34d83](https://github.com/googleapis/python-bigquery-dataframes/commit/9c34d834e83ca5514bee723ebb9a7ad1ad50e88d))
* Add ARIMA_EVAULATE options in forecasting models ([#336](https://github.com/googleapis/python-bigquery-dataframes/issues/336)) ([73e997b](https://github.com/googleapis/python-bigquery-dataframes/commit/73e997b3e80f844a8120b52ed2ece8b046cf4ca9))
* Add Index constructor, repr, copy, get_level_values, to_series ([#334](https://github.com/googleapis/python-bigquery-dataframes/issues/334)) ([e5d054e](https://github.com/googleapis/python-bigquery-dataframes/commit/e5d054e93a05f5c504e8db57b954c07d33e5f5b9))
* Improve error message for drive based BQ table reads ([#344](https://github.com/googleapis/python-bigquery-dataframes/issues/344)) ([0794788](https://github.com/googleapis/python-bigquery-dataframes/commit/0794788a2d232d795d803cd0c5b3f7d51c562cf1))
* Update cut to work without labels = False and show intervals as dict ([#335](https://github.com/googleapis/python-bigquery-dataframes/issues/335)) ([4ff53db](https://github.com/googleapis/python-bigquery-dataframes/commit/4ff53db48133b817bec5f123b634690244a610d3))


### Bug Fixes

* Chance default connection name in getting_started.ipnyb ([#347](https://github.com/googleapis/python-bigquery-dataframes/issues/347)) ([677f014](https://github.com/googleapis/python-bigquery-dataframes/commit/677f0146acf19def88fddbeb0527a078458948ae))
* Series iteration correctly returns values instead of index ([#339](https://github.com/googleapis/python-bigquery-dataframes/issues/339)) ([2c6af9b](https://github.com/googleapis/python-bigquery-dataframes/commit/2c6af9ba8b362dae39a6e082cdc816c955c73517))


### Documentation

* Add code samples for `Series.{between, cumprod}` ([#353](https://github.com/googleapis/python-bigquery-dataframes/issues/353)) ([09a52fd](https://github.com/googleapis/python-bigquery-dataframes/commit/09a52fda19cde8efa6b20731d5b8e21f50b18a9a))

## [0.19.2](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.19.1...v0.19.2) (2024-01-22)


### Bug Fixes

* Read_gbq large response issue ([#332](https://github.com/googleapis/python-bigquery-dataframes/issues/332)) ([b8178b9](https://github.com/googleapis/python-bigquery-dataframes/commit/b8178b9a47958d9176d99dfd8833556a64d9724d))
* Use object dtype for ARRAY columns in `to_pandas()` with pandas 1.x ([#329](https://github.com/googleapis/python-bigquery-dataframes/issues/329)) ([374ddb5](https://github.com/googleapis/python-bigquery-dataframes/commit/374ddb534777895d93a1e2ae2f9c6dbe5f10bf8c))


### Documentation

* Add `DataFrame.applymap` documentation ([#326](https://github.com/googleapis/python-bigquery-dataframes/issues/326)) ([bd531a1](https://github.com/googleapis/python-bigquery-dataframes/commit/bd531a1557c08bcee6a0d275747f0939cdd33e81))
* Add code samples for series methods ([#323](https://github.com/googleapis/python-bigquery-dataframes/issues/323)) ([32cc6fa](https://github.com/googleapis/python-bigquery-dataframes/commit/32cc6fa73dea80e31985d380d550d8042e5f5566))
* Add remote model requirements ([#333](https://github.com/googleapis/python-bigquery-dataframes/issues/333)) ([c91f70c](https://github.com/googleapis/python-bigquery-dataframes/commit/c91f70ca7b9793cc62578d7845c3aa31cf8a4507))

## [0.19.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.19.0...v0.19.1) (2024-01-17)


### Bug Fixes

* Handle multi-level columns for df aggregates properly ([#305](https://github.com/googleapis/python-bigquery-dataframes/issues/305)) ([5bb45ba](https://github.com/googleapis/python-bigquery-dataframes/commit/5bb45ba5560f178438d490a62520ccd36fd2f284))
* Update max_output_token limitation. ([#308](https://github.com/googleapis/python-bigquery-dataframes/issues/308)) ([5cccd36](https://github.com/googleapis/python-bigquery-dataframes/commit/5cccd36fd2081becd741541c4ac8d5cf53c076f2))


### Documentation

* Add code samples for Series.corr ([#316](https://github.com/googleapis/python-bigquery-dataframes/issues/316)) ([9150c16](https://github.com/googleapis/python-bigquery-dataframes/commit/9150c16e951fb757547721e0003910c7c49e3d27))

## [0.19.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.18.0...v0.19.0) (2024-01-09)


### Features

* Add 'columns' as an alias for 'col_order' ([#298](https://github.com/googleapis/python-bigquery-dataframes/issues/298)) ([a01b271](https://github.com/googleapis/python-bigquery-dataframes/commit/a01b271e76d05459f531cd83c6e93a2d13bfa061))
* Add Series dt.tz and dt.unit properties ([#303](https://github.com/googleapis/python-bigquery-dataframes/issues/303)) ([2e1a403](https://github.com/googleapis/python-bigquery-dataframes/commit/2e1a4036e58fb6b35aa68ac6d121cb0d04f4f369))
* Add to_gbq() method for LLM models ([#299](https://github.com/googleapis/python-bigquery-dataframes/issues/299)) ([dafbc1b](https://github.com/googleapis/python-bigquery-dataframes/commit/dafbc1bdb225c7132cdf7191792fde785947c7a1))
* Allow manually set clustering_columns in dataframe.to_gbq ([#302](https://github.com/googleapis/python-bigquery-dataframes/issues/302)) ([9c21323](https://github.com/googleapis/python-bigquery-dataframes/commit/9c213239a73b5cd0ca7b647a86238263d3947431))
* Support assigning to columns like a property ([#304](https://github.com/googleapis/python-bigquery-dataframes/issues/304)) ([f645c56](https://github.com/googleapis/python-bigquery-dataframes/commit/f645c56e5436adb100018afbf9ef18003a1a6ed9))
* Support upcasting numeric columns in concat ([#294](https://github.com/googleapis/python-bigquery-dataframes/issues/294)) ([e3a056a](https://github.com/googleapis/python-bigquery-dataframes/commit/e3a056a301e99c4c3d2a2ecdcbcaf8804be8089f))


### Bug Fixes

* DF.drop tuple input as multi-index ([#301](https://github.com/googleapis/python-bigquery-dataframes/issues/301)) ([21391a9](https://github.com/googleapis/python-bigquery-dataframes/commit/21391a9d07bb0dc6b6f900f1b069350d6232bd92))
* Fix bug converting non-string labels to sql ids ([#296](https://github.com/googleapis/python-bigquery-dataframes/issues/296)) ([a61c5fe](https://github.com/googleapis/python-bigquery-dataframes/commit/a61c5fef1e3b88f38269ee5bfd50886b8d2908ae))


### Documentation

* Add code samples for `Series.ffill` and `DataFrame.ffill` ([#307](https://github.com/googleapis/python-bigquery-dataframes/issues/307)) ([1c63b45](https://github.com/googleapis/python-bigquery-dataframes/commit/1c63b451bb057e5b6470d63d4b44c090d7172aa5))

## [0.18.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.17.0...v0.18.0) (2024-01-02)


### Features

* Add dataframe.to_html ([#259](https://github.com/googleapis/python-bigquery-dataframes/issues/259)) ([2cd6489](https://github.com/googleapis/python-bigquery-dataframes/commit/2cd64891170dcd4f2a709024a2993e36db210976))
* Add IntervalIndex support to bigframes.pandas.cut ([#254](https://github.com/googleapis/python-bigquery-dataframes/issues/254)) ([6c1969a](https://github.com/googleapis/python-bigquery-dataframes/commit/6c1969a35fe720cf3a804006bcc9046ba554fcc3))
* Add replace method to DataFrame ([#261](https://github.com/googleapis/python-bigquery-dataframes/issues/261)) ([5092215](https://github.com/googleapis/python-bigquery-dataframes/commit/5092215767d77c90b132e9cd6b3e3749827ebe09))
* Specific pyarrow mappings for decimal, bytes types ([#283](https://github.com/googleapis/python-bigquery-dataframes/issues/283)) ([a1c0631](https://github.com/googleapis/python-bigquery-dataframes/commit/a1c06319ab0e3697c3175112490488002bb344c0))


### Bug Fixes

* Dataframes to_gbq now creates dataset if it doesn't exist ([#222](https://github.com/googleapis/python-bigquery-dataframes/issues/222)) ([bac62f7](https://github.com/googleapis/python-bigquery-dataframes/commit/bac62f76af1af6ca8834c3690c7c79aeb12dd331))
* Exclude pandas 2.2.0rc0 to unblock prerelease tests ([#292](https://github.com/googleapis/python-bigquery-dataframes/issues/292)) ([ac1a745](https://github.com/googleapis/python-bigquery-dataframes/commit/ac1a745ddce9865f4585777b43c2234b9bf2841d))
* Fix DataFrameGroupby.agg() issue with as_index=False ([#273](https://github.com/googleapis/python-bigquery-dataframes/issues/273)) ([ab49350](https://github.com/googleapis/python-bigquery-dataframes/commit/ab493506e71ed8970a11fe2f88b2145150e09291))
* Make `Series.str.replace` work for simple strings ([#285](https://github.com/googleapis/python-bigquery-dataframes/issues/285)) ([ad67465](https://github.com/googleapis/python-bigquery-dataframes/commit/ad6746569b3af11be9d40805a1449ee1e89288dc))
* Update dataframe.to_gbq to dedup column names. ([#286](https://github.com/googleapis/python-bigquery-dataframes/issues/286)) ([746115d](https://github.com/googleapis/python-bigquery-dataframes/commit/746115d5564c95bc3c4a5309c99e7a29e535e6fe))
* Use setuptools.find_namespace_packages ([#246](https://github.com/googleapis/python-bigquery-dataframes/issues/246)) ([9ec352a](https://github.com/googleapis/python-bigquery-dataframes/commit/9ec352a338f11d82aee9cd665ffb0e6e97cb391b))


### Dependencies

* Migrate to `ibis-framework &gt;= "7.1.0"` ([#53](https://github.com/googleapis/python-bigquery-dataframes/issues/53)) ([9798a2b](https://github.com/googleapis/python-bigquery-dataframes/commit/9798a2b14dffb20432f732343cac92341e42fe09))


### Documentation

* Add code snippets for explore query result page ([#278](https://github.com/googleapis/python-bigquery-dataframes/issues/278)) ([7cbbb7d](https://github.com/googleapis/python-bigquery-dataframes/commit/7cbbb7d4608d8b7d1a360b2fe2d39d89a52f9546))
* Code samples for `astype` common to DataFrame and Series ([#280](https://github.com/googleapis/python-bigquery-dataframes/issues/280)) ([95b673a](https://github.com/googleapis/python-bigquery-dataframes/commit/95b673aeb1545744e4b1a353cf1f4d0202d8a1b2))
* Code samples for `DataFrame.copy` and `Series.copy` ([#290](https://github.com/googleapis/python-bigquery-dataframes/issues/290)) ([7cbc2b0](https://github.com/googleapis/python-bigquery-dataframes/commit/7cbc2b0ba572d11778ba7caf7c95b7fb8f3a31a7))
* Code samples for `drop` and `fillna` ([#284](https://github.com/googleapis/python-bigquery-dataframes/issues/284)) ([9c5012e](https://github.com/googleapis/python-bigquery-dataframes/commit/9c5012ec68275db83d1f6f7e743f5edaaaacd8cb))
* Code samples for `isna`, `isnull`, `dropna`, `isin` ([#289](https://github.com/googleapis/python-bigquery-dataframes/issues/289)) ([ad51035](https://github.com/googleapis/python-bigquery-dataframes/commit/ad51035bcf80d6a49f134df26624b578010b5b12))
* Code samples for `rename` , `size` ([#293](https://github.com/googleapis/python-bigquery-dataframes/issues/293)) ([eb69f60](https://github.com/googleapis/python-bigquery-dataframes/commit/eb69f60db52544882fb06c2d5fa0e41226dfe93f))
* Code samples for `reset_index` and `sort_values` ([#282](https://github.com/googleapis/python-bigquery-dataframes/issues/282)) ([acc0eb7](https://github.com/googleapis/python-bigquery-dataframes/commit/acc0eb7010951c8cfb91aecc45268b041217dd09))
* Code samples for `sample`, `get`, `Series.round` ([#295](https://github.com/googleapis/python-bigquery-dataframes/issues/295)) ([c2b1892](https://github.com/googleapis/python-bigquery-dataframes/commit/c2b1892825545a34ce4ed5b0ef99e99348466108))
* Code samples for `Series.{add, replace, unique, T, transpose}` ([#287](https://github.com/googleapis/python-bigquery-dataframes/issues/287)) ([0e1bbfc](https://github.com/googleapis/python-bigquery-dataframes/commit/0e1bbfc1055aff9757b5138907c11caab2f3965a))
* Code samples for `Series.{map, to_list, count}` ([#290](https://github.com/googleapis/python-bigquery-dataframes/issues/290)) ([7cbc2b0](https://github.com/googleapis/python-bigquery-dataframes/commit/7cbc2b0ba572d11778ba7caf7c95b7fb8f3a31a7))
* Code samples for `Series.{name, std, agg}` ([#293](https://github.com/googleapis/python-bigquery-dataframes/issues/293)) ([eb69f60](https://github.com/googleapis/python-bigquery-dataframes/commit/eb69f60db52544882fb06c2d5fa0e41226dfe93f))
* Code samples for `Series.groupby` and `Series.{sum,mean,min,max}` ([#280](https://github.com/googleapis/python-bigquery-dataframes/issues/280)) ([95b673a](https://github.com/googleapis/python-bigquery-dataframes/commit/95b673aeb1545744e4b1a353cf1f4d0202d8a1b2))
* Code samples for DataFrame `set_index`, `items` ([#295](https://github.com/googleapis/python-bigquery-dataframes/issues/295)) ([c2b1892](https://github.com/googleapis/python-bigquery-dataframes/commit/c2b1892825545a34ce4ed5b0ef99e99348466108))
* Fix the rendering for `get_dummies` ([#291](https://github.com/googleapis/python-bigquery-dataframes/issues/291)) ([252f3a2](https://github.com/googleapis/python-bigquery-dataframes/commit/252f3a2a0e1296c7d786acdc0bdebe9e4a9ae1be))

## [0.17.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.16.0...v0.17.0) (2023-12-14)


### Features

* Add `filters` argument to `read_gbq` for enhanced data querying ([#198](https://github.com/googleapis/python-bigquery-dataframes/issues/198)) ([034f71f](https://github.com/googleapis/python-bigquery-dataframes/commit/034f71f113235f2218223e43f129507c1ec3f6ff))
* Add module/class level api tracking ([#272](https://github.com/googleapis/python-bigquery-dataframes/issues/272)) ([4f3db3d](https://github.com/googleapis/python-bigquery-dataframes/commit/4f3db3d50fb782dbe03051ed024d03e19944d775))
* Deprecate `use_regional_endpoints` ([#199](https://github.com/googleapis/python-bigquery-dataframes/issues/199)) ([319a1f2](https://github.com/googleapis/python-bigquery-dataframes/commit/319a1f27be5bd96ebbe29f11a00a5a62d2b4237f))


### Bug Fixes

* Increase recursion limit, cache compilation tree hashes ([#184](https://github.com/googleapis/python-bigquery-dataframes/issues/184)) ([b54791c](https://github.com/googleapis/python-bigquery-dataframes/commit/b54791c820f56c578a0bd9883489de9b9c7eb3a2))
* Replaced raise `NotImplementedError` with return `NotImplemented` ([#258](https://github.com/googleapis/python-bigquery-dataframes/issues/258)) ([a133822](https://github.com/googleapis/python-bigquery-dataframes/commit/a133822974229f70529a414a682b6d98770d1846))


### Documentation

* Add code samples for `values` and `value_counts` ([#249](https://github.com/googleapis/python-bigquery-dataframes/issues/249)) ([f247d95](https://github.com/googleapis/python-bigquery-dataframes/commit/f247d957a12a119ce8a263df215e8a9ef7310ef6))
* Add sample for getting started with BQML ([#141](https://github.com/googleapis/python-bigquery-dataframes/issues/141)) ([fb14f54](https://github.com/googleapis/python-bigquery-dataframes/commit/fb14f54548e988c6c226753fcca162cf15b5c8d7))

## [0.16.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.15.0...v0.16.0) (2023-12-12)


### Features

* Add ARIMAPlus.predict parameters ([#264](https://github.com/googleapis/python-bigquery-dataframes/issues/264)) ([99598c7](https://github.com/googleapis/python-bigquery-dataframes/commit/99598c7d359f1d1e0671dcf27a5c77094f3c7f67))
* Add DataFrame from_dict and from_records methods ([#244](https://github.com/googleapis/python-bigquery-dataframes/issues/244)) ([8d81e24](https://github.com/googleapis/python-bigquery-dataframes/commit/8d81e24677613dcf4d275c27a327384b8c17bc85))
* Add DataFrame.select_dtypes method ([#242](https://github.com/googleapis/python-bigquery-dataframes/issues/242)) ([1737acc](https://github.com/googleapis/python-bigquery-dataframes/commit/1737acc51b4fdd9b385bbf91a758efd2e7ead11a))
* Add nunique method to Series/DataFrameGroupby ([#256](https://github.com/googleapis/python-bigquery-dataframes/issues/256)) ([c8ec245](https://github.com/googleapis/python-bigquery-dataframes/commit/c8ec245070402aa0770bc9b2375693de674ca925))
* Support dataframe.loc with conditional columns selection ([#233](https://github.com/googleapis/python-bigquery-dataframes/issues/233)) ([3febea9](https://github.com/googleapis/python-bigquery-dataframes/commit/3febea99358d10f823d43c3af83ea30458e579a2))


### Bug Fixes

* Enfore pandas version requirement &lt;2.1.4 ([#265](https://github.com/googleapis/python-bigquery-dataframes/issues/265)) ([9dd63f6](https://github.com/googleapis/python-bigquery-dataframes/commit/9dd63f6dcb6234e1f3aebd63c59e1e5c717099dc))
* Exclude pandas 2.1.4 from prerelease tests to unblock e2e tests ([b02fc2c](https://github.com/googleapis/python-bigquery-dataframes/commit/b02fc2c1843e18d3a8d6894c64763f53e6af1b73))
* Fix value_counts column label for normalize=True ([#245](https://github.com/googleapis/python-bigquery-dataframes/issues/245)) ([d3fa6f2](https://github.com/googleapis/python-bigquery-dataframes/commit/d3fa6f26931d5d0f0ae3fa49baccfc148f870417))
* Migrate e2e tests to bigframes-load-testing project ([8766ac6](https://github.com/googleapis/python-bigquery-dataframes/commit/8766ac63f501929577f71e6bd2b523e92c43ba66))
* Ml.sql logic ([#262](https://github.com/googleapis/python-bigquery-dataframes/issues/262)) ([68c6fdf](https://github.com/googleapis/python-bigquery-dataframes/commit/68c6fdf78af8b87fa4ef4f832631f24d7433a4d8))
* Update the llm_kmeans notebook ([#247](https://github.com/googleapis/python-bigquery-dataframes/issues/247)) ([66d1839](https://github.com/googleapis/python-bigquery-dataframes/commit/66d1839c3e9a3011c7feb13a59d966b64cf8313f))


### Documentation

* Add code samples for `shape` and `head` ([#257](https://github.com/googleapis/python-bigquery-dataframes/issues/257)) ([5bdcc65](https://github.com/googleapis/python-bigquery-dataframes/commit/5bdcc6594ef2e99e96636341d286ea70420858fe))
* Add example for dataframe.melt, dataframe.pivot, dataframe.stac… ([#252](https://github.com/googleapis/python-bigquery-dataframes/issues/252)) ([8c63697](https://github.com/googleapis/python-bigquery-dataframes/commit/8c636978f4a21eda2856862100b7a8272797fe42))
* Add example to dataframe.nlargest, dataframe.nsmallest, datafra… ([#234](https://github.com/googleapis/python-bigquery-dataframes/issues/234)) ([e735412](https://github.com/googleapis/python-bigquery-dataframes/commit/e735412fdc52d034df92dd5462d6956bdc0167be))
* Add examples for dataframe.cummin, dataframe.cummax, dataframe.cumsum, dataframe.cumprod ([#243](https://github.com/googleapis/python-bigquery-dataframes/issues/243)) ([0523a31](https://github.com/googleapis/python-bigquery-dataframes/commit/0523a31fa0b589f88afe0ad5b447634409ddeb86))
* Add examples for dataframe.nunique, dataframe.diff, dataframe.a… ([#251](https://github.com/googleapis/python-bigquery-dataframes/issues/251)) ([77074ec](https://github.com/googleapis/python-bigquery-dataframes/commit/77074ecbe7f52d1d7d1d1dc537fbe4062b407672))
* Correct the docs for `option_context` ([#263](https://github.com/googleapis/python-bigquery-dataframes/issues/263)) ([d21c6dd](https://github.com/googleapis/python-bigquery-dataframes/commit/d21c6dd26eadd64c526b0fd35b977a74b8334562))
* Correct the params rendering for `ml.remote` and `ml.ensemble` modules ([#248](https://github.com/googleapis/python-bigquery-dataframes/issues/248)) ([c2829e3](https://github.com/googleapis/python-bigquery-dataframes/commit/c2829e3d976a43c53251c9288266e3a8ec5304c5))
* Fix return annotation in API docstrings ([#253](https://github.com/googleapis/python-bigquery-dataframes/issues/253)) ([89a1c67](https://github.com/googleapis/python-bigquery-dataframes/commit/89a1c67fa5cbb76c1cc6ae24d5f919e22514705c))

## [0.15.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.14.1...v0.15.0) (2023-11-29)


### ⚠ BREAKING CHANGES

* model.predict returns all the columns ([#204](https://github.com/googleapis/python-bigquery-dataframes/issues/204))

### Features

* Add info and memory_usage methods to dataframe ([#219](https://github.com/googleapis/python-bigquery-dataframes/issues/219)) ([9d6613d](https://github.com/googleapis/python-bigquery-dataframes/commit/9d6613d318b558722b7bab12773efdea4bbe9931))
* Add remote vertex model support ([#237](https://github.com/googleapis/python-bigquery-dataframes/issues/237)) ([0bfc4fb](https://github.com/googleapis/python-bigquery-dataframes/commit/0bfc4fb117686c734d4a2503d5a6de0e64e9f9b9))
* Add the recent api method for ML component ([#225](https://github.com/googleapis/python-bigquery-dataframes/issues/225)) ([ed8876d](https://github.com/googleapis/python-bigquery-dataframes/commit/ed8876d3439a3b45b65e8789737c3c2e3a7f1adb))
* Model.predict returns all the columns ([#204](https://github.com/googleapis/python-bigquery-dataframes/issues/204)) ([416171a](https://github.com/googleapis/python-bigquery-dataframes/commit/416171a70d91d4a6b71622ba72685147ab7d6186))
* Send warnings on LLM prediction partial failures ([#216](https://github.com/googleapis/python-bigquery-dataframes/issues/216)) ([81125f9](https://github.com/googleapis/python-bigquery-dataframes/commit/81125f9505ad98e89939769a8e1fcf30518705f0))


### Bug Fixes

* Add df snapshots lookup for `read_gbq` ([#229](https://github.com/googleapis/python-bigquery-dataframes/issues/229)) ([d0d9b84](https://github.com/googleapis/python-bigquery-dataframes/commit/d0d9b84b101eb03c499d85e74dcfc900dedd4137))
* Avoid unnecessary row_number() on sort key for io ([#211](https://github.com/googleapis/python-bigquery-dataframes/issues/211)) ([a18d40e](https://github.com/googleapis/python-bigquery-dataframes/commit/a18d40e808ee0822d21715cc3e8f794c418aeebc))
* Dedup special character ([#209](https://github.com/googleapis/python-bigquery-dataframes/issues/209)) ([dd78acb](https://github.com/googleapis/python-bigquery-dataframes/commit/dd78acb174545ba292776a642afcec46f8ee4a2a))
* Invalid JSON type of the notebook ([#215](https://github.com/googleapis/python-bigquery-dataframes/issues/215)) ([a729831](https://github.com/googleapis/python-bigquery-dataframes/commit/a7298317ea2604faa6ae31817f1f729d7e0b9818))
* Make to_pandas override enable_downsampling when sampling_method is manually set. ([#200](https://github.com/googleapis/python-bigquery-dataframes/issues/200)) ([ae03756](https://github.com/googleapis/python-bigquery-dataframes/commit/ae03756f5ee45e0e74e0c0bdd4777e018eba2273))
* Polish the llm+kmeans notebook ([#208](https://github.com/googleapis/python-bigquery-dataframes/issues/208)) ([e8532b1](https://github.com/googleapis/python-bigquery-dataframes/commit/e8532b1d999d26ea1ebdd30efb8f2c0a93a6a28d))
* Update the llm+kmeans notebook with recent change ([#236](https://github.com/googleapis/python-bigquery-dataframes/issues/236)) ([f8917ab](https://github.com/googleapis/python-bigquery-dataframes/commit/f8917abc094e222e0435891d4d184b77bfe67722))
* Use anonymous dataset to create `remote_function` ([#205](https://github.com/googleapis/python-bigquery-dataframes/issues/205)) ([69b016e](https://github.com/googleapis/python-bigquery-dataframes/commit/69b016eae7ea97d84ceeb22ba09f5472841db072))


### Documentation

* Add code samples for `index` and `column` properties ([#212](https://github.com/googleapis/python-bigquery-dataframes/issues/212)) ([c88d38e](https://github.com/googleapis/python-bigquery-dataframes/commit/c88d38e69682f4c620174086b8f16f4780c04811))
* Add code samples for df reshaping, function, merge, and join methods ([#203](https://github.com/googleapis/python-bigquery-dataframes/issues/203)) ([010486c](https://github.com/googleapis/python-bigquery-dataframes/commit/010486c3494e05d714da6cc7d51514518d9ae1ea))
* Add examples for dataframe.kurt, dataframe.std, dataframe.count ([#232](https://github.com/googleapis/python-bigquery-dataframes/issues/232)) ([f9c6e72](https://github.com/googleapis/python-bigquery-dataframes/commit/f9c6e727e2b901310bb5301da449d616ea85e135))
* Add examples for dataframe.mean, dataframe.median, dataframe.va… ([#228](https://github.com/googleapis/python-bigquery-dataframes/issues/228)) ([edd0522](https://github.com/googleapis/python-bigquery-dataframes/commit/edd0522747eadb74780124fb18ed7face251441d))
* Add examples for dataframe.min, dataframe.max and dataframe.sum ([#227](https://github.com/googleapis/python-bigquery-dataframes/issues/227)) ([3a375e8](https://github.com/googleapis/python-bigquery-dataframes/commit/3a375e87b64b8fb51370bfec8f2cfdbcd8fe960a))
* Code samples for `Series.dot` and `DataFrame.dot` ([#226](https://github.com/googleapis/python-bigquery-dataframes/issues/226)) ([b62a07a](https://github.com/googleapis/python-bigquery-dataframes/commit/b62a07a95cd60f995a48825c9874822d0eb02483))
* Code samples for `Series.where` and `Series.mask` ([#217](https://github.com/googleapis/python-bigquery-dataframes/issues/217)) ([52dfad2](https://github.com/googleapis/python-bigquery-dataframes/commit/52dfad281def82548751a276ce42b087dbb09f9a))
* Code samples for dataframe.any, dataframe.all and dataframe.prod ([#223](https://github.com/googleapis/python-bigquery-dataframes/issues/223)) ([d7957fa](https://github.com/googleapis/python-bigquery-dataframes/commit/d7957fad071d223ef8f6fb8f3de395c865ff60aa))
* Make the code samples reflect default bq connection usage ([#206](https://github.com/googleapis/python-bigquery-dataframes/issues/206)) ([71844b0](https://github.com/googleapis/python-bigquery-dataframes/commit/71844b03cdbfe684320c186a0488c8c7fb4fcd6e))


### Miscellaneous Chores

* Release 0.15.0 ([#241](https://github.com/googleapis/python-bigquery-dataframes/issues/241)) ([6c899be](https://github.com/googleapis/python-bigquery-dataframes/commit/6c899be2989e24f697d72fe1bb92ebbf7dec84cb))

## [0.14.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.14.0...v0.14.1) (2023-11-16)


### Bug Fixes

* Correctly handle null values when initializing fingerprint ordering ([#210](https://github.com/googleapis/python-bigquery-dataframes/issues/210)) ([8324f13](https://github.com/googleapis/python-bigquery-dataframes/commit/8324f133547ec35da5eefc0a8b02fe0f3887d81d))


### Documentation

* Add an example notebook about line graphs ([#197](https://github.com/googleapis/python-bigquery-dataframes/issues/197)) ([f957b27](https://github.com/googleapis/python-bigquery-dataframes/commit/f957b278b39e0a472a3153e9e1906c2d5f2ac2e5))

## [0.14.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.13.0...v0.14.0) (2023-11-14)


### Features

* Add 'cross' join support ([#176](https://github.com/googleapis/python-bigquery-dataframes/issues/176)) ([765446a](https://github.com/googleapis/python-bigquery-dataframes/commit/765446a929abe1ac076c3037afa7892f64105356))
* Add 'index', 'pad', 'nearest' interpolate methods ([#162](https://github.com/googleapis/python-bigquery-dataframes/issues/162)) ([6a28403](https://github.com/googleapis/python-bigquery-dataframes/commit/6a2840349a23035bdfdabacd1e231b41bbb5ed7a))
* Add series.sample (identical to existing dataframe.sample) ([#187](https://github.com/googleapis/python-bigquery-dataframes/issues/187)) ([37914a4](https://github.com/googleapis/python-bigquery-dataframes/commit/37914a4077c681881491f5c36d1a9c9f4255e18f))
* Add unordered sql compilation ([#156](https://github.com/googleapis/python-bigquery-dataframes/issues/156)) ([58f420c](https://github.com/googleapis/python-bigquery-dataframes/commit/58f420c91d94ca085e9810f36513ffe772bfddcf))
* Log most recent API calls as `recent-bigframes-api-xx` labels on BigQuery jobs ([#145](https://github.com/googleapis/python-bigquery-dataframes/issues/145)) ([4ea33b7](https://github.com/googleapis/python-bigquery-dataframes/commit/4ea33b7433532ae3a386a6ffa9eb57360ea39526))
* Read_gbq creates order deterministically without table copy ([#191](https://github.com/googleapis/python-bigquery-dataframes/issues/191)) ([8ab81de](https://github.com/googleapis/python-bigquery-dataframes/commit/8ab81dee4d0eee499094f2dd576550f0c59d7551))
* Support `date_series.astype("string[pyarrow]")` to cast DATE to STRING ([#186](https://github.com/googleapis/python-bigquery-dataframes/issues/186)) ([aee0e8e](https://github.com/googleapis/python-bigquery-dataframes/commit/aee0e8e2518c59bd1e0b07940c3309871fde8899))
* Support `series.at[row_label] = scalar` ([#173](https://github.com/googleapis/python-bigquery-dataframes/issues/173)) ([0c8bd33](https://github.com/googleapis/python-bigquery-dataframes/commit/0c8bd33806bb99206b8b12dbdf7d7485c6ffb759))
* Temporary resources no longer use BigQuery Sessions ([#194](https://github.com/googleapis/python-bigquery-dataframes/issues/194)) ([4a02cac](https://github.com/googleapis/python-bigquery-dataframes/commit/4a02cac88c7d7b46bed1fa813a862fc2ef9ef084))


### Bug Fixes

* All sort operation are now stable ([#195](https://github.com/googleapis/python-bigquery-dataframes/issues/195)) ([3a2761f](https://github.com/googleapis/python-bigquery-dataframes/commit/3a2761f3c38d0de8b8eda47fffa15b8412aa84b0))
* Default to 7 days expiration for `read_csv`, `read_json`, `read_parquet` ([#193](https://github.com/googleapis/python-bigquery-dataframes/issues/193)) ([03606cd](https://github.com/googleapis/python-bigquery-dataframes/commit/03606cda30eb7645bfd4534460112dcca56b0ab0))
* Deprecate the `remote_service_type` in llm model ([#180](https://github.com/googleapis/python-bigquery-dataframes/issues/180)) ([a8a409a](https://github.com/googleapis/python-bigquery-dataframes/commit/a8a409ab0bd1f99dfb442df0703bf8786e0fe58e))
* For reset_index on unnamed multiindex, always use level_[n] label ([#182](https://github.com/googleapis/python-bigquery-dataframes/issues/182)) ([f95000d](https://github.com/googleapis/python-bigquery-dataframes/commit/f95000d3f88662be4d88c8b0152f1b838e99ec55))
* Match pandas behavior when assigning listlike to empty dfs ([#172](https://github.com/googleapis/python-bigquery-dataframes/issues/172)) ([c1d1f42](https://github.com/googleapis/python-bigquery-dataframes/commit/c1d1f42a21cc089877f79ebb46a39ddef6958e04))
* Use anonymous dataset instead of session dataset for temp tables ([#181](https://github.com/googleapis/python-bigquery-dataframes/issues/181)) ([800d44e](https://github.com/googleapis/python-bigquery-dataframes/commit/800d44eb5eb77da5d87b2e005f5a2ed53842e7b5))
* Use random table for `read_pandas` ([#192](https://github.com/googleapis/python-bigquery-dataframes/issues/192)) ([741c75e](https://github.com/googleapis/python-bigquery-dataframes/commit/741c75e5797e26a1487ff3da76a07953d9537f3f))
* Use random table when loading data for `read_csv`, `read_json`, `read_parquet` ([#175](https://github.com/googleapis/python-bigquery-dataframes/issues/175)) ([9d2e6dc](https://github.com/googleapis/python-bigquery-dataframes/commit/9d2e6dc1ae4e11e80da4aabe0daa3a6044137cc6))


### Documentation

* Add code samples for `read_gbq_function` using community UDFs ([#188](https://github.com/googleapis/python-bigquery-dataframes/issues/188)) ([7506eab](https://github.com/googleapis/python-bigquery-dataframes/commit/7506eabf2e58159507809e36abfe90c417dfe92f))
* Add docstring code samples for `Series.apply` and `DataFrame.map` ([#185](https://github.com/googleapis/python-bigquery-dataframes/issues/185)) ([c816d84](https://github.com/googleapis/python-bigquery-dataframes/commit/c816d843e6f3c5a944cd4395ed0e1e91cec49812))
* Add llm kmeans notebook as an included example ([#177](https://github.com/googleapis/python-bigquery-dataframes/issues/177)) ([d49ae42](https://github.com/googleapis/python-bigquery-dataframes/commit/d49ae42a379fafd601cc94227e7f8f14b3d5f8c3))
* Use `head()` to get top `n` results, not to preview results ([#190](https://github.com/googleapis/python-bigquery-dataframes/issues/190)) ([87f84c9](https://github.com/googleapis/python-bigquery-dataframes/commit/87f84c9e58e7d0ea521ac386c9f02791cdddd19f))

## [0.13.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.12.0...v0.13.0) (2023-11-07)


### Features

* `to_gbq` without a destination table writes to a temporary table ([#158](https://github.com/googleapis/python-bigquery-dataframes/issues/158)) ([e1817c9](https://github.com/googleapis/python-bigquery-dataframes/commit/e1817c9201ba4ea7fd2f8b6f4a667b010a6fec1b))
* Add `DataFrame.__iter__`, `DataFrame.iterrows`, `DataFrame.itertuples`, and `DataFrame.keys` methods ([#164](https://github.com/googleapis/python-bigquery-dataframes/issues/164)) ([c065071](https://github.com/googleapis/python-bigquery-dataframes/commit/c065071028c2f4ac80ee7f84dbeb1df385c2a512))
* Add `Series.__iter__` method ([#164](https://github.com/googleapis/python-bigquery-dataframes/issues/164)) ([c065071](https://github.com/googleapis/python-bigquery-dataframes/commit/c065071028c2f4ac80ee7f84dbeb1df385c2a512))
* Add interpolate() to series and dataframe ([#157](https://github.com/googleapis/python-bigquery-dataframes/issues/157)) ([b9cb55c](https://github.com/googleapis/python-bigquery-dataframes/commit/b9cb55c5b9354f9ff60de0aad66fe60049876055))
* Support 32k text-generation and multilingual embedding models ([#161](https://github.com/googleapis/python-bigquery-dataframes/issues/161)) ([5f0ea37](https://github.com/googleapis/python-bigquery-dataframes/commit/5f0ea37fffff792fc3fbed65e6ace846d8ef6a06))


### Bug Fixes

* Update default temp table expiration to 7 days ([#174](https://github.com/googleapis/python-bigquery-dataframes/issues/174)) ([4ff26cd](https://github.com/googleapis/python-bigquery-dataframes/commit/4ff26cdf862e9f9b91a3a1d2abfa7fbdf0af9c5b))

## [0.12.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.11.0...v0.12.0) (2023-11-01)


### Features

* Add `DataFrame.melt` ([#113](https://github.com/googleapis/python-bigquery-dataframes/issues/113)) ([4e4409c](https://github.com/googleapis/python-bigquery-dataframes/commit/4e4409c5b235171f3770aec852193026519948fd))
* Add `DataFrame.to_pandas_batches()` to download large `DataFrame` objects ([#136](https://github.com/googleapis/python-bigquery-dataframes/issues/136)) ([3afd4a3](https://github.com/googleapis/python-bigquery-dataframes/commit/3afd4a35f4c38dad86dab17ff62444cd418cab88))
* Add bigframes.options.compute.maximum_bytes_billed option that sets maximum bytes billed on query jobs ([#133](https://github.com/googleapis/python-bigquery-dataframes/issues/133)) ([63c7919](https://github.com/googleapis/python-bigquery-dataframes/commit/63c7919e28d2e0b864142320b47374d807f07c03))
* Add pandas.qcut ([#104](https://github.com/googleapis/python-bigquery-dataframes/issues/104)) ([8e44518](https://github.com/googleapis/python-bigquery-dataframes/commit/8e4451841ba09099b0ed5433f9102511741dfbed))
* Add pd.get_dummies ([#149](https://github.com/googleapis/python-bigquery-dataframes/issues/149)) ([d8baad5](https://github.com/googleapis/python-bigquery-dataframes/commit/d8baad5b71ec67a35a0fb6132ee16e4c7418c456))
* Add unstack to series, add level param ([#115](https://github.com/googleapis/python-bigquery-dataframes/issues/115)) ([5edcd19](https://github.com/googleapis/python-bigquery-dataframes/commit/5edcd19e6200db9b9ebe3d4945816b3ebf1f7bcd))
* Implement operator `@` for `DataFrame.dot` ([#139](https://github.com/googleapis/python-bigquery-dataframes/issues/139)) ([79a638e](https://github.com/googleapis/python-bigquery-dataframes/commit/79a638eda80c482b640b523426ffd95c42747edc))
* Populate ibis version in user agent ([#140](https://github.com/googleapis/python-bigquery-dataframes/issues/140)) ([c639a36](https://github.com/googleapis/python-bigquery-dataframes/commit/c639a3657465e2b68a3b93c363bd3ae1e969d2cc))


### Bug Fixes

* Don't override the global logging config ([#138](https://github.com/googleapis/python-bigquery-dataframes/issues/138)) ([2ddbf74](https://github.com/googleapis/python-bigquery-dataframes/commit/2ddbf743efc2fd8ffb61ae8d3333fc4b98ce4b55))
* Fix bug with column names under repeated column assignment ([#150](https://github.com/googleapis/python-bigquery-dataframes/issues/150)) ([29032d0](https://github.com/googleapis/python-bigquery-dataframes/commit/29032d06811569121f7be2a7de915740df7daf6e))
* Resolve plotly rendering issue by using ipython html for job pro… ([#134](https://github.com/googleapis/python-bigquery-dataframes/issues/134)) ([39df43e](https://github.com/googleapis/python-bigquery-dataframes/commit/39df43e243ac0374d1a1eb2a75779324825afbe9))
* Use indexee's session for loc listlike cases ([#152](https://github.com/googleapis/python-bigquery-dataframes/issues/152)) ([27c5725](https://github.com/googleapis/python-bigquery-dataframes/commit/27c57255c7fe11e1ef9b9826d988d80fc17442a6))


### Documentation

* Add artithmetic df sample code ([#153](https://github.com/googleapis/python-bigquery-dataframes/issues/153)) ([ac44ccd](https://github.com/googleapis/python-bigquery-dataframes/commit/ac44ccd3936cdb28755d2bbe16377d489f08d5e5))
* Fix indentation on `read_gbq_function` code sample ([#163](https://github.com/googleapis/python-bigquery-dataframes/issues/163)) ([0801d96](https://github.com/googleapis/python-bigquery-dataframes/commit/0801d96830dab467232277dea9fd2dacee41055c))
* Link to ML.EVALUATE BQML page for score() methods ([#137](https://github.com/googleapis/python-bigquery-dataframes/issues/137)) ([45c617f](https://github.com/googleapis/python-bigquery-dataframes/commit/45c617fee7becc42f1c129246ffdc32f3a963f12))

## [0.11.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.10.0...v0.11.0) (2023-10-26)


### Features

* Add back `reset_session` as an alias for `close_session` ([#124](https://github.com/googleapis/python-bigquery-dataframes/issues/124)) ([694a85a](https://github.com/googleapis/python-bigquery-dataframes/commit/694a85a0ef90d838700014a204d72b23362db1d8))
* Change `query` parameter to `query_or_table` in `read_gbq` ([#127](https://github.com/googleapis/python-bigquery-dataframes/issues/127)) ([f9bb3c4](https://github.com/googleapis/python-bigquery-dataframes/commit/f9bb3c4bc88c5ba2be6f17e12a0ec4f482ce161f))


### Bug Fixes

* Expose `bigframes.pandas.reset_session` as a public API ([#128](https://github.com/googleapis/python-bigquery-dataframes/issues/128)) ([b17e1f4](https://github.com/googleapis/python-bigquery-dataframes/commit/b17e1f43cd0f7567bc5b59b0e916cd20528312b3))
* Use series's own session in series.reindex listlike case ([#135](https://github.com/googleapis/python-bigquery-dataframes/issues/135)) ([95bff3f](https://github.com/googleapis/python-bigquery-dataframes/commit/95bff3f1902bc09dc3310798a42df8ffd31ed8ee))


### Documentation

* Add runnable code samples for DataFrames I/O methods and property ([#129](https://github.com/googleapis/python-bigquery-dataframes/issues/129)) ([6fea8ef](https://github.com/googleapis/python-bigquery-dataframes/commit/6fea8efac35871985677ebeb948a576e64a1ffa4))
* Add runnable code samples for reading methods ([#125](https://github.com/googleapis/python-bigquery-dataframes/issues/125)) ([a669919](https://github.com/googleapis/python-bigquery-dataframes/commit/a669919ff25b56156bd70ccd816a0bf19adb48aa))

## [0.10.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.9.0...v0.10.0) (2023-10-19)


### Features

* Implement DataFrame.dot for matrix multiplication ([#67](https://github.com/googleapis/python-bigquery-dataframes/issues/67)) ([29dd414](https://github.com/googleapis/python-bigquery-dataframes/commit/29dd4144c7e0569de3555a16f916be9c4489bf61))

## [0.9.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.8.0...v0.9.0) (2023-10-18)


### ⚠ BREAKING CHANGES

* rename `bigframes.pandas.reset_session` to `close_session` ([#101](https://github.com/googleapis/python-bigquery-dataframes/issues/101))

### Features

* Add `bigframes.options.bigquery.application_name` for partner attribution ([#117](https://github.com/googleapis/python-bigquery-dataframes/issues/117)) ([52d64ff](https://github.com/googleapis/python-bigquery-dataframes/commit/52d64ffdbbab16b1d94974b543ce9080be1ec0d1))
* Add AtIndexer getitems ([#107](https://github.com/googleapis/python-bigquery-dataframes/issues/107)) ([752b01f](https://github.com/googleapis/python-bigquery-dataframes/commit/752b01ff9df114c54ed58eb96956e9ce34a8ed47))
* Rename `bigframes.pandas.reset_session` to `close_session` ([#101](https://github.com/googleapis/python-bigquery-dataframes/issues/101)) ([36693bf](https://github.com/googleapis/python-bigquery-dataframes/commit/36693bff398c23e179d9bde95d52cbaddaf85c45))
* Send BigQuery cancel request when canceling bigframes process ([#103](https://github.com/googleapis/python-bigquery-dataframes/issues/103)) ([e325fbb](https://github.com/googleapis/python-bigquery-dataframes/commit/e325fbb1c91e040d87df10f7d4d5ce53f7c052cb))
* Support external packages in `remote_function` ([#98](https://github.com/googleapis/python-bigquery-dataframes/issues/98)) ([ec10c4a](https://github.com/googleapis/python-bigquery-dataframes/commit/ec10c4a5a7833c42e28fe9e7b734bc0c4fb84b6e))
* Use ArrowDtype for STRUCT columns in `to_pandas` ([#85](https://github.com/googleapis/python-bigquery-dataframes/issues/85)) ([9238fad](https://github.com/googleapis/python-bigquery-dataframes/commit/9238fadcfa7e843be6564813ff3131893b79f8b0))


### Bug Fixes

* Support multiindex for three loc getitem overloads ([#113](https://github.com/googleapis/python-bigquery-dataframes/issues/113)) ([68e3cd3](https://github.com/googleapis/python-bigquery-dataframes/commit/68e3cd37258084d045ea1075e5e61df12c28faac))


### Performance Improvements

* If primary keys are defined, `read_gbq` avoids copying table data ([#112](https://github.com/googleapis/python-bigquery-dataframes/issues/112)) ([e6c0cd1](https://github.com/googleapis/python-bigquery-dataframes/commit/e6c0cd1777736e0fa7285da59625fbac487573bd))


### Documentation

* Add documentation for `Series.struct.field` and `Series.struct.explode` ([#114](https://github.com/googleapis/python-bigquery-dataframes/issues/114)) ([a6dab9c](https://github.com/googleapis/python-bigquery-dataframes/commit/a6dab9cdb7dd0e56c93ca96b665ab1be1baac5e5))
* Add open-source link in API doc ([#106](https://github.com/googleapis/python-bigquery-dataframes/issues/106)) ([db51fe3](https://github.com/googleapis/python-bigquery-dataframes/commit/db51fe340f644a0d7c911c11d92c8299a4be3446))
* Update ML overview API doc ([#105](https://github.com/googleapis/python-bigquery-dataframes/issues/105)) ([1b3f3a5](https://github.com/googleapis/python-bigquery-dataframes/commit/1b3f3a5374915b2833c6c1ac05670e9708f07bff))

## [0.8.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.7.0...v0.8.0) (2023-10-12)


### ⚠ BREAKING CHANGES

* The default behavior of `to_parquet` is changing from no compression to `'snappy'` compression.

### Features

* Support compression in `to_parquet` ([a8c286f](https://github.com/googleapis/python-bigquery-dataframes/commit/a8c286f0995cc8cf2a4c44fb51855773ecf71f72))


### Bug Fixes

* Create session dataset for remote functions only when needed ([#94](https://github.com/googleapis/python-bigquery-dataframes/issues/94)) ([1d385be](https://github.com/googleapis/python-bigquery-dataframes/commit/1d385be1c68342a66ecb9f28c5efc83c18d0e64c))

## [0.7.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.6.0...v0.7.0) (2023-10-11)


### Features

* Add aliases for several series properties ([#80](https://github.com/googleapis/python-bigquery-dataframes/issues/80)) ([c0efec8](https://github.com/googleapis/python-bigquery-dataframes/commit/c0efec8956198247b27904345a795f09c80d3502))
* Add equals methods to series/dataframe ([#76](https://github.com/googleapis/python-bigquery-dataframes/issues/76)) ([636a209](https://github.com/googleapis/python-bigquery-dataframes/commit/636a209e0853501abd50784a11a87cf7f2282ee5))
* Add iat and iloc accessing by tuples of integers ([#90](https://github.com/googleapis/python-bigquery-dataframes/issues/90)) ([228aeba](https://github.com/googleapis/python-bigquery-dataframes/commit/228aeba09782ae2421040c7601c15d4af92790b6))
* Add level param to DataFrame.stack ([#88](https://github.com/googleapis/python-bigquery-dataframes/issues/88)) ([97b8bec](https://github.com/googleapis/python-bigquery-dataframes/commit/97b8bec1175499c74448a4fd46b4888c4b4c35c1))
* Allow df.drop to take an index object ([#68](https://github.com/googleapis/python-bigquery-dataframes/issues/68)) ([740c451](https://github.com/googleapis/python-bigquery-dataframes/commit/740c45176f79d4d2f7f28cb5f6c9eeb1327c8397))
* Use default session connection ([#87](https://github.com/googleapis/python-bigquery-dataframes/issues/87)) ([4ae4ef9](https://github.com/googleapis/python-bigquery-dataframes/commit/4ae4ef995348b95521c4988a8cfb3b5ac792fd69))


### Bug Fixes

* Change the invalid url in docs ([#93](https://github.com/googleapis/python-bigquery-dataframes/issues/93)) ([969800d](https://github.com/googleapis/python-bigquery-dataframes/commit/969800d669204de4d0f2e5e61da521217e55668b))


### Documentation

* Add more preprocessing models into the docs menu. ([#97](https://github.com/googleapis/python-bigquery-dataframes/issues/97)) ([1592315](https://github.com/googleapis/python-bigquery-dataframes/commit/159231505f339173560cd802dae3fed3e63a663b))

## [0.6.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.5.0...v0.6.0) (2023-10-04)


### Features

* Add df.unstack ([#63](https://github.com/googleapis/python-bigquery-dataframes/issues/63)) ([4a84714](https://github.com/googleapis/python-bigquery-dataframes/commit/4a84714e2fb07f70c70c79f8b8da9fcb41096e33))
* Add idxmin, idxmax to series, dataframe ([#74](https://github.com/googleapis/python-bigquery-dataframes/issues/74)) ([781307e](https://github.com/googleapis/python-bigquery-dataframes/commit/781307ec22d31a7657f8ee5c6eedc0e419450ccd))
* Add ml.preprocessing.KBinsDiscretizer ([#81](https://github.com/googleapis/python-bigquery-dataframes/issues/81)) ([24c6256](https://github.com/googleapis/python-bigquery-dataframes/commit/24c625638984f6a84191c7a4c8ac9fb6c3cf1dca))
* Add multi-column dataframe merge ([#73](https://github.com/googleapis/python-bigquery-dataframes/issues/73)) ([c9fa85c](https://github.com/googleapis/python-bigquery-dataframes/commit/c9fa85cc338be5e9a8dde59b255690aedbbc1127))
* Add update and align methods to dataframe ([#57](https://github.com/googleapis/python-bigquery-dataframes/issues/57)) ([bf050cf](https://github.com/googleapis/python-bigquery-dataframes/commit/bf050cf475ad8a9e3e0ca3f896ddaf96dbe13ae3))
* Support STRUCT data type with `Series.struct.field` to extract child fields ([#71](https://github.com/googleapis/python-bigquery-dataframes/issues/71)) ([17afac9](https://github.com/googleapis/python-bigquery-dataframes/commit/17afac9ff70a2b93ed70dc7bcce7beb9a53c2ece))


### Bug Fixes

* Avoid `403 response too large to return` error with `read_gbq` and large query results ([#77](https://github.com/googleapis/python-bigquery-dataframes/issues/77)) ([8f3b5b2](https://github.com/googleapis/python-bigquery-dataframes/commit/8f3b5b240f0f28fef92465abc53504e875d7335a))
* Change return type of `Series.loc[scalar]` ([#40](https://github.com/googleapis/python-bigquery-dataframes/issues/40)) ([fff3d45](https://github.com/googleapis/python-bigquery-dataframes/commit/fff3d45f03ffbc7bb23143a1572e3dd157463ca9))
* Fix df/series.iloc by list with multiindex ([#79](https://github.com/googleapis/python-bigquery-dataframes/issues/79)) ([971d091](https://github.com/googleapis/python-bigquery-dataframes/commit/971d091cac9ad662145a3d43d8f9a785eb0ccc23))

## [0.5.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.4.0...v0.5.0) (2023-09-28)


### Features

* Add `DataFrame.kurtosis` / `DF.kurt` method ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Add `DataFrame.rolling` and `DataFrame.expanding` methods ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Add `items`, `apply` methods to `DataFrame`. ([#43](https://github.com/googleapis/python-bigquery-dataframes/issues/43)) ([3adc1b3](https://github.com/googleapis/python-bigquery-dataframes/commit/3adc1b3aa3e2b218d4fa5debdaa4298276bdf801))
* Add axis param to simple df aggregations ([#52](https://github.com/googleapis/python-bigquery-dataframes/issues/52)) ([9cf9972](https://github.com/googleapis/python-bigquery-dataframes/commit/9cf99721ed83704e6ee28b15c699326c431eb252))
* Add index `dtype`, `astype`, `drop`, `fillna`, aggregate attributes. ([#38](https://github.com/googleapis/python-bigquery-dataframes/issues/38)) ([1a254a4](https://github.com/googleapis/python-bigquery-dataframes/commit/1a254a496633957b9506dd8392dcc6fd10762201))
* Add ml.preprocessing.LabelEncoder ([#50](https://github.com/googleapis/python-bigquery-dataframes/issues/50)) ([2510461](https://github.com/googleapis/python-bigquery-dataframes/commit/25104610e5ffe526315923946533a66713c1d155))
* Add ml.preprocessing.MaxAbsScaler ([#56](https://github.com/googleapis/python-bigquery-dataframes/issues/56)) ([14b262b](https://github.com/googleapis/python-bigquery-dataframes/commit/14b262bde2bb86093bf4df63862e369c5a84b0ad))
* Add ml.preprocessing.MinMaxScaler ([#64](https://github.com/googleapis/python-bigquery-dataframes/issues/64)) ([392113b](https://github.com/googleapis/python-bigquery-dataframes/commit/392113b70d6a8c407accbb6684d75b31261e3741))
* Add more index methods ([#54](https://github.com/googleapis/python-bigquery-dataframes/issues/54)) ([a6e32aa](https://github.com/googleapis/python-bigquery-dataframes/commit/a6e32aa875370063c48ce7922c2aa369a770bd30))
* Support `calculate_p_values` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `class_weights="balanced"` in `LogisticRegression` model ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `df[column_name] = df_only_one_column` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `early_stop` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `enable_global_explain` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `l2_reg` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `learn_rate_strategy` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `ls_init_learn_rate` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `max_iterations` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `min_rel_progress` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support `optimize_strategy` parameter in `bigframes.ml.linear_model.LinearRegression` ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))
* Support casting string to integer or float ([#59](https://github.com/googleapis/python-bigquery-dataframes/issues/59)) ([3502f83](https://github.com/googleapis/python-bigquery-dataframes/commit/3502f835b35c437933430698e7a1c9badaddcb99))


### Bug Fixes

* Fix header skipping logic in `read_csv` ([#49](https://github.com/googleapis/python-bigquery-dataframes/issues/49)) ([d56258c](https://github.com/googleapis/python-bigquery-dataframes/commit/d56258cbfcda168cb9e437a021e282818d622d6a))
* Generate unique ids on join to avoid id collisions ([#65](https://github.com/googleapis/python-bigquery-dataframes/issues/65)) ([7ab65e8](https://github.com/googleapis/python-bigquery-dataframes/commit/7ab65e88deb0080e9c36c2709f8a5385ccaf8cf2))
* LabelEncoder params consistent with Sklearn ([#60](https://github.com/googleapis/python-bigquery-dataframes/issues/60)) ([632caec](https://github.com/googleapis/python-bigquery-dataframes/commit/632caec420a7e23188f01b96a00c354d205da74e))
* Loosen filter items tests to accomodate shifting pandas impl ([#41](https://github.com/googleapis/python-bigquery-dataframes/issues/41)) ([edabdbb](https://github.com/googleapis/python-bigquery-dataframes/commit/edabdbb131150707ea9211292cacbb60b8d076dd))


### Performance Improvements

* Add ability to cache dataframe and series to session table ([#51](https://github.com/googleapis/python-bigquery-dataframes/issues/51)) ([416d7cb](https://github.com/googleapis/python-bigquery-dataframes/commit/416d7cb9b560d7e33dcc0227f03a00d43f55ba0d))
* Inline small `Series` and `DataFrames` in query text ([#45](https://github.com/googleapis/python-bigquery-dataframes/issues/45)) ([5e199ec](https://github.com/googleapis/python-bigquery-dataframes/commit/5e199ecf1ecf13a68a2ed0dd4464afd9db977ab1))
* Reimplement unpivot to use cross join rather than union ([#47](https://github.com/googleapis/python-bigquery-dataframes/issues/47)) ([f9a93ce](https://github.com/googleapis/python-bigquery-dataframes/commit/f9a93ce71d053aa17b1e3a2946c90e0227076184))
* Simplify join order to use multiple order keys instead of string. ([#36](https://github.com/googleapis/python-bigquery-dataframes/issues/36)) ([5056da6](https://github.com/googleapis/python-bigquery-dataframes/commit/5056da6b385dbcfc179d2bcbb6549fa539428cda))


### Documentation

* Link to Remote Functions code samples from README and API reference ([c1900c2](https://github.com/googleapis/python-bigquery-dataframes/commit/c1900c29a44199d5d8d036d6d842b4f00448fa79))

## [0.4.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.3.2...v0.4.0) (2023-09-16)


### Features

* Add `axis` parameter to `droplevel` and `reorder_levels` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `bfill` and `ffill` to `DataFrame` and `Series` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `DataFrame.combine` and `DataFrame.combine_first` ([#27](https://github.com/googleapis/python-bigquery-dataframes/issues/27)) ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `DataFrame.nlargest`, `nsmallest` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `DataFrame.pct_change` and `Series.pct_change` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `DataFrame.skew` and `GroupBy.skew` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `DataFrame.to_dict`, `to_excel`, `to_latex`, `to_records`, `to_string`, `to_markdown`, `to_pickle`, `to_orc` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `diff` method to `DataFrame` and `GroupBy` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `filter` and `reindex` to `Series` and `DataFrame` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `reindex_like` to `DataFrame` and `Series` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add `swaplevel` to `DataFrame` and `Series` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add partial support for `Sereies.replace` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Support `DataFrame.loc[bool_series, column] = scalar` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Support a persistent `name` in `remote_function` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))


### Bug Fixes

* `remote_function` uses same credentials as other APIs ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Add type hints to models ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Raise error when ARIMAPlus is used with Pipeline ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Remove `transforms` parameter in `model.fit` (**breaking change**) ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Support column joins with "None indexer" ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Use for literals `Int64Dtype` in `cut` ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Use lowercase strings for parameter literals in `bigframes.ml` (**breaking change**) ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))


### Performance Improvements

* `bigframes-api` label to I/O query jobs ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))


### Documentation

* Document possible parameter values for PaLM2TextGenerator ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Document region logic in README ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))
* Fix OneHotEncoder sample ([7c6b0dd](https://github.com/googleapis/python-bigquery-dataframes/commit/7c6b0dd2f99139c8830e762201a45b28486532ff))

## [0.3.2](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.3.1...v0.3.2) (2023-09-06)


### Bug Fixes

* Make release.sh script for PyPI upload executable ([#20](https://github.com/googleapis/python-bigquery-dataframes/issues/20)) ([9951610](https://github.com/googleapis/python-bigquery-dataframes/commit/995161068b118a639903878acfde3202087c25f8))

## [0.3.1](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.3.0...v0.3.1) (2023-09-05)


### Bug Fixes

* **release:** Use correct directory name for release build config ([#17](https://github.com/googleapis/python-bigquery-dataframes/issues/17)) ([3dd25b3](https://github.com/googleapis/python-bigquery-dataframes/commit/3dd25b379ed832ea062e188f483d2789830de67b))

## [0.3.0](https://github.com/googleapis/python-bigquery-dataframes/compare/v0.2.0...v0.3.0) (2023-09-02)


### Features

* Add `bigframes.get_global_session()` and `bigframes.reset_session()` aliases ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `bigframes.pandas.read_pickle` function ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `components_`, `explained_variance_`, and `explained_variance_ratio_` properties to `bigframes.ml.decomposition.PCA` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Add `fit_transform` to `bigquery.ml` transformers ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add `Series.dropna` and `DataFrame.fillna` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Add `Series.str` methods `isalpha`, `isdigit`, `isdecimal`, `isalnum`, `isspace`, `islower`, `isupper`, `zfill`, `center` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support `bigframes.pandas.merge()` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `DataFrame.isin` with list and dict inputs ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `DataFrame.pivot` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support `DataFrame.stack` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `DataFrame`-`DataFrame` binary operations ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `df[my_column] = [a python list]` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Index.is_monotonic` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `np.arcsin`, `np.arccos`, `np.arctan`, `np.sinh`, `np.cosh`, `np.tanh`, `np.arcsinh`, `np.arccosh`, `np.arctanh`, `np.exp` with Series argument ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `np.sin`, `np.cos`, `np.tan`, `np.log`, `np.log10`, `np.sqrt`, `np.abs` with Series argument ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `pow()` and power operator in `DataFrame` and `Series` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support `read_json` with `engine=bigquery` for newline-delimited JSON files ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Series.corr` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Support `Series.map` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support for `np.add`, `np.subtract`, `np.multiply`, `np.divide`, `np.power` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Support MultiIndex for DataFrame columns ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Use `pandas.Index` for column labels ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Use default session and connection in `ml.llm` and `ml.imported` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))


### Bug Fixes

* Add error message to `set_index` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Align column names with pandas in `DataFrame.agg` results ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Allow (but still not recommended) `ORDER BY` in `read_gbq` input when an `index_col` is defined ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Check for IAM role on the BigQuery connection when initializing a `remote_function` ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Check that types are specified in `read_gbq_function` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Don't use query cache for Session construction ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Include survey link in abstract `NotImplementedError` exception messages ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Label temp table creation jobs with `source=bigquery-dataframes-temp` label ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Make `X_train` argument names consistent across methods ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))
* Raise AttributeError for unimplemented pandas methods ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Raise exception for invalid function in `read_gbq_function` ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Support spaces in column names in `DataFrame` initializater ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))


### Performance Improvements

* Add local cache for `__repr_*__` methods ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Lazily instantiate client library objects ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Use `row_number()` filter for `head` / `tail` ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))


### Documentation

* Add ML section under Overview ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add release status to table of contents ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Add samples and best practices to `read_gbq` docs ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Correct the return types of Dataframe and Series ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Create subfolders for notebooks ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Fix link to GitHub ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Highlight bigframes is open-source ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Sample ML Drug Name Generation notebook ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Set `options.bigquery.project` in sample code ([89b9503](https://github.com/googleapis/python-bigquery-dataframes/commit/89b95033d6b449bfc21249057d7c024d096c80d0))
* Transform remote function user guide into sample code ([a32b747](https://github.com/googleapis/python-bigquery-dataframes/commit/a32b74751785c8e8aec40ce01df639dd7c4fbb77))
* Update remote function notebook with read_gbq_function usage ([8fab755](https://github.com/googleapis/python-bigquery-dataframes/commit/8fab75576757230bca5c7df10994837ac406300f))

## 0.2.0 (2023-08-17)

### Features
* Add KMeans.cluster_centers_.
* Allow column labels to be any type handled by bq df, column labels can be integers now.
* Add dataframegroupby.agg().
* Add Series Property is_monotonic_increasing and is_monotonic_decreasing.
* Add match, fullmatch, get, pad str methods.
* Add series isin function.

### Bug Fixes
* Update ML package to use sessions for queries.
* Optimize `read_gbq` with `index_col` set to cluster by `index_col`.
* Raise ValueError if the location mismatched.
* `read_gbq` no longer uses 'time travel' with query inputs.

### Documentation
* Add docstring to _uniform_sampling to avoid user using it.

## 0.1.1 (2023-08-14)

### Documentation

* Correct link to code repository in `setup.py` and use correct terminology for
  `console.cloud.google.com` links.

## 0.1.0 (2023-08-11)

### Features

* Add `bigframes.pandas` package with an API compatible with
  [pandas](https://pandas.pydata.org/). Supported data sources include:
  BigQuery SQL queries, BigQuery tables, CSV (local and GCS), Parquet (local
  and Cloud Storage), and more.
* Add `bigframes.ml` package with an API inspired by
  [scikit-learn](https://scikit-learn.org/stable/). Train machine learning
  models and run batch predicition, powered by [BigQuery
  ML](https://cloud.google.com/bigquery/docs/bqml-introduction).

## [0.0.0](https://pypi.org/project/bigframes/0.0.0/) (2023-02-22)

* Empty package to reserve package name.
