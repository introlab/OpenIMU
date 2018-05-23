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
        self.assertEqual(group.id_group, None)
        self.assertEqual(group.description, None)
        self.assertEqual(group.name, None)

    def test_variable_args_construction(self):
        pass

    def test_get_set_name(self):
        group = Group()
        name = 'My Name'
        group.name = name
        self.assertEqual(group.name, name)

    def test_get_set_description(self):
        group = Group()
        description = 'My Description'
        group.description = description
        self.assertEqual(group.description, description)

    def test_get_set_id_group(self):
        group = Group()
        id_group = 0
        group.id_group = id_group
        self.assertEqual(group.id_group, id_group)

    def test_is_valid(self):
        group = Group()
        self.assertEqual(group.is_valid(), False)
        group.id_group = 0
        self.assertEqual(group.is_valid(), False)
        group.name = 'My Name'
        self.assertEqual(group.is_valid(), False)
        group.description = 'My Description'
        self.assertEqual(group.is_valid(), True)

    def test_properties(self):
        my_id_group = 0
        my_name = 'My Name'
        my_description = 'My Description'
        group = Group()
        group.id_group = my_id_group
        group.name = my_name
        group.description = my_description
        self.assertEqual(group.id_group, my_id_group)
        self.assertEqual(group.name, my_name)
        self.assertEqual(group.description, my_description)
