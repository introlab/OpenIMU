"""
 Group
 @authors Simon Brière, Dominic Létourneau
 @date 27/03/2018
"""


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

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def print(self):
        print('Group','id_group:',self.id_group,'name:',self.name, 'description:',self.description)

    def __str__(self):
        return 'Group: ' + str(self.as_tuple())

    def as_tuple(self):
        return (self.id_group, self.name, self.description)

    def from_tuple(self, tuple):
        (self.id_group, self.name, self.description) = tuple


if __name__ == '__main__':
    mygroup = Group()
    mygroup.print()
    print(mygroup)

    mygroup2 = Group()
    mygroup2.from_tuple((0,'name','description'))
    print(mygroup2)

    mygroup3 = Group((1,'test','test'))
    print(mygroup3)

