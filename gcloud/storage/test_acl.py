import unittest2


class Test_ACLEntity(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import _ACLEntity
        return _ACLEntity

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_default_identifier(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        self.assertEqual(entity.type, TYPE)
        self.assertEqual(entity.identifier, None)
        self.assertEqual(entity.get_roles(), set())

    def test_ctor_explicit_identifier(self):
        TYPE = 'type'
        ID = 'id'
        entity = self._makeOne(TYPE, ID)
        self.assertEqual(entity.type, TYPE)
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(entity.get_roles(), set())

    def test___str__no_identifier(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        self.assertEqual(str(entity), TYPE)

    def test___str__w_identifier(self):
        TYPE = 'type'
        ID = 'id'
        entity = self._makeOne(TYPE, ID)
        self.assertEqual(str(entity), '%s-%s' % (TYPE, ID))

    def test_grant_simple(self):
        TYPE = 'type'
        ROLE = 'role'
        entity = self._makeOne(TYPE)
        found = entity.grant(ROLE)
        self.assertTrue(found is entity)
        self.assertEqual(entity.get_roles(), set([ROLE]))

    def test_grant_duplicate(self):
        TYPE = 'type'
        ROLE1 = 'role1'
        ROLE2 = 'role2'
        entity = self._makeOne(TYPE)
        entity.grant(ROLE1)
        entity.grant(ROLE2)
        entity.grant(ROLE1)
        self.assertEqual(entity.get_roles(), set([ROLE1, ROLE2]))

    def test_revoke_miss(self):
        TYPE = 'type'
        ROLE = 'nonesuch'
        entity = self._makeOne(TYPE)
        found = entity.revoke(ROLE)
        self.assertTrue(found is entity)
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_hit(self):
        TYPE = 'type'
        ROLE1 = 'role1'
        ROLE2 = 'role2'
        entity = self._makeOne(TYPE)
        entity.grant(ROLE1)
        entity.grant(ROLE2)
        entity.revoke(ROLE1)
        self.assertEqual(entity.get_roles(), set([ROLE2]))

    def test_grant_read(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_read()
        self.assertEqual(entity.get_roles(), set([entity.READER_ROLE]))

    def test_grant_write(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_write()
        self.assertEqual(entity.get_roles(), set([entity.WRITER_ROLE]))

    def test_grant_owner(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_owner()
        self.assertEqual(entity.get_roles(), set([entity.OWNER_ROLE]))

    def test_revoke_read(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(entity.READER_ROLE)
        entity.revoke_read()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_write(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(entity.WRITER_ROLE)
        entity.revoke_write()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_owner(self):
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(entity.OWNER_ROLE)
        entity.revoke_owner()
        self.assertEqual(entity.get_roles(), set())


class Test_ACL(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import ACL
        return ACL

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        acl = self._makeOne()
        self.assertEqual(acl.entities, {})
        self.assertEqual(list(acl.get_entities()), [])
        self.assertFalse(acl.loaded)

    def test_clear(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        acl.entity(TYPE, ID)
        acl.clear()
        self.assertTrue(acl.loaded)
        self.assertEqual(acl.entities, {})
        self.assertEqual(list(acl.get_entities()), [])

    def test_reset(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        acl.entity(TYPE, ID)
        acl.reset()
        self.assertFalse(acl.loaded)
        self.assertEqual(acl.entities, {})
        self.assertEqual(list(acl.get_entities()), [])

    def test___iter___empty(self):
        acl = self._makeOne()
        self.assertEqual(list(acl), [])

    def test___iter___non_empty_no_roles(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        acl.entity(TYPE, ID)
        self.assertEqual(list(acl), [])

    def test___iter___non_empty_w_roles(self):
        TYPE = 'type'
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        entity.grant(ROLE)
        self.assertEqual(list(acl),
                         [{'entity': '%s-%s' % (TYPE, ID), 'role': ROLE}])

    def test___iter___non_empty_w_empty_role(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        entity.grant('')
        self.assertEqual(list(acl), [])

    def test_entity_from_dict_allUsers(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity_from_dict({'entity': 'allUsers', 'role': ROLE})
        self.assertEqual(entity.type, 'allUsers')
        self.assertEqual(entity.identifier, None)
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl),
                         [{'entity': 'allUsers', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_allAuthenticatedUsers(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity_from_dict({'entity': 'allAuthenticatedUsers',
                                       'role': ROLE})
        self.assertEqual(entity.type, 'allAuthenticatedUsers')
        self.assertEqual(entity.identifier, None)
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl),
                         [{'entity': 'allAuthenticatedUsers', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_string_w_hyphen(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity_from_dict({'entity': 'type-id', 'role': ROLE})
        self.assertEqual(entity.type, 'type')
        self.assertEqual(entity.identifier, 'id')
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_from_dict_string_wo_hyphen(self):
        ROLE = 'role'
        acl = self._makeOne()
        self.assertRaises(ValueError,
                          acl.entity_from_dict,
                          {'entity': 'bogus', 'role': ROLE})
        self.assertEqual(list(acl.get_entities()), [])

    def test_has_entity_miss_str(self):
        acl = self._makeOne()
        self.assertFalse(acl.has_entity('nonesuch'))

    def test_has_entity_miss_entity(self):
        from gcloud.storage.acl import _ACLEntity
        TYPE = 'type'
        ID = 'id'
        entity = _ACLEntity(TYPE, ID)
        acl = self._makeOne()
        self.assertFalse(acl.has_entity(entity))

    def test_has_entity_hit_str(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity('%s-%s' % (TYPE, ID)))

    def test_has_entity_hit_entity(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity(entity))

    def test_get_entity_miss_str_no_default(self):
        acl = self._makeOne()
        self.assertEqual(acl.get_entity('nonesuch'), None)

    def test_get_entity_miss_entity_no_default(self):
        from gcloud.storage.acl import _ACLEntity
        TYPE = 'type'
        ID = 'id'
        entity = _ACLEntity(TYPE, ID)
        acl = self._makeOne()
        self.assertEqual(acl.get_entity(entity), None)

    def test_get_entity_miss_str_w_default(self):
        DEFAULT = object()
        acl = self._makeOne()
        self.assertTrue(acl.get_entity('nonesuch', DEFAULT) is DEFAULT)

    def test_get_entity_miss_entity_w_default(self):
        from gcloud.storage.acl import _ACLEntity
        DEFAULT = object()
        TYPE = 'type'
        ID = 'id'
        entity = _ACLEntity(TYPE, ID)
        acl = self._makeOne()
        self.assertTrue(acl.get_entity(entity, DEFAULT) is DEFAULT)

    def test_get_entity_hit_str(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity('%s-%s' % (TYPE, ID)))

    def test_get_entity_hit_entity(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.has_entity(entity))

    def test_add_entity_miss(self):
        from gcloud.storage.acl import _ACLEntity
        TYPE = 'type'
        ID = 'id'
        ROLE = 'role'
        entity = _ACLEntity(TYPE, ID)
        entity.grant(ROLE)
        acl = self._makeOne()
        acl.add_entity(entity)
        self.assertTrue(acl.loaded)
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_add_entity_hit(self):
        from gcloud.storage.acl import _ACLEntity
        TYPE = 'type'
        ID = 'id'
        KEY = '%s-%s' % (TYPE, ID)
        ROLE = 'role'
        entity = _ACLEntity(TYPE, ID)
        entity.grant(ROLE)
        acl = self._makeOne()
        before = acl.entity(TYPE, ID)
        acl.add_entity(entity)
        self.assertTrue(acl.loaded)
        self.assertFalse(acl.get_entity(KEY) is before)
        self.assertTrue(acl.get_entity(KEY) is entity)
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_miss(self):
        TYPE = 'type'
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        self.assertTrue(acl.loaded)
        entity.grant(ROLE)
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_entity_hit(self):
        TYPE = 'type'
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        before = acl.entity(TYPE, ID)
        before.grant(ROLE)
        entity = acl.entity(TYPE, ID)
        self.assertTrue(entity is before)
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])
        self.assertEqual(list(acl.get_entities()), [entity])

    def test_user(self):
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.user(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, 'user')
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl),
                         [{'entity': 'user-%s' % ID, 'role': ROLE}])

    def test_group(self):
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.group(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, 'group')
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl),
                         [{'entity': 'group-%s' % ID, 'role': ROLE}])

    def test_domain(self):
        ID = 'id'
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.domain(ID)
        entity.grant(ROLE)
        self.assertEqual(entity.type, 'domain')
        self.assertEqual(entity.identifier, ID)
        self.assertEqual(list(acl),
                         [{'entity': 'domain-%s' % ID, 'role': ROLE}])

    def test_all(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.all()
        entity.grant(ROLE)
        self.assertEqual(entity.type, 'allUsers')
        self.assertEqual(entity.identifier, None)
        self.assertEqual(list(acl),
                         [{'entity': 'allUsers', 'role': ROLE}])

    def test_all_authenticated(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.all_authenticated()
        entity.grant(ROLE)
        self.assertEqual(entity.type, 'allAuthenticatedUsers')
        self.assertEqual(entity.identifier, None)
        self.assertEqual(list(acl),
                         [{'entity': 'allAuthenticatedUsers', 'role': ROLE}])

    def test_get_entities_empty(self):
        acl = self._makeOne()
        self.assertEqual(acl.get_entities(), [])

    def test_get_entities_nonempty(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
        self.assertEqual(acl.get_entities(), [entity])

    def test_save_raises_NotImplementedError(self):
        acl = self._makeOne()
        self.assertRaises(NotImplementedError, acl.save)


class Test_BucketACL(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import BucketACL
        return BucketACL

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        bucket = object()
        acl = self._makeOne(bucket)
        self.assertEqual(acl.entities, {})
        self.assertEqual(list(acl.get_entities()), [])
        self.assertTrue(acl.bucket is bucket)

    def test_save(self):
        class _Bucket(object):
            def save_acl(self, acl):
                self._saved = acl
        bucket = _Bucket()
        acl = self._makeOne(bucket)
        acl.save()
        self.assertTrue(bucket._saved is acl)


class Test_DefaultObjectACL(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import DefaultObjectACL
        return DefaultObjectACL

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_save(self):
        class _Bucket(object):
            def save_default_object_acl(self, acl):
                self._saved = acl
        bucket = _Bucket()
        acl = self._makeOne(bucket)
        acl.save()
        self.assertTrue(bucket._saved is acl)


class Test_ObjectACL(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import ObjectACL
        return ObjectACL

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        key = object()
        acl = self._makeOne(key)
        self.assertEqual(acl.entities, {})
        self.assertEqual(list(acl.get_entities()), [])
        self.assertTrue(acl.key is key)

    def test_save(self):
        class _Key(object):
            def save_acl(self, acl):
                self._saved = acl
        key = _Key()
        acl = self._makeOne(key)
        acl.save()
        self.assertTrue(key._saved is acl)
