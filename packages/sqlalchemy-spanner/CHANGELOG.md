# Changelog

## [1.6.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.5.0...v1.6.0) (2023-04-26)


### Features

* Enable instance-level connection ([#316](https://github.com/googleapis/python-spanner-sqlalchemy/issues/316)) ([9af8e86](https://github.com/googleapis/python-spanner-sqlalchemy/commit/9af8e863f7fb0fa8bea050ca022bbe4e05315d6d))

## [1.5.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.4.0...v1.5.0) (2023-04-19)


### Features

* Feat: SQLAlchemy 2.0 support ([#314](https://github.com/googleapis/python-spanner-sqlalchemy/issues/314)) ([61d836b](https://github.com/googleapis/python-spanner-sqlalchemy/commit/61d836bade2a89d04b5c61e4ca9c56e7163f6cc6))

## [1.4.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.3.0...v1.4.0) (2023-04-06)


### Features

* User provided client ([#311](https://github.com/googleapis/python-spanner-sqlalchemy/issues/311)) ([5b07111](https://github.com/googleapis/python-spanner-sqlalchemy/commit/5b0711102bb45f5775addbda61cb4da5231c96d7))

## [1.3.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.2.2...v1.3.0) (2023-03-20)


### Features

* Implement get_view_names() method ([#306](https://github.com/googleapis/python-spanner-sqlalchemy/issues/306)) ([63461e6](https://github.com/googleapis/python-spanner-sqlalchemy/commit/63461e67364b5214e7ea8a2d89c0fda4d9ced72d)), closes [#303](https://github.com/googleapis/python-spanner-sqlalchemy/issues/303)
* Support request priorities ([#286](https://github.com/googleapis/python-spanner-sqlalchemy/issues/286)) ([3aecf2d](https://github.com/googleapis/python-spanner-sqlalchemy/commit/3aecf2d651e6eb9f3af72a3ed3599aa51b4158a9))


### Bug Fixes

* Alembic incompatibility with sqlalchemy &lt; 1.3.11 ([#290](https://github.com/googleapis/python-spanner-sqlalchemy/issues/290)) ([f99f3a7](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f99f3a78477aecc71af70deba41b861e12d51c28))
* Introspect constraints, keeping their order ([#289](https://github.com/googleapis/python-spanner-sqlalchemy/issues/289)) ([7f65972](https://github.com/googleapis/python-spanner-sqlalchemy/commit/7f659729e15848c1493cb271e832b6968d7ab031))
* Test fix ([#310](https://github.com/googleapis/python-spanner-sqlalchemy/issues/310)) ([c376d42](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c376d422ab455ee88bb94e2cd136aa9ef865e375))

## [1.2.2](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.2.1...v1.2.2) (2022-10-04)


### Bug Fixes

* Adding requirements ([#250](https://github.com/googleapis/python-spanner-sqlalchemy/issues/250)) ([61a13d4](https://github.com/googleapis/python-spanner-sqlalchemy/commit/61a13d4ba152a24d5fa6083594aa86f46d5395de))
* Don't introspect internal UNIQUE constraints ([#244](https://github.com/googleapis/python-spanner-sqlalchemy/issues/244)) ([51cdc53](https://github.com/googleapis/python-spanner-sqlalchemy/commit/51cdc534856b5ab933213803257679faa33be41c))
* Spanner auto managed indexes should not be introspected ([#241](https://github.com/googleapis/python-spanner-sqlalchemy/issues/241)) ([c3b5907](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c3b59077ff8d6d8916007bf204f90e1d1ed41c00))
* Update dialect name for ALTER operation overrides ([#234](https://github.com/googleapis/python-spanner-sqlalchemy/issues/234)) ([f9e8ebe](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f9e8ebedc863b2b84b2decffc1831125001785c8))


### Documentation

* Add auto retry mechanism explanation ([#243](https://github.com/googleapis/python-spanner-sqlalchemy/issues/243)) ([68b9bc8](https://github.com/googleapis/python-spanner-sqlalchemy/commit/68b9bc8b389c29451317cf78989578e0a7369dad))
* Mention autocommit_block as a solution for Aborted transaction … ([#239](https://github.com/googleapis/python-spanner-sqlalchemy/issues/239)) ([f23e599](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f23e599ef6a9d8f198c41f32a586e42af840280d)), closes [#229](https://github.com/googleapis/python-spanner-sqlalchemy/issues/229)
* Mention package install with pip ([#245](https://github.com/googleapis/python-spanner-sqlalchemy/issues/245)) ([528a9b0](https://github.com/googleapis/python-spanner-sqlalchemy/commit/528a9b0ba1bb9f0b96e35c809faa923f292684a0))

## [1.2.1](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.2.0...v1.2.1) (2022-08-09)


### Bug Fixes

* alembic migration fails in case of a sequential upgrade ([#200](https://github.com/googleapis/python-spanner-sqlalchemy/issues/200)) ([f62f664](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f62f664f31ec052068e241729344aec5f605c4f8))
* don't reset attributes of non-Spanner connections ([#222](https://github.com/googleapis/python-spanner-sqlalchemy/issues/222)) ([072415e](https://github.com/googleapis/python-spanner-sqlalchemy/commit/072415eb9ea0bf701be2a35c4cc3dc80854ca831))
* incorrect DDL generated when using server_default ([#209](https://github.com/googleapis/python-spanner-sqlalchemy/issues/209)) ([#220](https://github.com/googleapis/python-spanner-sqlalchemy/issues/220)) ([7ab1742](https://github.com/googleapis/python-spanner-sqlalchemy/commit/7ab174233dc75fd34d4127cb06dd49c216d92abc))


### Documentation

* add a note about connection URL prefixes ([#219](https://github.com/googleapis/python-spanner-sqlalchemy/issues/219)) ([a986949](https://github.com/googleapis/python-spanner-sqlalchemy/commit/a9869498f220a529a1dcc51c89d53af54311074c))

## [1.2.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.1.0...v1.2.0) (2022-06-03)


### Features

* allow SQLAlchemy 1.4 use ([#198](https://github.com/googleapis/python-spanner-sqlalchemy/issues/198)) ([7793b7d](https://github.com/googleapis/python-spanner-sqlalchemy/commit/7793b7ddfcbd99e966e3ef6f7ec13d7dc04d39fb))

## [1.1.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.0.0...v1.1.0) (2022-01-28)


### Features

* drop read_only on a connection returned back to a pool ([#189](https://github.com/googleapis/python-spanner-sqlalchemy/issues/189)) ([16388c1](https://github.com/googleapis/python-spanner-sqlalchemy/commit/16388c1c9ba7798c0c0df786f2e4a8c86b7767c2))
* rollback a connection returned back to pool ([#193](https://github.com/googleapis/python-spanner-sqlalchemy/issues/193)) ([13ff9cb](https://github.com/googleapis/python-spanner-sqlalchemy/commit/13ff9cb73049d989bacb97fd8be3ad3bdce7023c))
* support SQLAlchemy 1.4 ([#191](https://github.com/googleapis/python-spanner-sqlalchemy/issues/191)) ([029b181](https://github.com/googleapis/python-spanner-sqlalchemy/commit/029b18109c1ff21318c3820da5aa0945b6d6325d))


### Bug Fixes

* bump up google-cloud-spanner required version ([#171](https://github.com/googleapis/python-spanner-sqlalchemy/issues/171)) ([33c86e8](https://github.com/googleapis/python-spanner-sqlalchemy/commit/33c86e8fdeac4fd65569c438e8613dcb86e15edc))
* connection reset fails when an additional dialect is used ([#188](https://github.com/googleapis/python-spanner-sqlalchemy/issues/188)) ([417b8b8](https://github.com/googleapis/python-spanner-sqlalchemy/commit/417b8b81911417ee3a1f826c37a9e490641944ac))
* delete stale instance with delay of 5 seconds ([#194](https://github.com/googleapis/python-spanner-sqlalchemy/issues/194)) ([2932a02](https://github.com/googleapis/python-spanner-sqlalchemy/commit/2932a02bb58c4e2800da1e18452babcfc74617d6))
* NOT NULL computed column creation failure ([#173](https://github.com/googleapis/python-spanner-sqlalchemy/issues/173)) ([e336735](https://github.com/googleapis/python-spanner-sqlalchemy/commit/e3367354d3b24328d7162fd2ccc778f23c630cd2))


### Documentation

* add a README section for the autoincremented ids ([#180](https://github.com/googleapis/python-spanner-sqlalchemy/issues/180)) ([4c610ea](https://github.com/googleapis/python-spanner-sqlalchemy/commit/4c610eaecd32679f23cae2f70d299d3c3d33d024))
* explicitly recommend uuid to generate PKs ([#182](https://github.com/googleapis/python-spanner-sqlalchemy/issues/182)) ([b10f2ca](https://github.com/googleapis/python-spanner-sqlalchemy/commit/b10f2cae0eb13eb5496d08cbeae77a626b4ad6f1)), closes [#181](https://github.com/googleapis/python-spanner-sqlalchemy/issues/181)

## [1.0.0](https://www.github.com/googleapis/python-spanner-sqlalchemy/compare/v0.1.0...v1.0.0) (2021-12-08)


### Features

* add code samples ([#55](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/55)) ([406c34b](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/406c34bdb21e01a1317c074fab34d87bb3d61020))
* set user-agent string to distinguish SQLAlchemy requests ([#116](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/116)) ([b5e1a21](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/b5e1a211a0475690feed36fd222a41c216d8fb82))
* support computed columns ([#139](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/139)) ([046ca97](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/046ca975778f4793e2c37d70d2a602546f9d4699)), closes [#137](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/137)
* support JSON data type ([#135](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/135)) ([184a7d5](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/184a7d576a790bbbd049fe80d589af78831379b4))
* support read_only connections ([#125](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/125)) ([352c47d](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/352c47de7bb4ea1c30b50a7fe5aee0c4d102e80e))
* support stale reads ([#146](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/146)) ([d80cb27](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/d80cb2792437731c24905c7a6919468c37779c67))


### Bug Fixes

* ALTER COLUMN NOT NULL directive fails because of inappropriate syntax ([#124](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/124)) ([c433cda](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/c433cda99fd8544810c878328a272a3a9430630f))
* array columns reflection ([#119](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/119)) ([af3b97b](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/af3b97bfa4b3ed4b223384c9ed3fa0643204d8c9)), closes [#118](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/118)
* calculate limit value correctly for offset only queries ([#160](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/160)) ([6844336](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/684433682ed29d9cde8c9898796024cefeb38493))
* correct typo in spanner_interleave_on_delete_cascade keyword ([#99](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/99)) ([a0ebf75](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/a0ebf758eda351c0a20103f9e8c2243f002b2e6e))
* raise Unimplemented error when creating temporary tables ([#159](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/159)) ([646d6ac](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/646d6ac24ccd0643b67abff9da28118e0a6f6e55))
* rollback failed exception log ([#106](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/106)) ([809e6ab](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/809e6abb29f82a7fbe6587d606e8d75283f2a2fe))


### Documentation

* add query hints example ([#153](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/153)) ([9c23804](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/9c23804746bc8c638b6c22f2cb6ea57778f7fd19))
* reformatted README titles ([#141](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/141)) ([a3ccbac](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/a3ccbac476679fe8048ed2109e5489b873278c9c))
* update benchmarks ([#155](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/155)) ([3500653](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/35006536e4de31dbcba022b73f0aadf39bc89e39))


### Miscellaneous Chores

* setup release 1.0.0 ([#165](https://www.github.com/googleapis/python-spanner-sqlalchemy/issues/165)) ([37a415d](https://www.github.com/googleapis/python-spanner-sqlalchemy/commit/37a415d071d39e99f233a1c15c1c4b89bd436570))
