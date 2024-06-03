# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigframes/#history

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
