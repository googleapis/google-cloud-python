# Changelog

## [1.17.1](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.17.0...v1.17.1) (2025-10-21)


### Bug Fixes

* Return Correct Column Order in get_multi_foreign_keys ([#783](https://github.com/googleapis/python-spanner-sqlalchemy/issues/783)) ([42027d5](https://github.com/googleapis/python-spanner-sqlalchemy/commit/42027d56abe3b3e87faece03f4ade84b9703acd6)), closes [#779](https://github.com/googleapis/python-spanner-sqlalchemy/issues/779)

## [1.17.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.16.0...v1.17.0) (2025-10-09)


### Features

* Add Support for Interleaved Indexes ([#762](https://github.com/googleapis/python-spanner-sqlalchemy/issues/762)) ([77b86f1](https://github.com/googleapis/python-spanner-sqlalchemy/commit/77b86f1ad9d31932c960497eb1fb29635b74cb92)), closes [#761](https://github.com/googleapis/python-spanner-sqlalchemy/issues/761)

## [1.16.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.15.0...v1.16.0) (2025-09-02)


### Features

* Support NULL FILTERED indexes ([#750](https://github.com/googleapis/python-spanner-sqlalchemy/issues/750)) ([4bc0589](https://github.com/googleapis/python-spanner-sqlalchemy/commit/4bc05898995a586816e116e0a3205966a52d1ef8))


### Documentation

* Add sample for parse_json ([#752](https://github.com/googleapis/python-spanner-sqlalchemy/issues/752)) ([b2f0e89](https://github.com/googleapis/python-spanner-sqlalchemy/commit/b2f0e89b8f01481fa6f29da055300eeb533591cc)), closes [#735](https://github.com/googleapis/python-spanner-sqlalchemy/issues/735)

## [1.15.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.14.0...v1.15.0) (2025-08-19)


### Features

* Add license metadata to setup.py ([#712](https://github.com/googleapis/python-spanner-sqlalchemy/issues/712)) ([8f2e97e](https://github.com/googleapis/python-spanner-sqlalchemy/commit/8f2e97e527b00bfb6db40d946a21f522177eab7b))
* Enable SQLAlchemy 2.0's insertmany feature ([#721](https://github.com/googleapis/python-spanner-sqlalchemy/issues/721)) ([1fe9f4b](https://github.com/googleapis/python-spanner-sqlalchemy/commit/1fe9f4b0a2f94d66c925d1d60a1fd83fc45e9c89))
* Support informational foreign keys ([#719](https://github.com/googleapis/python-spanner-sqlalchemy/issues/719)) ([c565ae1](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c565ae12b1b429c66037e9cd0c4be427a60ab5b0))


### Bug Fixes

* Report column defaults in introspection ([#744](https://github.com/googleapis/python-spanner-sqlalchemy/issues/744)) ([309c641](https://github.com/googleapis/python-spanner-sqlalchemy/commit/309c64179d668dbe24881e6d7fb4783fb1d8bbf2)), closes [#730](https://github.com/googleapis/python-spanner-sqlalchemy/issues/730)
* Respect existing server default in alter column DDL ([#733](https://github.com/googleapis/python-spanner-sqlalchemy/issues/733)) ([1f8a25f](https://github.com/googleapis/python-spanner-sqlalchemy/commit/1f8a25f63286c1241141985d4f10f558e929a272))

## [1.14.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.13.1...v1.14.0) (2025-06-27)


### Features

* Support commit timestamp option ([#697](https://github.com/googleapis/python-spanner-sqlalchemy/issues/697)) ([82bb8ed](https://github.com/googleapis/python-spanner-sqlalchemy/commit/82bb8ed583a5fd91c8a10fb73c85a6a5f45269f6))

## [1.13.1](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.13.0...v1.13.1) (2025-06-20)


### Bug Fixes

* Support retrieval of cross-schema foreign keys ([ef07a1f](https://github.com/googleapis/python-spanner-sqlalchemy/commit/ef07a1f55736eae9751f85fef66599fdfa21bcd4)), closes [#638](https://github.com/googleapis/python-spanner-sqlalchemy/issues/638)

## [1.13.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.12.0...v1.13.0) (2025-06-05)


### Features

* Introduce compatibility with native namespace packages ([#375](https://github.com/googleapis/python-spanner-sqlalchemy/issues/375)) ([052e699](https://github.com/googleapis/python-spanner-sqlalchemy/commit/052e699f82a795def518f4f0a32039e1c68174a0))

## [1.12.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.11.1...v1.12.0) (2025-06-02)


### Features

* Document the use of statement and transaction tags ([#676](https://github.com/googleapis/python-spanner-sqlalchemy/issues/676)) ([c78ad04](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c78ad04dc7a3e1c773bde21ef927d5250f47992d))
* Support database role in connect arguments ([#667](https://github.com/googleapis/python-spanner-sqlalchemy/issues/667)) ([47aa27c](https://github.com/googleapis/python-spanner-sqlalchemy/commit/47aa27c489cb7051cb55468ab4d6b79f8c0ce1f3))
* Support multi-row inserts ([#671](https://github.com/googleapis/python-spanner-sqlalchemy/issues/671)) ([f5d94cd](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f5d94cd15cba43684fc584072018ab3bc826f457)), closes [#670](https://github.com/googleapis/python-spanner-sqlalchemy/issues/670)

## [1.11.1](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.11.0...v1.11.1) (2025-05-27)


### Bug Fixes

* Update README to include isolation level repeatable read ([#668](https://github.com/googleapis/python-spanner-sqlalchemy/issues/668)) ([d84daf6](https://github.com/googleapis/python-spanner-sqlalchemy/commit/d84daf65a496bdff6f5d9e835490785c69533238))

## [1.11.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.10.0...v1.11.0) (2025-05-07)


### Features

* Add isolation level support and sample ([#652](https://github.com/googleapis/python-spanner-sqlalchemy/issues/652)) ([0aba318](https://github.com/googleapis/python-spanner-sqlalchemy/commit/0aba31835bc581a0a05e29b5878ba0a665686414))
* Add SpannerPickleType ([#655](https://github.com/googleapis/python-spanner-sqlalchemy/issues/655)) ([0837542](https://github.com/googleapis/python-spanner-sqlalchemy/commit/0837542e5606ab9ea7a8765bf54524ebf9b0dd71)), closes [#654](https://github.com/googleapis/python-spanner-sqlalchemy/issues/654)
* Support schemas in queries and dml statements ([#639](https://github.com/googleapis/python-spanner-sqlalchemy/issues/639)) ([81c154a](https://github.com/googleapis/python-spanner-sqlalchemy/commit/81c154a37b82315a8bb57319ba11272626addad3))


### Bug Fixes

* Column order in get_multi_pk_constraint ([#640](https://github.com/googleapis/python-spanner-sqlalchemy/issues/640)) ([16c87e4](https://github.com/googleapis/python-spanner-sqlalchemy/commit/16c87e4fbf1b9d5dbac0e3279cce078a2d09e4b4))
* Include schema when creating indices ([#637](https://github.com/googleapis/python-spanner-sqlalchemy/issues/637)) ([41905e2](https://github.com/googleapis/python-spanner-sqlalchemy/commit/41905e21b5b6473d5dbf75d40db765ebf48235dc))

## [1.10.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.9.0...v1.10.0) (2025-03-17)


### Features

* Support AUTO_INCREMENT and IDENTITY columns ([#610](https://github.com/googleapis/python-spanner-sqlalchemy/issues/610)) ([f67ebe8](https://github.com/googleapis/python-spanner-sqlalchemy/commit/f67ebe888ef4da8d94ff6d1e1d7f4cd5de37616c))

## [1.9.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.8.0...v1.9.0) (2025-02-21)


### Features

* Support request and transaction tags ([#558](https://github.com/googleapis/python-spanner-sqlalchemy/issues/558)) ([c4496fd](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c4496fd73c2afe0f519fed0264abe2abb9d022b9))


### Documentation

* Add test for using FOR UPDATE ([#575](https://github.com/googleapis/python-spanner-sqlalchemy/issues/575)) ([8419ae4](https://github.com/googleapis/python-spanner-sqlalchemy/commit/8419ae4ef07ba5b5e3134586c475cfcaeda240b5))

## [1.8.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.7.0...v1.8.0) (2024-12-09)


### Features

* Add helper function for insert-or-update ([#526](https://github.com/googleapis/python-spanner-sqlalchemy/issues/526)) ([6ff12ec](https://github.com/googleapis/python-spanner-sqlalchemy/commit/6ff12ecf6f1883525a901df4b4103b45ca95abed)), closes [#391](https://github.com/googleapis/python-spanner-sqlalchemy/issues/391)
* Support dml returning ([#335](https://github.com/googleapis/python-spanner-sqlalchemy/issues/335)) ([7db3f37](https://github.com/googleapis/python-spanner-sqlalchemy/commit/7db3f374510673d6521b16ca44d21043069d6ee7))
* Support float32 ([#531](https://github.com/googleapis/python-spanner-sqlalchemy/issues/531)) ([6c3cb42](https://github.com/googleapis/python-spanner-sqlalchemy/commit/6c3cb42919c5c8d52719d855af4fc2bb22c13fae))
* Support Partitioned DML ([#541](https://github.com/googleapis/python-spanner-sqlalchemy/issues/541)) ([108d965](https://github.com/googleapis/python-spanner-sqlalchemy/commit/108d965c60b6ea817de7fed86dca3d20f923d975)), closes [#496](https://github.com/googleapis/python-spanner-sqlalchemy/issues/496)


### Bug Fixes

* Add `existing_nullable` usage to `visit_column_type` ([#329](https://github.com/googleapis/python-spanner-sqlalchemy/issues/329)) ([273f03b](https://github.com/googleapis/python-spanner-sqlalchemy/commit/273f03bdf27c12317712a9939eedd25bd88c475a))
* Map now() to current_timestamp ([#540](https://github.com/googleapis/python-spanner-sqlalchemy/issues/540)) ([4b24f33](https://github.com/googleapis/python-spanner-sqlalchemy/commit/4b24f335ff918c7404201db16d05ccc817626dfe)), closes [#497](https://github.com/googleapis/python-spanner-sqlalchemy/issues/497)
* Support storing columns for indices ([#485](https://github.com/googleapis/python-spanner-sqlalchemy/issues/485)) ([93579c8](https://github.com/googleapis/python-spanner-sqlalchemy/commit/93579c8d6298dd9a07b2ca2b9c451036e33d2e6f))
* Support THEN RETURN for insert, update, delete ([#503](https://github.com/googleapis/python-spanner-sqlalchemy/issues/503)) ([ac64472](https://github.com/googleapis/python-spanner-sqlalchemy/commit/ac644726665213f234ce8ec4dea715c820a670e9))


### Dependencies

* Add nh3 ([#481](https://github.com/googleapis/python-spanner-sqlalchemy/issues/481)) ([3c2bcf9](https://github.com/googleapis/python-spanner-sqlalchemy/commit/3c2bcf9901ce132a6d5d5d3b1ad3608526a378b5))
* Add proto plus ([#482](https://github.com/googleapis/python-spanner-sqlalchemy/issues/482)) ([8663453](https://github.com/googleapis/python-spanner-sqlalchemy/commit/86634531793cf01b46cefe87f74375ee59060638))
* Update all deps ([#413](https://github.com/googleapis/python-spanner-sqlalchemy/issues/413)) ([25d9d2c](https://github.com/googleapis/python-spanner-sqlalchemy/commit/25d9d2c32638eb3e551921eecea435452c548bcb))


### Documentation

* Add sample for read-only transactions ([#533](https://github.com/googleapis/python-spanner-sqlalchemy/issues/533)) ([d2d72b6](https://github.com/googleapis/python-spanner-sqlalchemy/commit/d2d72b6fad4ea457114a50a2869d053798fed452))
* Add sample for stale reads ([#539](https://github.com/googleapis/python-spanner-sqlalchemy/issues/539)) ([e9df810](https://github.com/googleapis/python-spanner-sqlalchemy/commit/e9df8105b18e03dbf3b746fed85ffe9da286b953))
* Add samples for Spanner-specific features ([#492](https://github.com/googleapis/python-spanner-sqlalchemy/issues/492)) ([a6ed382](https://github.com/googleapis/python-spanner-sqlalchemy/commit/a6ed382be2a7105f9e8b2f855df3919e8c6750c9))
* Cleanup the transaction section of README a bit ([#545](https://github.com/googleapis/python-spanner-sqlalchemy/issues/545)) ([c3b5df5](https://github.com/googleapis/python-spanner-sqlalchemy/commit/c3b5df52c2fc62b11aa684c2d02dac95dd06ab59))
* Fix readme typo ([#487](https://github.com/googleapis/python-spanner-sqlalchemy/issues/487)) ([b452b4f](https://github.com/googleapis/python-spanner-sqlalchemy/commit/b452b4f73d200b99fd800862c88304b67aa035c5))

## [1.7.0](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.6.2...v1.7.0) (2024-02-07)


### Features

* Support sequences ([#336](https://github.com/googleapis/python-spanner-sqlalchemy/issues/336)) ([e35a8a0](https://github.com/googleapis/python-spanner-sqlalchemy/commit/e35a8a01fadce8b5a4b0208f9e6146a4241fa827))


### Bug Fixes

* Db.params OpenTelemetry integration issue ([#346](https://github.com/googleapis/python-spanner-sqlalchemy/issues/346)) ([0a69031](https://github.com/googleapis/python-spanner-sqlalchemy/commit/0a69031c9145945e5c438df48977329a67f94a78))
* Fixing test for literals due to change in sqlalchemy core tests ([#384](https://github.com/googleapis/python-spanner-sqlalchemy/issues/384)) ([62cccc3](https://github.com/googleapis/python-spanner-sqlalchemy/commit/62cccc33cba504f8a4c67bd215341a3e747ec9bf))
* Table name should be quoted by back quotes (`) on DROP TABLE ([#385](https://github.com/googleapis/python-spanner-sqlalchemy/issues/385)) ([628d26c](https://github.com/googleapis/python-spanner-sqlalchemy/commit/628d26c416cbe44871d8114251989d9f581bebf0))

## [1.6.2](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.6.1...v1.6.2) (2023-05-31)


### Bug Fixes

* Disables sequence support ([#326](https://github.com/googleapis/python-spanner-sqlalchemy/issues/326)) ([7b441ff](https://github.com/googleapis/python-spanner-sqlalchemy/commit/7b441ff867160a102ebe88dfa27b3e21b9149007))

## [1.6.1](https://github.com/googleapis/python-spanner-sqlalchemy/compare/v1.6.0...v1.6.1) (2023-05-23)


### Bug Fixes

* Add opentelemetry version ([#322](https://github.com/googleapis/python-spanner-sqlalchemy/issues/322)) ([b80d24d](https://github.com/googleapis/python-spanner-sqlalchemy/commit/b80d24d251f07d4c000aa214955cf9729cd49545))
* Fix check so it's all lowercase. ([#321](https://github.com/googleapis/python-spanner-sqlalchemy/issues/321)) ([8fae358](https://github.com/googleapis/python-spanner-sqlalchemy/commit/8fae3587d5c963539b255c976136b18041147e5b))

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
