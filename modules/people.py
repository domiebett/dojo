
class Person(object):
    """Creates a Person who can either be a Fellow or Staff"""

    def __init__(self, name, role, living_space=False):

        self.name = name
        self.role = role
        self.id_key = 0
        self.living_space = living_space
        self.gender = ""
        self.age = 0

    # Sets the gender variable

    def set_gender(self, gender):
        """Sets the gender of the person"""
        self.gender = gender

    # Sets the age variable

    def set_age(self, age):
        """Sets the age of the person"""
        self.age = age

    # Retrieves the gender variable

    def get_gender(self):
        """Returns the gender of the person"""
        if self.gender == "":
            return "Gender not assigned"
        return self.gender

    # Retrieves the age variable

    def get_age(self):
        """Returns the age of the person"""
        if self.gender == 0:
            return "Age not assigned"
        return self.age


class Fellow(Person):
    """Constructs a Fellow object"""

    def __init__(self, name, living_space=False):

        self.name = name
        self.role = "Fellow"
        self.living_space = living_space
        self.age = 0
        self.gender = ""


class Staff(Person):
    """Constructs a Staff object"""

    def __init__(self, name):

        self.name = name
        self.role = "Staff"
        self.age = 0
        self.gender = ""
