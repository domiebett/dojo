import random

from rooms import Room, Office, LivingSpace
from people import Person, Fellow, Staff


class Dojo():

    """Creates two global variables, office_array and 
    living_space_array which are lists that hold data 
    for rooms that are Offices and Living Spaces 
    respectively.
    """

    # initialises the class

    def __init__(self):
        self.office_array = [Office("Blue")]
        self.living_space_array = []

    # Adds rooms created in the main module into their
    # respective arrays above.

    def add_room(self, room):
        if isinstance(room, Office):
            self.office_array.append(room)

        elif isinstance(room, LivingSpace):
            self.living_space_array.append(room)

    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class

    def create_room(self, room_type, room_names):

        # The two below if statements creates an Office or LivingSpace
        # object, same number of times equal to the number of arguments
        # passed for room names in command line

        if room_type == "office":

            for room_name in room_names:
                new_room = Office(room_name)
                self.add_room(new_room)

        if room_type == "living_space":

            for room_name in room_names:
                new_room = LivingSpace(room_name)
                self.add_room(new_room)

        self.get_rooms(room_type)

    # Returns all empty rooms in a office or living space depending
    # on which person (staff|fellow) is been added

    def empty_arrays(self, array):

        empty_rooms = []

        for x in array:
            if not x.is_full():
                empty_rooms.append(x)

        return empty_rooms

    # Function creates a person object by instantiating the person role
    # class, i.e Fellow or Staff

    def add_person(self, person_name, person_role, wants_accomodation):

        empty_rooms = []
        new_person = ""

        # If person is staff, as
        if person_role == "staff":
            new_person = Staff(person_name)
            empty_rooms = self.empty_arrays(self.office_array)

        elif person_role == "fellow":
            new_person = Fellow(person_name)
            empty_rooms = self.empty_arrays(self.office_array)
        
        random_room = random.choice(empty_rooms)
        random_room.add_occupant(new_person)
        
        for x in random_room.room_occupants:
            print (x.name)

    # Used to fetch data from the room arrays in __init__.

    def get_rooms(self, room_type):
        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print ("Created a " + room.room_type + " named " + room.name)