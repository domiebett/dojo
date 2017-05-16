
class Person(object):

    def __init__(self, name, role, living_space=False):
        self.name = name
        self.role = role
        self.living_space = living_space

    # Sets the gender variable

    def set_gender(self, gender):
        self.gender = gender
    
    # Sets the age variable

    def set_age(self, age):
        self.age = age
    
    # Retrieves the gender variable

    def get_gender():
        if(self.gender==""):
            return "Gender not assigned"
        return self.gender

    # Retrieves the age variable

    def get_age():
        if(self.gender == 0):
            return "Age not assigned"
        return self.age


class Fellow(Person):

    def __init__(self, name, living_space=False):
        self.name = name
        self.role = "Fellow"
        self.living_space = living_space
        self.age = 0
        self.gender = ""


class Staff(Person):

    def __init__(self, name):
        self.name = name
        self.role = "Staff"
        self.age = 0
        self.gender = ""