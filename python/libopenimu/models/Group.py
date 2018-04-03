"""
 Group
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""

import unittest


class Group:
    def __init__(self, *args, **kwargs):
        # Initial state
        self._id_group = None
        self._name = None
        self._description = None

        # Variable args
        if len(args) == 1:
            self.from_tuple(args[0])
        elif len(args) == 3:
            self._id_group = kwargs.get('id_group', None)
            self._name = kwargs.get('name', None)
            self._description = kwargs.get('description', None)

    def set_id_group(self, id_group):
        self._id_group = id_group

    def get_id_group(self):
        return self._id_group

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_description(self, description):
        self._description = description

    def get_description(self):
        return self._description

    def print(self):
        print('Group', 'id_group:', self._id_group, 'name:', self._name, 'description:', self._description)

    def __str__(self):
        return 'Group: ' + str(self.as_tuple())

    def as_tuple(self):
        return self._id_group, self._name, self._description

    def from_tuple(self, tuple):
        (self._id_group, self._name, self._description) = tuple

    def is_valid(self):
        if self._id_group is None:
            return False
        if self._name is None:
            return False
        if self._description is None:
            return False
        return True

    # Properties
    id_group = property(get_id_group, set_id_group)
    name = property(get_name, set_name)
    description = property(get_description, set_description)

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

    def test_variable_args_construction(self):
        pass

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

    def test_properties(self):
        my_id_group = 0
        my_name = 'My Name'
        my_description = 'My Description'
        group = Group()
        group.id_group = my_id_group
        group.name = my_name
        group.description = my_description
        self.assertEqual(group.get_id_group(), my_id_group)
        self.assertEqual(group.id_group, my_id_group)
        self.assertEqual(group.get_name(), my_name)
        self.assertEqual(group.name, my_name)
        self.assertEqual(group.get_description(), my_description)
        self.assertEqual(group.description, my_description)
