import base64


class Person(object):
    """Creates a Person who can either be a Fellow or Staff"""


    def __init__(self, name, role, living_space=False):

        self.id_key = id(self)
        self.name = name
        self.role = role
        self.living_space = living_space
        self.gender = ""
        self.age = 0

    def set_gender(self, gender):
        """Sets the gender of the person"""
        self.gender = gender

    def set_age(self, age):
        """Sets the age of the person"""
        self.age = age

    def get_gender(self):
        """Returns the gender of the person"""
        if self.gender == "":
            return "Gender not assigned"
        return self.gender

    def get_age(self):
        """Returns the age of the person"""
        if self.gender == 0:
            return "Age not assigned"
        return self.age


class Fellow(Person):
    """Constructs a Fellow object"""

    def __init__(self, name, living_space=False):

        super().__init__(name, role="Fellow")
        self.name = name
        self.role = "Fellow"
        self.living_space = living_space
        self.age = 0
        self.gender = ""


class Staff(Person):
    """Constructs a Staff object"""

    def __init__(self, name):

        super().__init__(name, role="Staff")
        self.name = name
        self.role = "Staff"
        self.age = 0
        self.gender = ""
