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

    def random_empty_rooms(self, array):

        empty_rooms = []

        for x in array:
            if x.has_space():
                empty_rooms.append(x)

        if len(empty_rooms)<=0:
            return False
            
        random_room = random.choice(empty_rooms)
        return random_room

    # Function creates a person object by instantiating the person role
    # class, i.e Fellow or Staff

    def add_person(self, person_name, person_role, accommodation):

        random_office = self.random_empty_rooms(self.office_array)
        random_living_space = self.random_empty_rooms(self.living_space_array)

        # checks if there is an office to add person

        if type(random_office)=="bool":
            return "All offices are filled"

        random_office_name = ""
        random_living_space_name = "None"

        # Adds a fellow to a random office that still has space.

        if (person_role == "fellow"):

            fellow = Fellow(person_name)
            random_office.add_occupant(fellow)
            random_office_name = random_office.name

        # Adds a fellow to a  living space depending on whether
        # they want accommodation.

            if accommodation=="Y":

                if type(random_living_space)=="bool":
                    return "All living spaces are filled"
                random_living_space.add_occupant(fellow)
                random_living_space_name = random_living_space.name

        # Adds a staff member to random office with space

        if (person_role == "staff"):

            staff = Staff(person_name)
            random_office.add_occupant(staff)
            random_office_name = random_office.name

        print("\n" + person_name + " (" + person_role + ")" " has been assigned:")
        print("  Office: " + random_office_name)
        print("  Living Space: " + random_living_space_name + "\n")

    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class

    def create_room(self, room_type, room_names):
        for room in room_names:
            self.room_creator(room_type, room)

        print("\nOffices quantity: " + str(len(self.office_array)) +
              "\nLiving Spaces: " + str(len(self.living_space_array)) + 
              "\n")

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

    # Adds rooms created in the main module into their
    # respective arrays above.

    def add_room(self, room):
        if isinstance(room, Office):
            self.office_array.append(room)

        elif isinstance(room, LivingSpace):
            self.living_space_array.append(room)

    # Prints all occupants of the argument passed as room_name

    def print_room(self, room_name):

        merged_array = self.office_array + self.living_space_array

        if len(merged_array)<=0:
            return "No room exists"

        for room in merged_array:

            if room_name == room.name:
                string = "\nAllocation: \n"
                string += "\t Room Name: " + room_name + ".\n"

                occupants = room.room_occupants
                string += "\t Occupants:"

                for occupant in occupants:
                    string += "" + occupant.name + ", "

                string += "\n"
                return string

    def print_allocations(self, output):

        string = "\nAllocations: \n"
        string+="\tOffices\n"
        string+="\t---------\n"
        for room in self.office_array:
            string+="\t\tOffice Name: " + room.name + "\n"
            string+="\t\tOccupants: \n"
            for occupant in room.room_occupants:
                string+="\t\t\t" + occupant.name + "\n"
        
        string+="\n\tLiving Spaces\n"
        string+="\t----------------\n"
        for room in self.living_space_array:
            string+="\tLiving Space Name:" + room.name + "\n"
            string+="\t\tOccupants: \n"
            for occupant in room.room_occupants:
                string+="\t\t\t" + occupant.name + "\n"
        
        string+="\n"
        
        if output=="None":
            return string
        else:
            file_name = "output/" + output+".txt"
            file_output = open(file_name, "w")
            file_output.write(string)
            file_output.close()
            return "File saved to " + file_name + "."

    # Used to fetch data from the room arrays above.

    def get_rooms(self, room_type):

        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print ("Created a " + room.room_type + " named " + room.name)


dojo_object = Dojo()
dojo_object.create_room("office", ["Blue"])
dojo_object.create_room("living_space", ["Red"])
dojo_object.create_room("living_space", ["Black"])
dojo_object.add_person("Dominic Bett", "fellow", "Y")
dojo_object.add_person("Kachwany Bett", "fellow", "Y")
dojo_object.add_person("Barazza Bett", "fellow", "Y")

dojo_object.print_allocations("output")
