import random
from modules.rooms import Office, LivingSpace
from modules.people import Fellow, Staff


class Dojo():

    """Contains functions to create rooms, add people, and
    printing room allocations
    """

    # initialises the class

    def __init__(self):
        self.office_array = []
        self.living_space_array = []
        self.office_unallocated = []
        self.living_unallocated = []

    # returns a random room that has space for more occupants. Argument
    # passed can be the office_array or the living_space_array.

    def random_empty_rooms(self, array):

        """Generates a random room with space for allocation"""

        empty_rooms = []

        for a in array:
            if a.has_space():
                empty_rooms.append(a)

        # returns "Full if all the rooms are full"

        if len(empty_rooms) <= 0:
            return "Full"

        # select a random room.

        random_room = random.choice(empty_rooms)
        return random_room

    # append people who have no allocated rooms to respective lists above.

    def append_unallocated_persons(self, person_name, person_role="fellow", room="O"):

        """Appends people not allocated to any room to lists"""

        person = ""
        if person_role == "fellow":
            person = Fellow(person_name)
        elif person_role == "staff":
            person = Staff(person_name)
        else:
            return "No such specification"

        if room == "O":
            self.office_unallocated.append(person)
        elif room == "L":
            self.living_unallocated.append(person)

    # Function creates a person object by instantiating the person role
    # class, i.e Fellow or Staff

    def add_person(self, person_name, person_role, accommodation):

        """Adds people and assigns them a room. Adds them to the unallocated
        list if no rooms exist"""

        random_office = self.random_empty_rooms(self.office_array)
        random_living_space = self.random_empty_rooms(self.living_space_array)
        print("\n   " + person_name + " (" + person_role + ")" " has been assigned:")

        # checks if there is an office to add person. If there isn't,
        # appends person to unallocated office array

        if random_office == "Full":

            print("     Offices are full. Assigning to unallocated")
            self.append_unallocated_persons(person_name)
            random_office_name = "UNALLOCATED !!"

        else:
            random_office_name = random_office.name

        # Adds a fellow to a random office that still has space.

        if person_role == "fellow":

            fellow = Fellow(person_name)
            if not random_office == "Full":
                random_office.add_occupant(fellow)
            print("     Office: " + random_office_name)

        # Adds a fellow to a  living space depending on whether
        # they want accommodation.

            if accommodation == "Y":

                if random_living_space == "Full":

                    print("     Living spaces are full. Assigning to unallocated")
                    self.append_unallocated_persons(
                        person_name, person_role, "L")
                    random_living_space_name = "UNALLOCATED !!"

                else:
                    random_living_space_name = random_living_space.name
                    random_living_space.add_occupant(fellow)

                print("     Living Space: " + random_living_space_name + "\n")

        # Adds a staff member to random office with space

        if person_role == "staff":

            staff = Staff(person_name)
            random_office.add_occupant(staff)
            random_office_name = random_office.name
            print("  Office: " + random_office_name)

    # Calls the room creator

    def create_room(self, room_type, room_names):

        """Calls the room creator method with room type and room
        name arguments"""

        for room in room_names:
            self.room_creator(room_type, room)
            self.assign_unallocated(room_type)

        print("\nOffices quantity: " + str(len(self.office_array)) +
              "\nLiving Spaces: " + str(len(self.living_space_array)) +
              "\n")

    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class

    def room_creator(self, room_type, room_name):

        """Creates rooms; either offices or living spaces"""

        office_names = [room.name for room in self.office_array]
        living_space_names = [room.name for room in self.living_space_array]
        rooms = office_names + living_space_names

        # The two below if statements creates an Office or LivingSpace
        # object, depending on the room_type

        if room_type == "office":

            for name in rooms:
                if name == room_name:
                    print("Room named " + room_name + " already exists")
                    return "Room exists"

            new_room = Office(room_name)
            self.add_room(new_room)
            print ("Created office named " + room_name)

        if room_type == "living_space":

            for name in rooms:
                if name == room_name:
                    print("Room named " + room_name + " already exists")
                    return "Room exists"

            new_room = LivingSpace(room_name)
            self.add_room(new_room)
            print("Created Living Space named " + room_name)
        
        return "Created Successfully"

    # Adds rooms created in the main module into their
    # respective arrays above.

    def add_room(self, room):

        """Adds rooms to their respective room array"""

        if isinstance(room, Office):
            self.office_array.append(room)

        elif isinstance(room, LivingSpace):
            self.living_space_array.append(room)

    # Prints all occupants of the argument passed as room_name

    def print_room(self, room_name):

        """Prints occupants in room with name argument"""

        # merges the office and living_space arrays.

        merged_array = self.office_array + self.living_space_array

        if len(merged_array) <= 0:
            return "No room exists"

        # loops through merged_array to find room with the name in
        # passed in as function argument and prints it and its occupants.

        for room in merged_array:

            if room_name == room.name:
                string = "\nAllocation: \n"
                string += "\t Room Name: " + room_name + \
                    " (" + room.room_type + ").\n"

                occupants = room.room_occupants
                string += "\t Occupants:"

                for occupant in occupants:
                    string += "" + occupant.name + ", "

                string += "\n"
                return string

    # Used to print all allocations for all rooms in the Andela dojo.

    def print_allocations(self, output):

        """Prints out all allocations"""

        # Builds a string that contains all the data and either returns
        # it to be printed or makes a new file with the name in argument.

        string = "\nALLOCATIONS: \n"
        string += "\tOFFICES\n"
        string += "\t---------"
        for room in self.office_array:
            string += "\n\tOffice Name: " + room.name + "\n"
            string += "\tOccupants: \n"
            count=1
            for occupant in room.room_occupants:
                string += "\t\t" + str(count) + ". " + occupant.name + "\n"
                count+=1

        string += "\n\tLIVING SPACES\n"
        string += "\t----------------"
        for room in self.living_space_array:
            string += "\n\tLiving Space Name:" + room.name + "\n"
            string += "\tOccupants: \n"
            count = 1
            for occupant in room.room_occupants:
                string += "\t\t" + str(count) + ". " + occupant.name + "\n"
                count+=1

        string += "\n"

        # returns the string to be printed to console.

        if output is None:
            return string

        # creates txt file and writes to it.

        else:
            file_name = "output/" + output + ".txt"
            file_output = open(file_name, "w")
            file_output.write(string)
            file_output.close()
            return "File saved to " + file_name + "."

    # prints all unallocated persons

    def print_unallocated(self, output):

        # builds string with information for unallocated persons

        string = "\nUNALLOCATED: \n"
        string += "\tOFFICES\n"
        string += "\t---------\n"
        for i in range(len(self.office_unallocated)):
            string += "\t\t" + str(i + 1) + ". " + \
                self.office_unallocated[i].name + "\n"

        string += "\n\tLIVING SPACES\n"
        string += "\t---------------\n"
        for i in range(len(self.living_unallocated)):
            string += "\t\t" + str(i + 1) + ". " + \
                self.living_unallocated[i].name + "\n"

        if output is None:
            return string

        else:
            file_name = "output/" + output + ".txt"
            file_output = open(file_name, "w")
            file_output.write(string)
            file_output.close()
            return "File saved to path: '" + file_name + "'."

    def reallocate_person(self, person_identifier, new_room_name):

        pass

    def assign_unallocated(self, room_type):
        if room_type == "office":

            for person in self.office_unallocated:
                empty_room = self.random_empty_rooms(self.office_array)

                if empty_room == "Full":
                    break
                else:
                    empty_room.add_occupant(person)
                    self.office_unallocated.remove(person)
                    print(person.name + " has been added to Office " + empty_room.name)

        if room_type == "living_space":

            for person in self.living_unallocated:
                empty_room = self.random_empty_rooms(self.living_space_array)

                if empty_room == "Full":
                    break
                else:
                    empty_room.add_occupant(person)
                    self.living_unallocated.remove(person)
                    print(person.name + " has been added to Living Space " + empty_room.name)


    # Used to fetch data from the room arrays above.

    def get_rooms(self, room_type):

        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print("Created a " + room.room_type + " named " + room.name)
