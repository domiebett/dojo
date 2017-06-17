
import os
import sys
from os import path

from modules.database import Base, People, Rooms, Unallocated
from modules.people import Fellow, Person, Staff
from modules.rooms import LivingSpace, Office, Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools.tools import get_input, is_int, random_empty_rooms

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


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

    def add_person(self, person_name, person_role, accommodation="N"):
        """Creates people and assigns them a room. Adds them to the unallocated
        list if no rooms exist"""

        if not person_role == "fellow" and not person_role == "staff":
            print("\n   The role '" + person_role +
                  "' is not allowed. Only fellows and staff")
            return "Not allowed"

        random_office = random_empty_rooms(self.office_array)
        random_living_space = random_empty_rooms(self.living_space_array)
        print("\n   " + person_name +
              " (" + person_role + ")" " has been assigned:")

        # checks if there is an office to add person. If there isn't,
        # appends person to unallocated office array

        if random_office == "Full":

            print("     Offices are full. Assigning to unallocated")
            self.append_unallocated_persons(person_name, person_role)
            random_office_name = "UNALLOCATED !!"

        else:
            random_office_name = random_office.name

        # Adds a fellow to a random office that still has space.

        if person_role == "fellow":

            fellow = Fellow(person_name)
            if not random_office == "Full":
                fellow.office_name = random_office.name
                random_office.add_occupant(fellow)
            print("     Office: " + random_office_name)

        # Adds a fellow to a  living space depending on whether
        # they want accommodation.

            if accommodation == "Y":

                if random_living_space == "Full":

                    print("     Living spaces are full. Assigning to" +
                          " unallocated")
                    self.append_unallocated_persons(
                        person_name, person_role, "L")
                    random_living_space_name = "UNALLOCATED !!"

                else:
                    fellow.living_space_name = random_living_space.name
                    random_living_space_name = random_living_space.name
                    random_living_space.add_occupant(fellow)

                print("     Living Space: " + random_living_space_name)

            elif accommodation == "N":
                print("     No Living Space allocated")

            else:
                print("     The above option is not allowed")
                return "Wrong input"

        # Adds a staff member to random office that has space

        if person_role == "staff":

            staff = Staff(person_name)
            if not random_office == "Full":
                staff.office_name = random_office.name
                random_office.add_occupant(staff)
                random_office_name = random_office.name
            print("     Office: " + random_office_name)

            if accommodation == "Y":

                print("     Staff cannot be assigned living space")
                return "Wrong allocation"

    def append_unallocated_persons(
            self, person_name, person_role="fellow", room="O"):
        """Appends people not allocated to any room to unallocated lists"""

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

    def create_room(self, room_type, room_names):
        """Calls the room creator method with room type and an array
        of room names as arguments"""

        for room_name in room_names:
            self.room_creator(room_type, room_name)
        self.assign_unallocated(room_type)

        print("\nOffices quantity: " + str(len(self.office_array)) +
              "\nLiving Spaces: " + str(len(self.living_space_array)) +
              "\n")

    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class

    def room_creator(self, room_type, room_name):
        """Creates rooms; either offices or living spaces and appends
        it to either office_array or living_space_array"""

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
            self.office_array.append(new_room)
            print("\n   Created office named " + room_name)

        if room_type == "living_space":

            for name in rooms:
                if name == room_name:
                    print("Room named " + room_name + " already exists")
                    return "Room exists"

            new_room = LivingSpace(room_name)
            self.living_space_array.append(new_room)
            print("\n   Created Living Space named " + room_name)

        return "Created Successfully"

    def print_room(self, room_name):
        """Prints occupants in room with name parsed as argument"""

        merged_array = self.office_array + self.living_space_array
        room_exists = False

        for room in merged_array:
            if room.name == room_name:
                room_exists = True

        if not room_exists:
            return "No room exists"

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

    def print_allocations(self, output):
        """Returns a string with all allocations in office and living_spaces"""

        string = "\nALLOCATIONS: \n"
        string += "\tOFFICES\n"
        string += "\t---------"
        for room in self.office_array:
            string += "\n\tOffice Name: " + room.name + "\n"
            string += "\tOccupants: \n"
            count = 1

            data = [[" ", "Name", "|", "Id"], [" ", "-----", "", "---"]]

            # Arranges occupant information into a list which is then appended
            # to the 'data' list to be used to display data to console.

            for occupant in room.room_occupants:
                data.append([(str(count) + ". "), occupant.name,
                             "|", str(occupant.id_key)])
                count += 1

            col_width = [max(map(len, col))
                         for col in zip(*data)]  # Spaces between columns

            # Takes each list from the data list above and arranges it as
            # rows, with columns spaced with the maximum column width plus
            # col_width

            for row in data:
                string += "\t\t" + (" ".join((val.ljust(width)
                                              for val, width
                                              in zip(row, col_width))) + "\n")

        string += "\n\tLIVING SPACES\n"
        string += "\t----------------"
        for room in self.living_space_array:
            string += "\n\tLiving Space Name:" + room.name + "\n"
            string += "\tOccupants: \n"
            count = 1
            data = [[" ", "Name", "|", "Id"], [" ", "-----", "", "---"]]
            for occupant in room.room_occupants:
                data.append([(str(count) + ". "), occupant.name,
                             "|", str(occupant.id_key)])
                count += 1

            col_width = [max(map(len, col)) for col in zip(*data)]
            for row in data:
                string += "\t\t" + (" ".join((val.ljust(width)
                                              for val, width
                                              in zip(row, col_width))) + "\n")

        string += "\n"

        # returns the string to be printed to console or creates txt file
        # and writes to it.

        if output is None:
            return string

        else:
            file_name = "output/" + output + ".txt"
            with open(file_name, 'w') as file_output:
                file_output = open(file_name, "w")
                file_output.write(string)
                file_output.close()
                return "File saved to " + file_name + "."

    def print_unallocated(self, output):
        """Returns all unallocated persons either printed to console or
        to text file"""

        string = "\nUNALLOCATED: \n"
        string += "\tOFFICES\n"
        string += "\t---------\n"
        data = [[" ", "Name", "|", "Id"], [" ", "-----", "", "---"]]
        count = 1

        for person in self.office_unallocated:

            data.append([(str(count) + ". "), person.name,
                         "|", str(person.id_key)])
            count += 1

        col_width = [max(map(len, col)) for col in zip(*data)]
        for row in data:
            string += "\t\t" + (" ".join((val.ljust(width)
                                          for val, width
                                          in zip(row, col_width))) + "\n")

        string += "\n\tLIVING SPACES\n"
        string += "\t---------------\n"
        data = [[" ", "Name", "|", "Id"], [" ", "-----", "", "---"]]
        count = 1

        for person in self.living_unallocated:

            data.append([(str(count) + ". "), person.name,
                         "|", str(person.id_key)])
            count += 1

        col_width = [max(map(len, col)) for col in zip(*data)]
        for row in data:
            string += "\t\t" + (" ".join((val.ljust(width)
                                          for val, width
                                          in zip(row, col_width))) + "\n")

        if output is None:
            return string

        else:
            file_name = "output/" + output + ".txt"
            with open(file_name, 'w') as file_output:
                file_output = open(file_name, "w")
                file_output.write(string)
                file_output.close()
                return "File saved to path: '" + file_name + "'."

    def assign_unallocated(self, room_type):
        """Automatically allocates unallocated people to rooms if one exists"""

        if room_type == "office":

            for i in range(len(self.office_unallocated)):
                empty_room = random_empty_rooms(self.office_array)

                if empty_room == "Full":
                    break
                else:
                    person = self.office_unallocated[0]
                    person.office_name = empty_room.name
                    empty_room.add_occupant(person)
                    self.office_unallocated.remove(person)
                    print("\t" + person.name +
                          " has been added to Office " + empty_room.name)

        if room_type == "living_space":

            for i in range(len(self.living_unallocated)):
                empty_room = random_empty_rooms(self.living_space_array)

                if empty_room == "Full":
                    break
                else:
                    person = self.living_unallocated[0]
                    person.living_space_name = empty_room.name
                    empty_room.add_occupant(person)
                    self.living_unallocated.remove(person)
                    print("\t" + person.name +
                          " has been added to Living Space " + empty_room.name)

    def reallocate_person(self, person_identifier, room_name):
        """Reallocates person to another room"""

        if not is_int(person_identifier):
            print("\n   Id must be an integer, type 'print_allocations' " +
                  "to view all people's id(s)")

            return "Not an integer"

        selected_room = "None"
        selected_person = "None"
        current_room = "None"
        merged_array = self.office_array + self.living_space_array

        # Finds current room, room to be reallocated to and person
        # for reallocation and assigns them to variables
        for room in merged_array:
            if room.name == room_name:
                selected_room = room

                if selected_room.room_type == "office":
                    for office in self.office_array:
                        for person in office.room_occupants:
                            if int(person.id_key) == int(person_identifier):
                                current_room = office
                                selected_person = person
                                break

                elif selected_room.room_type == "living_space":
                    for living_space in self.living_space_array:
                        for person in living_space.room_occupants:
                            if int(person.id_key) == int(person_identifier):
                                current_room = living_space
                                selected_person = person
                                break

        # Reallocates person if room_type match, person & room exists and
        # destination is not full

        if isinstance(selected_room, Room):

            if isinstance(selected_person, Person):

                if current_room.name == room_name:
                    print("\n   Person is already in the room\n")
                    return "Wrong reallocation"

                if current_room.room_type == selected_room.room_type:

                    if selected_room.has_space():
                        if selected_room.room_type == "office":
                            selected_person.office_name = selected_room.name
                        elif selected_room.room_type == "living_space":
                            selected_person.living_space_name = selected_room.name

                        selected_room.add_occupant(selected_person)
                        current_room.room_occupants.remove(selected_person)
                        print("\n   " + selected_person.name +
                              " has been reallocated to " +
                              selected_room.room_type + " " +
                              selected_room.name + "\n")

                    else:
                        return "Destination is full"

                else:
                    print("\n   You have to reallocate to similar room types" +
                          "\n")
                    return "Cannot add to room"

            else:
                print("   Person is not allocated to any " +
                      selected_room.room_type + "s")
                return "Person doesnt exist"
        else:
            print("   Room doesnt exist")
            return "Room doesnt exist"

    def load_people(self, file_name):
        """Loads people from a text file and adds them to rooms"""

        full_file_name = "input/" + str(file_name) + ".txt"
        try:
            input_file = open(full_file_name)
            data_list = input_file.readlines()
            person_name = ""
            person_role = ""
            person_accommodation = ""

            # Loops through all lines in text file checking for data integrity
            # then calls the add person function to create and assign random
            # room

            for data in data_list:
                person_data = data.split()

                if len(person_data) >= 3 and len(person_data) <= 4:
                    person_name = str(
                        person_data[0]) + " " + str(person_data[1])
                    person_role = str(person_data[2])

                    if len(person_data) == 4:
                        person_accommodation = str(person_data[3])
                    else:
                        person_accommodation = "N"

                    self.add_person(person_name, person_role,
                                    person_accommodation)
                else:
                    print("\n   Data is corrupt, check format and try again")

            input_file.close()

        except(FileNotFoundError):
            print("\n    File not found\n")
            return "File not found"

    def save_state(self, database=None):
        """Saves data for rooms, persons, and unallocated persons to the sqlite
        database provided, saves to default.db if no database is provided"""

        if database is None:
            database = "default.db"
        if os.path.exists(database):
            os.remove(database)

        database_name = "sqlite:///" + str(database)
        engine = create_engine(database_name)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        print("\n   Database " + database_name + " was created successfully")

        Session = sessionmaker(bind=engine)
        session = Session()

        # Add rooms

        merged_rooms = self.office_array + self.living_space_array
        people_array = []
        for room in merged_rooms:
            room_name = room.name
            room_type = room.room_type
            db_room = Rooms(room_name, room_type)
            session.add(db_room)

            # Filter people to avoid duplicates

            for person in room.room_occupants:

                if person not in people_array:
                    people_array.append(person)

        session.commit()

        # Add people

        for person in people_array:

            person_living_space_name = ""
            if person.role == "fellow":
                person_living_space_name = person.living_space_name
            elif person.role == "staff":
                person_living_space_name = "None"

            db_person = People(person.name, person.role, person.gender,
                               person.age, person.office_name,
                               person_living_space_name)

            session.add(db_person)

        session.commit()

        print("   All rooms have been added to the database successfully")

        # Add unallocated persons

        merged_unallocated = self.office_unallocated + self.living_unallocated
        for person in merged_unallocated:

            if person in self.office_unallocated:
                room_type = "office"
            if person in self.living_unallocated:
                room_type = "living_space"

            db_unallocated = Unallocated(person.name, person.role, room_type,
                                         person.gender, person.age)
            session.add(db_unallocated)

        session.commit()
        print("   Unallocated persons have been added to the database" +
              "successfully\n")

        if os.path.exists(database):
            return "Success"

    def load_state(self, database=None):
        """Loads data from sqlite database using SQLAlchemy library."""

        if database is None:
            database = "default.db"

        # Checks if db file exists.
        temp_office_array = []
        temp_living_array = []

        if os.path.exists(database):

            database_name = "sqlite:///" + str(database)
            engine = create_engine(database_name)

            Session = sessionmaker(bind=engine)
            session = Session()

            # Retrieve rooms if they exist

            if session.query(Rooms):

                for db_room in session.query(Rooms):
                    if db_room.room_type == "office":
                        office = Office(db_room.name)
                        temp_office_array.append(office)
                        print("   Office named " + office.name + " retrieved")
                    elif db_room.room_type == "living_space":
                        living_space = LivingSpace(db_room.name)
                        temp_living_array.append(living_space)
                        print("   Living space name " +
                              living_space.name + " retrieved")

                # Retrieve people if they exist and add them to rooms

                if session.query(People):

                    for person in session.query(People):
                        if person.role == "fellow":

                            fellow = Fellow(person.name)
                            fellow.office_name = person.office_name

                            if not person.office_name == "None":
                                self.add_to_room(
                                    fellow, person.office_name,
                                    temp_office_array)

                            fellow.living_space_name = person.living_space_name
                            if not person.living_space_name == "None":
                                self.add_to_room(
                                    fellow, person.living_space_name,
                                    temp_living_array)

                        elif person.role == "staff":
                            staff = Staff(person.name)
                            staff.office_name = person.office_name
                            if not person.office_name == "None":
                                self.add_to_room(
                                    staff, person.office_name,
                                    temp_office_array)

                print("\n   Successfully retrieved rooms and occupants\n")

                # Check for room conflicts and add rooms based on user input.

                self.add_db_rooms(temp_office_array)
                self.add_db_rooms(temp_living_array)
            else:
                print("   There are no rooms in database")

            # Retrieve unallocated persons if they exist

            if session.query(Unallocated):

                for person in session.query(Unallocated):
                    if person.role == "fellow":
                        fellow = Fellow(person.name)
                        if person.room_type == "office":
                            self.office_unallocated.append(fellow)
                        elif person.room_type == "living_space":
                            self.living_unallocated.append(fellow)
                    if person.role == "staff":
                        staff = Staff(person.name)
                        if person.room_type == "office":
                            self.office_unallocated.append(staff)

                print("   Successfully retrieved unallocated persons")

            else:
                print("   There are no unallocated people in database")

        else:
            print("There is no database named " + database)
            return "No database"

    def add_to_room(self, person, room_name, array):
        """Finds room with name that matches argument 'room_name' and adds
        person to it"""

        for room in array:
            if room_name == room.name:

                room.add_occupant(person)
                print("\n     Added " + person.name + " to " + room_name)
                return "Success"

    def add_db_rooms(self, rooms_array):
        """Checks for conflicts between db rooms and system rooms and requests user
        input to either keep system data or overwrite it with database data"""

        merged_array = self.office_array + self.living_space_array
        room_to_replace = None

        # Checks if room exist

        for temp_room in rooms_array:
            room_conflict = False

            for room in merged_array:
                dbroom_name = temp_room.name
                if room.name == dbroom_name:
                    room_conflict = True
                    room_to_replace = room
                    break

            # If room exists then gives option to keep or overwrite system data

            if room_conflict:
                print("\n   There is conflict. Room named " +
                      dbroom_name + " exists in system")
                print(
                    "   Which version would you like to keep?\
                     \n   Type 'skip' to keep all system files")
                response = get_input(
                    "      Enter ['database'], ['system'] or ['skip'] >> ")

                if str(response) == "database":
                    print("\n    Overwriting system data with database\n")

                    if room.room_type == "office":
                        self.office_array.append(temp_room)
                        self.office_array.remove(room_to_replace)
                    elif room.room_type == "living_space":
                        self.living_space_array.append(temp_room)
                        self.living_space_array.remove(room_to_replace)

                elif str(response) == "system":
                    print("\n    Keeping system data\n")

                elif str(response) == "skip":
                    print("\n    Keeping default system data")
                    return "Skip"

                else:
                    print("   Option: " + response + " is not known. \
                        Please type:\n 'database', 'system' or 'skip'")
                    self.add_db_rooms(rooms_array)

            else:
                if temp_room.room_type == "office":
                    self.office_array.append(temp_room)
                elif temp_room.room_type == "living_space":
                    self.living_space_array.append(temp_room)

    def delete_object(self, del_object, identifier, selector="all"):
        """Deletes either room or person. Room's identifier is room name while
        person identifier is his id_key. selector gives options to delete from
        the office, living_space or unallocated, or all"""

        merged_array = self.office_array + self.living_space_array

        if del_object == "room":

            for room in merged_array:
                if room.name == identifier:
                    if room.room_type == "office":
                        self.office_array.remove(room)
                        print("Room named " + room.name + " has been deleted.")
                        return "Success"
                    elif room.room_type == "living_space":
                        self.living_space_array.remove(room)
                        print("Room named " + room.name +
                              " has been deleted from " + room.room_type + "s")
                        return "Success"

        elif del_object == "person":

            if not is_int(identifier):
                print("    To delete a person identifier needs to be an" +
                      "integer")
                return "Not integer"

            if selector == "office":
                self.delete_from_room(self.office_array, identifier)
            elif selector == "living_space":
                self.delete_from_room(self.living_space_array, identifier)
            elif selector == "unallocated":
                self.delete_from_unallocated(
                    self.office_unallocated, identifier)
                self.delete_from_unallocated(
                    self.living_unallocated, identifier)
            elif selector == "all":
                self.delete_from_room(self.office_array, identifier)
                self.delete_from_room(self.living_space_array, identifier)
                self.delete_from_unallocated(
                    self.office_unallocated, identifier)
                self.delete_from_unallocated(
                    self.living_unallocated, identifier)

        else:
            print("Command not supported, you can only delete 'person'" +
                  " and 'room'")
            return "Wrong object"

    def delete_from_room(self, array, identifier):
        """Used to delete people from specific rooms"""

        for room in array:
            for occupant in room.room_occupants:
                if occupant.id_key == int(identifier):
                    room.room_occupants.remove(occupant)
                    print("Occupant " + occupant.name +
                          " has been deleted from " + room.room_type + " " +
                          room.name)

    def delete_from_unallocated(self, array, identifier):
        """Used to delete unallocated people"""

        for person in array:
            if person.id_key == int(identifier):
                array.remove(person)
                print("Removed " + person.name + " from waiting list")
