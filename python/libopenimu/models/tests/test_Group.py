"""

    Unit testing for Group
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
from libopenimu.models.Group import Group


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
