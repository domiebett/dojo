class Person(object):
    """Creates a Person who can either be a Fellow or Staff"""

    def __init__(self, name, role, living_space=False):

        self.id_key = id(self)
        self.name = name
        self.role = role
        self.living_space = living_space
        self.gender = None
        self.age = None
        self.office_name = "None"

    def set_gender(self, gender):
        """Sets the gender of the person"""

        if not isinstance(gender, str):
            return "Should be a string"
        self.gender = gender

    def set_age(self, age):
        """Sets the age of the person"""

        if not isinstance(age, int):
            return "Should be a number"
        self.age = age

    def get_gender(self):
        """Returns the gender of the person"""

        if self.gender is None:
            return "Gender not assigned"
        return self.gender

    def get_age(self):
        """Returns the age of the person"""

        if self.age is None:
            return "Age not assigned"
        return self.age


class Fellow(Person):
    """Constructs a Fellow object"""

    def __init__(self, name, living_space=False):

        super().__init__(name, role="fellow")
        self.name = name
        self.role = "fellow"
        self.living_space = living_space
        self.living_space_name = "None"


class Staff(Person):
    """Constructs a Staff object"""

    def __init__(self, name):

        super().__init__(name, role="staff")
        self.name = name
        self.role = "staff"
