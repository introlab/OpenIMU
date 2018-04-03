"""
 Group
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import unittest


class Group:
    # def __init__(self, id_group=None, name=None, description=None):
    #    self.id_group = id_group
    #    self.name = name
    #    self.description = description

    def __init__(self, tuple=(None,None,None)):
        self.id_group = None
        self.name = None
        self.description = None
        self.from_tuple(tuple)

    def set_id_group(self, id_group):
        self.id_group = id_group

    def get_id_group(self):
        return self.id_group

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def print(self):
        print('Group', 'id_group:', self.id_group, 'name:', self.name, 'description:', self.description)

    def __str__(self):
        return 'Group: ' + str(self.as_tuple())

    def as_tuple(self):
        return self.id_group, self.name, self.description

    def from_tuple(self, tuple):
        (self.id_group, self.name, self.description) = tuple

    def is_valid(self):
        if self.id_group is None:
            return False
        if self.name is None:
            return False
        if self.description is None:
            return False
        return True



"""
Unit testing
"""


class GroupTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_args_construction(self):
        group = Group()
        self.assertEqual(group.get_id_group(), None)
        self.assertEqual(group.get_description(), None)
        self.assertEqual(group.get_name(), None)

    def test_get_set_name(self):
        group = Group()
        name = 'My Name'
        group.set_name(name)
        self.assertEqual(group.get_name(), name)

    def test_get_set_description(self):
        group = Group()
        description = 'My Description'
        group.set_description(description)
        self.assertEqual(group.get_description(), description)

    def test_get_set_id_group(self):
        group = Group()
        id_group = 0
        group.set_id_group(id_group)
        self.assertEqual(group.get_id_group(), id_group)

    def test_as_from_tuple(self):
        group = Group()
        id_group = 0
        name = 'My Name'
        description = 'My Description'
        group.from_tuple((id_group, name, description))
        self.assertEqual(group.as_tuple(), (id_group, name, description))
        self.assertEqual(group.is_valid(), True)

    def test_is_valid(self):
        group = Group()
        self.assertEqual(group.is_valid(), False)
        group.set_id_group(0)
        self.assertEqual(group.is_valid(), False)
        group.set_name('My Name')
        self.assertEqual(group.is_valid(), False)
        group.set_description('My Description')
        self.assertEqual(group.is_valid(), True)
        group2 = Group((0, 'My Name', 'My Description'))
        self.assertEqual(group2.is_valid(), True)
