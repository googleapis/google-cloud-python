import unittest2


class Test_ACL_Entity(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.acl import ACL
        return ACL.Entity

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
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_read()
        self.assertEqual(entity.get_roles(), set([ACL.Role.Reader]))

    def test_grant_write(self):
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_write()
        self.assertEqual(entity.get_roles(), set([ACL.Role.Writer]))

    def test_grant_owner(self):
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant_owner()
        self.assertEqual(entity.get_roles(), set([ACL.Role.Owner]))

    def test_revoke_read(self):
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(ACL.Role.Reader)
        entity.revoke_read()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_write(self):
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(ACL.Role.Writer)
        entity.revoke_write()
        self.assertEqual(entity.get_roles(), set())

    def test_revoke_owner(self):
        from gcloud.storage.acl import ACL
        TYPE = 'type'
        entity = self._makeOne(TYPE)
        entity.grant(ACL.Role.Owner)
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

    def test___iter___empty(self):
        acl = self._makeOne()
        self.assertEqual(list(acl), [])

    def test___iter___non_empty_no_roles(self):
        TYPE = 'type'
        ID = 'id'
        acl = self._makeOne()
        entity = acl.entity(TYPE, ID)
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

    def test_entity_from_dict_allUsers(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity_from_dict({'entity': 'allUsers', 'role': ROLE})
        self.assertEqual(entity.type, 'allUsers')
        self.assertEqual(entity.identifier, None)
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl),
                         [{'entity': 'allUsers', 'role': ROLE}])

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

    def test_entity_from_dict_string_w_hyphen(self):
        ROLE = 'role'
        acl = self._makeOne()
        entity = acl.entity_from_dict({'entity': 'type-id', 'role': ROLE})
        self.assertEqual(entity.type, 'type')
        self.assertEqual(entity.identifier, 'id')
        self.assertEqual(entity.get_roles(), set([ROLE]))
        self.assertEqual(list(acl),
                         [{'entity': 'type-id', 'role': ROLE}])

    def test_entity_from_dict_string_wo_hyphen(self):
        ROLE = 'role'
        acl = self._makeOne()
        self.assertRaises(ValueError,
                          acl.entity_from_dict,
                                {'entity': 'bogus', 'role': ROLE})
