# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigframes/#history

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
