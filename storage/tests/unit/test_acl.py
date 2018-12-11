# Copyright 2014 Google LLC
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

import unittest


class Test_ACLEntity(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.acl import _ACLEntity

        return _ACLEntity

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_default_identifier(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        self.assertEqual(entity.type, TYPE)
        self.assertIsNone(entity.identifier)
        self.assertEqual(entity.get_roles(), set())

    def test_ctor_w_identifier(self):
        TYPE = "type"
        ID = "id"
        entity = self._make_one(TYPE, ID)
        self.assertEqual(entity.type, TYPE)
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(entity.get_roles(), set())

    def test___str__no_identifier(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        self.assertEqual(str(entity), TYPE)

    def test___str__w_identifier(self):
        TYPE = "type"
        ID = "id"
        entity = self._make_one(TYPE, ID)
        self.assertEqual(str(entity), "%s-%s" % (TYPE, ID))

    def test_grant_simple(self):
        TYPE = "type"
        ROLE = "role"
        entity = self._make_one(TYPE)
        entity.grant(ROLE)
        self.assertEqual(entity.get_roles(), set([ROLE]))

    def test_grant_duplicate(self):
        TYPE = "type"
        ROLE1 = "role1"
        ROLE2 = "role2"
        entity = self._make_one(TYPE)
        entity.grant(ROLE1)
        entity.grant(ROLE2)
        entity.grant(ROLE1)
        self.assertEqual(entity.get_roles(), set([ROLE1, ROLE2]))

    def test_revoke_miss(self):
        TYPE = "type"
        ROLE = "nonesuch"
        entity = self._make_one(TYPE)
        entity.revoke(ROLE)
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_hit(self):
        TYPE = "type"
        ROLE1 = "role1"
        ROLE2 = "role2"
        entity = self._make_one(TYPE)
        entity.grant(ROLE1)
        entity.grant(ROLE2)
        entity.revoke(ROLE1)
        self.assertEqual(entity.get_roles(), set([ROLE2]))

    def test_grant_read(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant_read()
        self.assertEqual(entity.get_roles(), set([entity.READER_ROLE]))

    def test_grant_write(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant_write()
        self.assertEqual(entity.get_roles(), set([entity.WRITER_ROLE]))

    def test_grant_owner(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant_owner()
        self.assertEqual(entity.get_roles(), set([entity.OWNER_ROLE]))

    def test_revoke_read(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant(entity.READER_ROLE)
        entity.revoke_read()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_write(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant(entity.WRITER_ROLE)
        entity.revoke_write()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_owner(self):
        TYPE = "type"
        entity = self._make_one(TYPE)
        entity.grant(entity.OWNER_ROLE)
        entity.revoke_owner()
        self.assertEqual(entity.get_roles(), set())


class Test_ACL(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.acl import ACL

        return ACL

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_validate_predefined(self):
        ACL = self._get_target_class()
        self.assertIsNone(ACL.validate_predefined(None))
        self.assertEqual(ACL.validate_predefined("public-read"), "publicRead")
        self.assertEqual(ACL.validate_predefined("publicRead"), "publicRead")
        with self.assertRaises(ValueError):
            ACL.validate_predefined("publicread")

    def test_ctor(self):
        acl = self._make_one()
        self.assertEqual(acl.entities, {})
        self.assertFalse(acl.loaded)

    def test__ensure_loaded(self):
        acl = self._make_one()

        def _reload():
            acl._really_loaded = True

        acl.reload = _reload
        acl._ensure_loaded()
        self.assertTrue(acl._really_loaded)

    def test_client_is_abstract(self):
        acl = self._make_one()
        self.assertRaises(NotImplementedError, lambda: acl.client)

    def test_reset(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        acl.entity(TYPE, ID)
        acl.reset()
        self.assertEqual(acl.entities, {})
        self.assertFalse(acl.loaded)

    def test___iter___empty_eager(self):
        acl = self._make_one()
        acl.loaded = True
        self.assertEqual(list(acl), [])

    def test___iter___empty_lazy(self):
        acl = self._make_one()

        def _reload():
            acl.loaded = True

        acl.reload = _reload
        self.assertEqual(list(acl), [])
        self.assertTrue(acl.loaded)

    def test___iter___non_empty_no_roles(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        acl.entity(TYPE, ID)
        self.assertEqual(list(acl), [])

    def test___iter___non_empty_w_roles(self):
        TYPE = "type"
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        entity.grant(ROLE)
        self.assertEqual(list(acl), [{"entity": "%s-%s" % (TYPE, ID), "role": ROLE}])

    def test___iter___non_empty_w_empty_role(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        entity.grant("")
        self.assertEqual(list(acl), [])

    def test_entity_from_dict_allUsers_eager(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity_from_dict({"entity": "allUsers", "role": ROLE})
        self.assertEqual(entity.type, "allUsers")
        self.assertIsNone(entity.identifier)
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl), [{"entity": "allUsers", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_allAuthenticatedUsers(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity_from_dict({"entity": "allAuthenticatedUsers", "role": ROLE})
        self.assertEqual(entity.type, "allAuthenticatedUsers")
        self.assertIsNone(entity.identifier)
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl), [{"entity": "allAuthenticatedUsers", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_string_w_hyphen(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity_from_dict({"entity": "type-id", "role": ROLE})
        self.assertEqual(entity.type, "type")
        self.assertEqual(entity.identifier, "id")
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_string_wo_hyphen(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        self.assertRaises(
            ValueError, acl.entity_from_dict, {"entity": "bogus", "role": ROLE}
        )
        self.assertEqual(list(acl.get_entities()), [])

    def test_has_entity_miss_str_eager(self):
        acl = self._make_one()
        acl.loaded = True
        self.assertFalse(acl.has_entity("nonesuch"))

    def test_has_entity_miss_str_lazy(self):
        acl = self._make_one()

        def _reload():
            acl.loaded = True

        acl.reload = _reload
        self.assertFalse(acl.has_entity("nonesuch"))
        self.assertTrue(acl.loaded)

    def test_has_entity_miss_entity(self):
        from google.cloud.storage.acl import _ACLEntity

        TYPE = "type"
        ID = "id"
        entity = _ACLEntity(TYPE, ID)
        acl = self._make_one()
        acl.loaded = True
        self.assertFalse(acl.has_entity(entity))

    def test_has_entity_hit_str(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity("%s-%s" % (TYPE, ID)))

    def test_has_entity_hit_entity(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity(entity))

    def test_get_entity_miss_str_no_default_eager(self):
        acl = self._make_one()
        acl.loaded = True
        self.assertIsNone(acl.get_entity("nonesuch"))

    def test_get_entity_miss_str_no_default_lazy(self):
        acl = self._make_one()

        def _reload():
            acl.loaded = True

        acl.reload = _reload
        self.assertIsNone(acl.get_entity("nonesuch"))
        self.assertTrue(acl.loaded)

    def test_get_entity_miss_entity_no_default(self):
        from google.cloud.storage.acl import _ACLEntity

        TYPE = "type"
        ID = "id"
        entity = _ACLEntity(TYPE, ID)
        acl = self._make_one()
        acl.loaded = True
        self.assertIsNone(acl.get_entity(entity))

    def test_get_entity_miss_str_w_default(self):
        DEFAULT = object()
        acl = self._make_one()
        acl.loaded = True
        self.assertIs(acl.get_entity("nonesuch", DEFAULT), DEFAULT)

    def test_get_entity_miss_entity_w_default(self):
        from google.cloud.storage.acl import _ACLEntity

        DEFAULT = object()
        TYPE = "type"
        ID = "id"
        entity = _ACLEntity(TYPE, ID)
        acl = self._make_one()
        acl.loaded = True
        self.assertIs(acl.get_entity(entity, DEFAULT), DEFAULT)

    def test_get_entity_hit_str(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity("%s-%s" % (TYPE, ID)))

    def test_get_entity_hit_entity(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity(entity))

    def test_add_entity_miss_eager(self):
        from google.cloud.storage.acl import _ACLEntity

        TYPE = "type"
        ID = "id"
        ROLE = "role"
        entity = _ACLEntity(TYPE, ID)
        entity.grant(ROLE)
        acl = self._make_one()
        acl.loaded = True
        acl.add_entity(entity)
        self.assertTrue(acl.loaded)
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_add_entity_miss_lazy(self):
        from google.cloud.storage.acl import _ACLEntity

        TYPE = "type"
        ID = "id"
        ROLE = "role"
        entity = _ACLEntity(TYPE, ID)
        entity.grant(ROLE)
        acl = self._make_one()

        def _reload():
            acl.loaded = True

        acl.reload = _reload
        acl.add_entity(entity)
        self.assertTrue(acl.loaded)
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])
        self.assertTrue(acl.loaded)

    def test_add_entity_hit(self):
        from google.cloud.storage.acl import _ACLEntity

        TYPE = "type"
        ID = "id"
        ENTITY_VAL = "%s-%s" % (TYPE, ID)
        ROLE = "role"
        entity = _ACLEntity(TYPE, ID)
        entity.grant(ROLE)
        acl = self._make_one()
        acl.loaded = True
        before = acl.entity(TYPE, ID)
        acl.add_entity(entity)
        self.assertTrue(acl.loaded)
        self.assertIsNot(acl.get_entity(ENTITY_VAL), before)
        self.assertIs(acl.get_entity(ENTITY_VAL), entity)
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_miss(self):
        TYPE = "type"
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.loaded)
        entity.grant(ROLE)
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_hit(self):
        TYPE = "type"
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        before = acl.entity(TYPE, ID)
        before.grant(ROLE)
        entity = acl.entity(TYPE, ID)
        self.assertIs(entity, before)
        self.assertEqual(list(acl), [{"entity": "type-id", "role": ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_user(self):
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.user(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, "user")
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl), [{"entity": "user-%s" % ID, "role": ROLE}])

    def test_group(self):
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.group(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, "group")
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl), [{"entity": "group-%s" % ID, "role": ROLE}])

    def test_domain(self):
        ID = "id"
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.domain(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, "domain")
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl), [{"entity": "domain-%s" % ID, "role": ROLE}])

    def test_all(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.all()
        entity.grant(ROLE)
        self.assertEqual(entity.type, "allUsers")
        self.assertIsNone(entity.identifier)
        self.assertEqual(list(acl), [{"entity": "allUsers", "role": ROLE}])

    def test_all_authenticated(self):
        ROLE = "role"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.all_authenticated()
        entity.grant(ROLE)
        self.assertEqual(entity.type, "allAuthenticatedUsers")
        self.assertIsNone(entity.identifier)
        self.assertEqual(list(acl), [{"entity": "allAuthenticatedUsers", "role": ROLE}])

    def test_get_entities_empty_eager(self):
        acl = self._make_one()
        acl.loaded = True
        self.assertEqual(acl.get_entities(), [])

    def test_get_entities_empty_lazy(self):
        acl = self._make_one()

        def _reload():
            acl.loaded = True

        acl.reload = _reload
        self.assertEqual(acl.get_entities(), [])
        self.assertTrue(acl.loaded)

    def test_get_entities_nonempty(self):
        TYPE = "type"
        ID = "id"
        acl = self._make_one()
        acl.loaded = True
        entity = acl.entity(TYPE, ID)
        self.assertEqual(acl.get_entities(), [entity])

    def test_reload_missing(self):
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/652
        ROLE = "role"
        connection = _Connection({})
        client = _Client(connection)
        acl = self._make_one()
        acl.reload_path = "/testing/acl"
        acl.loaded = True
        acl.entity("allUsers", ROLE)
        acl.reload(client=client)
        self.assertEqual(list(acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0], {"method": "GET", "path": "/testing/acl", "query_params": {}}
        )

    def test_reload_empty_result_clears_local(self):
        ROLE = "role"
        connection = _Connection({"items": []})
        client = _Client(connection)
        acl = self._make_one()
        acl.reload_path = "/testing/acl"
        acl.loaded = True
        acl.entity("allUsers", ROLE)

        acl.reload(client=client)

        self.assertTrue(acl.loaded)
        self.assertEqual(list(acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0], {"method": "GET", "path": "/testing/acl", "query_params": {}}
        )

    def test_reload_nonempty_result_w_user_project(self):
        ROLE = "role"
        USER_PROJECT = "user-project-123"
        connection = _Connection({"items": [{"entity": "allUsers", "role": ROLE}]})
        client = _Client(connection)
        acl = self._make_one()
        acl.reload_path = "/testing/acl"
        acl.loaded = True
        acl.user_project = USER_PROJECT

        acl.reload(client=client)

        self.assertTrue(acl.loaded)
        self.assertEqual(list(acl), [{"entity": "allUsers", "role": ROLE}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "GET",
                "path": "/testing/acl",
                "query_params": {"userProject": USER_PROJECT},
            },
        )

    def test_save_none_set_none_passed(self):
        connection = _Connection()
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.save(client=client)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_save_existing_missing_none_passed(self):
        connection = _Connection({})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.save(client=client)
        self.assertEqual(list(acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]["method"], "PATCH")
        self.assertEqual(kw[0]["path"], "/testing")
        self.assertEqual(kw[0]["data"], {"acl": []})
        self.assertEqual(kw[0]["query_params"], {"projection": "full"})

    def test_save_no_acl(self):
        ROLE = "role"
        AFTER = [{"entity": "allUsers", "role": ROLE}]
        connection = _Connection({"acl": AFTER})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.entity("allUsers").grant(ROLE)
        acl.save(client=client)
        self.assertEqual(list(acl), AFTER)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]["method"], "PATCH")
        self.assertEqual(kw[0]["path"], "/testing")
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {"projection": "full"},
                "data": {"acl": AFTER},
            },
        )

    def test_save_w_acl_w_user_project(self):
        ROLE1 = "role1"
        ROLE2 = "role2"
        STICKY = {"entity": "allUsers", "role": ROLE2}
        USER_PROJECT = "user-project-123"
        new_acl = [{"entity": "allUsers", "role": ROLE1}]
        connection = _Connection({"acl": [STICKY] + new_acl})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.user_project = USER_PROJECT

        acl.save(new_acl, client=client)

        entries = list(acl)
        self.assertEqual(len(entries), 2)
        self.assertTrue(STICKY in entries)
        self.assertTrue(new_acl[0] in entries)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {"projection": "full", "userProject": USER_PROJECT},
                "data": {"acl": new_acl},
            },
        )

    def test_save_prefefined_invalid(self):
        connection = _Connection()
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        with self.assertRaises(ValueError):
            acl.save_predefined("bogus", client=client)

    def test_save_predefined_valid(self):
        PREDEFINED = "private"
        connection = _Connection({"acl": []})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.save_predefined(PREDEFINED, client=client)
        entries = list(acl)
        self.assertEqual(len(entries), 0)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {"projection": "full", "predefinedAcl": PREDEFINED},
                "data": {"acl": []},
            },
        )

    def test_save_predefined_w_XML_alias(self):
        PREDEFINED_XML = "project-private"
        PREDEFINED_JSON = "projectPrivate"
        connection = _Connection({"acl": []})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.save_predefined(PREDEFINED_XML, client=client)
        entries = list(acl)
        self.assertEqual(len(entries), 0)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {
                    "projection": "full",
                    "predefinedAcl": PREDEFINED_JSON,
                },
                "data": {"acl": []},
            },
        )

    def test_save_predefined_valid_w_alternate_query_param(self):
        # Cover case where subclass overrides _PREDEFINED_QUERY_PARAM
        PREDEFINED = "publicRead"
        connection = _Connection({"acl": []})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl._PREDEFINED_QUERY_PARAM = "alternate"
        acl.save_predefined(PREDEFINED, client=client)
        entries = list(acl)
        self.assertEqual(len(entries), 0)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {"projection": "full", "alternate": PREDEFINED},
                "data": {"acl": []},
            },
        )

    def test_clear(self):
        ROLE1 = "role1"
        ROLE2 = "role2"
        STICKY = {"entity": "allUsers", "role": ROLE2}
        connection = _Connection({"acl": [STICKY]})
        client = _Client(connection)
        acl = self._make_one()
        acl.save_path = "/testing"
        acl.loaded = True
        acl.entity("allUsers", ROLE1)
        acl.clear(client=client)
        self.assertEqual(list(acl), [STICKY])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(
            kw[0],
            {
                "method": "PATCH",
                "path": "/testing",
                "query_params": {"projection": "full"},
                "data": {"acl": []},
            },
        )


class Test_BucketACL(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.acl import BucketACL

        return BucketACL

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        NAME = "name"
        bucket = _Bucket(NAME)
        acl = self._make_one(bucket)
        self.assertEqual(acl.entities, {})
        self.assertFalse(acl.loaded)
        self.assertIs(acl.bucket, bucket)
        self.assertEqual(acl.reload_path, "/b/%s/acl" % NAME)
        self.assertEqual(acl.save_path, "/b/%s" % NAME)

    def test_user_project(self):
        NAME = "name"
        USER_PROJECT = "user-project-123"
        bucket = _Bucket(NAME)
        acl = self._make_one(bucket)
        self.assertIsNone(acl.user_project)
        bucket.user_project = USER_PROJECT
        self.assertEqual(acl.user_project, USER_PROJECT)


class Test_DefaultObjectACL(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.acl import DefaultObjectACL

        return DefaultObjectACL

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        NAME = "name"
        bucket = _Bucket(NAME)
        acl = self._make_one(bucket)
        self.assertEqual(acl.entities, {})
        self.assertFalse(acl.loaded)
        self.assertIs(acl.bucket, bucket)
        self.assertEqual(acl.reload_path, "/b/%s/defaultObjectAcl" % NAME)
        self.assertEqual(acl.save_path, "/b/%s" % NAME)


class Test_ObjectACL(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.acl import ObjectACL

        return ObjectACL

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        NAME = "name"
        BLOB_NAME = "blob-name"
        bucket = _Bucket(NAME)
        blob = _Blob(bucket, BLOB_NAME)
        acl = self._make_one(blob)
        self.assertEqual(acl.entities, {})
        self.assertFalse(acl.loaded)
        self.assertIs(acl.blob, blob)
        self.assertEqual(acl.reload_path, "/b/%s/o/%s/acl" % (NAME, BLOB_NAME))
        self.assertEqual(acl.save_path, "/b/%s/o/%s" % (NAME, BLOB_NAME))

    def test_user_project(self):
        NAME = "name"
        BLOB_NAME = "blob-name"
        USER_PROJECT = "user-project-123"
        bucket = _Bucket(NAME)
        blob = _Blob(bucket, BLOB_NAME)
        acl = self._make_one(blob)
        self.assertIsNone(acl.user_project)
        blob.user_project = USER_PROJECT
        self.assertEqual(acl.user_project, USER_PROJECT)


class _Blob(object):

    user_project = None

    def __init__(self, bucket, blob):
        self.bucket = bucket
        self.blob = blob

    @property
    def path(self):
        return "%s/o/%s" % (self.bucket.path, self.blob)


class _Bucket(object):

    user_project = None

    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return "/b/%s" % self.name


class _Connection(object):
    _delete_ok = False

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._deleted = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Client(object):
    def __init__(self, connection):
        self._connection = connection
