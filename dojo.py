import random
from rooms import Room, Office, LivingSpace
from people import Person, Fellow, Staff


class Dojo():

    """Creates two global variables, office_array and 
    living_space_array which are lists that hold data 
    for rooms that are Offices and Living Spaces 
    respectively.
    """

    #initialises the class

    def __init__(self):
        self.office_array = []
        self.office_array.append(Office("Blue"))
        self.living_space_array = []
        self.living_space_array.append(LivingSpace("Red"))

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
            if not x.is_full():
                empty_rooms.append(x)

        return empty_rooms


    # Function creates a person object by instantiating the person role
    # class, i.e Fellow or Staff

    def add_person(self, person_name, person_role, wants_accommodation):

        empty_offices = self.empty_rooms(self.office_array)
        empty_living_space = self.empty_rooms(self.living_space_array)

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

        office_names = [room.name for room in self.office_array]
        living_space_names = [room.name for room in self.living_space_array]
        rooms = office_names + living_space_names


        # The two below if statements creates an Office or LivingSpace
        # object, same number of times equal to the number of arguments
        # passed for room names in command line

        if room_type == "office":

            for room_name in room_names:
                for name in rooms:
                    if name == room_name:
                        print("Room exists")
                        return "Room exists"

                new_room = Office(room_name)
                self.add_room(new_room)

        if room_type == "living_space":

            for room_name in room_names:
                new_room = LivingSpace(room_name)
                self.add_room(new_room)

        self.get_rooms(room_type)

    # Used to fetch data from the room arrays above.

    def get_rooms(self, room_type):
        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print ("Created a " + room.room_type + " named " + room.name)
