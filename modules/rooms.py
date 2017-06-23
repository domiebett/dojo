from modules.people import Staff
from abc import ABCMeta, abstractmethod


class Room(object):

    __metaclass__ = ABCMeta

    """Is a room object which contains functions to be imported by
    livingspace and office objects"""

    @abstractmethod
    def abs_method(self):
        pass

    def has_space(self):
        """Checks if room has space or if it is full"""

        if len(self.occupants) < self.maximum_people:
            return True
        return False

    def add_occupant(self, person):
        """Adds occupants to the rooms. Also checks if occupant is Staff
        and denies them access to the Living Space"""

        if not self.has_space():
            print("   This room is full, try another")
            return "This room is full, try another"
        elif isinstance(self, LivingSpace):
            if isinstance(person, Staff):
                print("   Staff are not allowed in Living Space")
                return "Staff not allowed in Living Space"
            else:
                self.occupants.append(person)
        else:
            self.occupants.append(person)


class LivingSpace(Room):

    """Creates a Living Space object for fellows in the Dojo Facilities"""

    def __init__(self, name):

        self.name = name
        self.type = "living_space"
        self.maximum_people = 4
        self.occupants = []


class Office(Room):

    """Creates Offices for the Dojo Facility"""

    def __init__(self, name):

        self.name = name
        self.type = "office"
        self.maximum_people = 6
        self.occupants = []
