from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    gender = Column(String)
    age = Column(Integer)
    office_name = Column(String)
    living_space_name = Column(String)

    def __init__(self, name, role, gender, age,
                 office_name, living_space_name="None"):
        self.name = name
        self.role = role
        self.gender = gender
        self.age = age
        self.office_name = office_name
        self.living_space_name = living_space_name


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    room_type = Column(String)

    def __init__(self, name, room_type):
        self.name = name
        self.room_type = room_type


class Unallocated(Base):

    __tablename__ = "unallocated"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    room_type = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, role, room_type, gender, age):

        self.name = name
        self.role = role
        self.room_type = room_type
        self.gender = gender
        self.age = age
