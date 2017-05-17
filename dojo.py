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
        self.office_array = []
        self.living_space_array = []

    # Adds rooms created in the main module into their
    # respective arrays above.

    def add_room(self, room):
        if isinstance(room, Office):
            self.office_array.append(room)

        elif isinstance(room, LivingSpace):
            self.living_space_array.append(room)

    def empty_rooms(self, array):

        empty_rooms = []

        for x in array:
            if x.has_space():
                empty_rooms.append(x)

        return empty_rooms

    # Function creates a person object by instantiating the person role
    # class, i.e Fellow or Staff

    def add_person(self, person_name, person_role, wants_accommodation):

        empty_offices = self.empty_rooms(self.office_array)
        empty_living_space = self.empty_rooms(self.living_space_array)

        # checks if there is an office to add person

        if (len(empty_offices) <= 0):
            return "There is no office room to add person"

        random_office = random.choice(empty_offices)
        random_office_name = ""
        random_living_space_name = "None"

        # Adds a fellow to a random office that still has space.

        if (person_role == "fellow"):

            fellow = Fellow(person_name)
            random_office.add_occupant(fellow)
            random_office_name = random_office.name

        # Adds a fellow to a  living space depending on whether
        # they want accommodation.
            if (wants_accommodation == "Y"):

                if (len(empty_living_space) <= 0):
                    return "There is no living space to add person"

                random_living_space = random.choice(empty_living_space)
                random_living_space.add_occupant(fellow)
                random_living_space_name = random_living_space.name

        # Adds a staff member to random office with space

        if (person_role == "staff"):

            staff = Staff(person_name)
            random_office.add_occupant(staff)
            random_office_name = random_office.name

        print("\n" + person_name + " (" + person_role + ")" " has been assinged:")
        print("  Office: " + random_office_name)
        print("  Living Space: " + random_living_space_name + "\n")

    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class

    def create_room(self, room_type, room_names):
        for room in room_names:
            self.room_creator(room_type, room)

        print("You have Offices: " + str(len(self.office_array)) +
              "\n and Living Spaces: " + str(len(self.living_space_array)))

    def room_creator(self, room_type, room_name):

        office_names = [room.name for room in self.office_array]
        living_space_names = [room.name for room in self.living_space_array]
        rooms = office_names + living_space_names

        # The two below if statements creates an Office or LivingSpace
        # object, same number of times equal to the number of arguments
        # passed for room names in command line

        if room_type == "office":

            for name in rooms:
                if name == room_name:
                    print("Room named " + room_name + " already exists")
                    return "Room exists"

            new_room = Office(room_name)
            self.add_room(new_room)

        if room_type == "living_space":

            for name in rooms:
                if name == room_name:
                    print("Room named " + room_name + " already exists")
                    return "Room exists"

            new_room = LivingSpace(room_name)
            self.add_room(new_room)

        self.get_rooms(room_type)

    def print_room(self, room_name):

        merged_array = self.office_array + self.living_space_array
        occupants = []
        string = "\nAllocation: \n"
        string += "\t Office Name: " + room_name + ".\n"
        for room in merged_array:
            if room_name == room.name:
                occupants = room.room_occupants
            else:
                occupants = "Sorry, but there is no such room"
                return "No such room exists"

        string += "\t Occupants:"

        for occupant in occupants:
            string += "" + occupant.name + ", "

        string += "\n"
        print(string)

    # Used to fetch data from the room arrays above.

    def get_rooms(self, room_type):
        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print ("Created a " + room.room_type + " named " + room.name)


# dojo_object = Dojo()
# dojo_object.create_room("office", ["Blue"])
# dojo_object.create_room("living_space", ["Red"])
# dojo_object.add_person("Dominic Bett", "fellow", "Y")
# dojo_object.add_person("Kachwany Bett", "fellow", "N")
# dojo_object.add_person("Barazza Bett", "fellow", "N")
# print(dojo_object.living_space_array)

# dojo_object.print_room("Blue")
