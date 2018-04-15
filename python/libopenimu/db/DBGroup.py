"""

Testing sqlalchemy ORM...

"""
import sqlalchemy
from libopenimu.models.Group import Group
from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, Sequence

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Group(Base):
    __tablename__ = 'tabGroups'

    id_group = Column(Integer, Sequence('id_group_sequence'), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Database rep
    def __repr__(self):
        return "<Group(name='%s', description='%s')>" % (self.name, self.description)


# Main
if __name__ == '__main__':

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///test.db', echo=True)

    # Will create all tables
    Base.metadata.create_all(engine)

    # Will create Session interface class
    Session = sessionmaker(bind=engine)

    # Session instance
    session = Session()

    print('Starting... sqlalchemy version: ', sqlalchemy.__version__)
    print(Group.__table__)
    mygroup1 = Group(name='MyName', description='MyDescription')
    mygroup2 = Group(name='MyName', description='MyDescription')
    session.add(mygroup1)
    session.add(mygroup2)
    session.commit()

    print(session.dirty)

