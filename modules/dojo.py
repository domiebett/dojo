
import os
import sys
from os import path

from modules.database import Base, People, Rooms, Unallocated
from modules.people import Fellow, Person, Staff
from modules.rooms import LivingSpace, Office, Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools.tools import *
from termcolor import cprint

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
            cprint("\n   The role '" + person_role +
                   "' is not allowed. Only fellows and staff", "red")
            return "Not allowed"

        random_office = random_empty_rooms(self.office_array)
        random_living_space = random_empty_rooms(self.living_space_array)
        cprint("\n   " + person_name +
               " (" + person_role + ")" " has been assigned:", "green")

        # checks if there is an office to add person. If there isn't,
        # appends person to unallocated office array

        if random_office == "Full":

            cprint("     Offices are full. Assigning to unallocated", "yellow")
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
            cprint("     Office: " + random_office_name, "green")

        # Adds a fellow to a  living space depending on whether
        # they want accommodation.

            if accommodation == "Y":

                if random_living_space == "Full":

                    cprint("     Living spaces are full. Assigning to" +
                           " unallocated", "green")
                    self.append_unallocated_persons(
                        person_name, person_role, "L")
                    random_living_space_name = "UNALLOCATED !!"

                else:
                    fellow.living_space_name = random_living_space.name
                    random_living_space_name = random_living_space.name
                    random_living_space.add_occupant(fellow)

                cprint("     Living Space: " + random_living_space_name,
                       "green")

            elif accommodation == "N":
                cprint("     No Living Space allocated", "yellow")

            else:
                cprint("     The above option is not allowed", "red")
                return "Wrong input"

        # Adds a staff member to random office that has space

        if person_role == "staff":

            staff = Staff(person_name)
            if not random_office == "Full":
                staff.office_name = random_office.name
                random_office.add_occupant(staff)
                random_office_name = random_office.name
            cprint("     Office: " + random_office_name, "green")

            if accommodation == "Y":

                cprint("     Staff cannot be assigned living space", "red")
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

        type_array = ["office", "living_space"]
        if room_type not in type_array:
            cprint("   " + room_type + " is not a valid room type.", "red")
            return "Wrong room type"

        for room_name in room_names:
            self.room_creator(room_type, room_name)

        if room_type == "office":
            assign_unallocated(self.office_unallocated,
                               self.office_array)
        elif room_type == "living_space":
            assign_unallocated(self.living_unallocated,
                               self.living_space_array)

        cprint("\n    Offices quantity: " + str(len(self.office_array)) +
               "\n    Living Spaces: " + str(len(self.living_space_array)) +
               "\n", "green")

    def room_creator(self, room_type, room_name):
        """Creates rooms; either offices or living spaces and appends
        it to either office_array or living_space_array"""

        office_names = [room.name for room in self.office_array]
        living_space_names = [room.name for room in self.living_space_array]
        rooms = office_names + living_space_names

        for name in rooms:
            if name.upper() == room_name.upper():
                cprint("Room named " + room_name + " already exists", "red")
                return "Room exists"

        # The two below if statements creates an Office or LivingSpace
        # object, depending on the room_type

        if room_type == "office":

            new_room = Office(room_name)
            self.office_array.append(new_room)

        elif room_type == "living_space":

            new_room = LivingSpace(room_name)
            self.living_space_array.append(new_room)

        else:
            cprint("\n   The room type " + room_type + " is not in system",
                   "red")
            return "Wrong room type"

        cprint("\n   Created " + new_room.room_type + " " + room_name, "green")
        return "Created Successfully"

    def print_room(self, room_name):
        """Prints occupants in room with name parsed as argument"""

        merged_array = self.office_array + self.living_space_array

        if merged_array:

            for room in merged_array:

                if room_name == room.name:
                    string = "\nAllocation: \n"
                    string += "\tRoom Name: " + room_name + \
                        " (" + room.room_type + ").\n"

                    string += occupant_string(room)

                    string += "\n"
                    return string

            return "Room doesnt exist"

        else:
            return ("\n   There are no rooms to print\n")

    def print_allocations(self, output):
        """Returns a string with all allocations in office and living_spaces"""

        title = "\nALLOCATIONS: \n"
        string = "\tOFFICES\n"
        string += "\t---------"

        if self.office_array:
            for room in self.office_array:
                string += "\n\tOffice Name: " + room.name + "\n"
                string += occupant_string(room)

        else:
            string += "\n\tThere are no offices in the system"

        string += "\n\tLIVING SPACES\n"
        string += "\t----------------"

        if self.living_space_array:
            for room in self.living_space_array:
                string += "\n\tLiving Space Name:" + room.name + "\n"
                string += occupant_string(room)

        else:
            string += "\n\tThere are no living spaces in the system"

        string = title + string + "\n"

        # returns the string to be printed to console or creates txt file
        # and writes to it.

        if output is None:
            return string

        else:
            file_name = "output/" + output
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
            file_name = "output/" + output
            with open(file_name, 'w') as file_output:
                file_output = open(file_name, "w")
                file_output.write(string)
                file_output.close()
                return "File saved to path: '" + file_name + "'."

    def reallocate_person(self, person_identifier, room_name):
        """Reallocates person to another room"""

        if not is_int(person_identifier):
            cprint("\n   Id must be an integer, type 'print_allocations' " +
                   "to view all people's id(s)", "red")

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
                    cprint("\n   Person is already in the room\n", "red")
                    return "Wrong reallocation"

                if current_room.room_type == selected_room.room_type:

                    if selected_room.has_space():
                        if selected_room.room_type == "office":
                            selected_person.office_name = selected_room.name
                        elif selected_room.room_type == "living_space":
                            selected_person.living_space_name = selected_room.name

                        selected_room.add_occupant(selected_person)
                        current_room.room_occupants.remove(selected_person)
                        cprint("\n   " + selected_person.name +
                               " has been reallocated to " +
                               selected_room.room_type + " " +
                               selected_room.name + "\n", "green")

                    else:
                        return "Destination is full"

                else:
                    cprint("\n   You have to reallocate to similar room types" +
                           "\n", "red")
                    return "Cannot add to room"

            else:
                cprint("   Person is not allocated to any " +
                       selected_room.room_type + "s", "red")
                return "Person doesnt exist"
        else:
            cprint("   Room doesnt exist", "red")
            return "Room doesnt exist"

    def load_people(self, file_name):
        """Loads people from a text file and adds them to rooms"""

        full_file_name = "input/" + str(file_name) + ".txt"
        try:
            input_file = open(full_file_name)
            data_list = input_file.readlines()

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
                    cprint("\n   Data is corrupt, check format and try again",
                           "red")

            input_file.close()

        except(FileNotFoundError):
            cprint("\n    File not found\n", "red")
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
        cprint("\n   Database " + database_name + " was created successfully",
               "green")

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

        cprint("   All rooms have been added to the database successfully",
               "green")

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
        cprint("   Unallocated persons have been added to the database" +
               "successfully\n", "green")

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
                        cprint("   Office named " + office.name + " retrieved",
                               "green")
                    elif db_room.room_type == "living_space":
                        living_space = LivingSpace(db_room.name)
                        temp_living_array.append(living_space)
                        cprint("   Living space name " +
                               living_space.name + " retrieved", "green")

                # Retrieve people if they exist and add them to rooms

                if session.query(People):

                    for person in session.query(People):
                        if person.role == "fellow":

                            fellow = Fellow(person.name)
                            fellow.office_name = person.office_name

                            if not person.office_name == "None":
                                add_to_room(
                                    fellow, person.office_name,
                                    temp_office_array)

                            fellow.living_space_name = person.living_space_name
                            if not person.living_space_name == "None":
                                add_to_room(
                                    fellow, person.living_space_name,
                                    temp_living_array)

                        elif person.role == "staff":
                            staff = Staff(person.name)
                            staff.office_name = person.office_name
                            if not person.office_name == "None":
                                add_to_room(
                                    staff, person.office_name,
                                    temp_office_array)

                cprint("\n   Successfully retrieved rooms and occupants\n",
                       "green")

                # Check for room conflicts and add rooms based on user input.

                self.add_db_rooms(temp_office_array)
                self.add_db_rooms(temp_living_array)
            else:
                cprint("   There are no rooms in database", "yellow")

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

                cprint("   Successfully retrieved unallocated persons",
                       "green")

            else:
                cprint("   There are no unallocated people in database",
                       "yellow")

        else:
            cprint("There is no database named " + database, "red")
            return "No database"

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
                cprint("\n   There is conflict. Room named " +
                       dbroom_name + " exists in system", "red")
                cprint(
                    "   Which version would you like to keep?\
                     \n   Type 'skip' to keep all system files", "red")
                response = get_input(
                    "      Enter ['database'], ['system'] or ['skip'] >> ")

                if str(response) == "database":
                    cprint("\n    Overwriting system data with database\n",
                           "green")

                    if room.room_type == "office":
                        self.office_array.append(temp_room)
                        self.office_array.remove(room_to_replace)
                    elif room.room_type == "living_space":
                        self.living_space_array.append(temp_room)
                        self.living_space_array.remove(room_to_replace)

                elif str(response) == "system":
                    cprint("\n    Keeping system data\n", "green")

                elif str(response) == "skip":
                    cprint("\n    Keeping default system data", "green")
                    return "Skip"

                else:
                    cprint("   Option: " + response + " is not known. \
                        Please type:\n 'database', 'system' or 'skip'", "red")
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
                        cprint("Room named " + room.name + " has been " +
                               " deleted.", "green")
                        return "Success"
                    elif room.room_type == "living_space":
                        self.living_space_array.remove(room)
                        cprint("Room named " + room.name +
                               " has been deleted from " + room.room_type +
                               "s", "green")
                        return "Success"

        elif del_object == "person":

            if not is_int(identifier):
                cprint("    To delete a person identifier needs to be an" +
                       " integer", "red")
                return "Not integer"

            if selector == "office":
                delete_from_room(self.office_array, identifier)
            elif selector == "living_space":
                delete_from_room(self.living_space_array, identifier)
            elif selector == "unallocated":
                self.delete_from_unallocated(
                    self.office_unallocated, identifier)
                self.delete_from_unallocated(
                    self.living_unallocated, identifier)
            elif selector == "all":
                delete_from_room(self.office_array, identifier)
                delete_from_room(self.living_space_array, identifier)
                delete_from_unallocated(
                    self.office_unallocated, identifier)
                delete_from_unallocated(
                    self.living_unallocated, identifier)

        else:
            cprint("Command not supported, you can only delete 'person'" +
                   " and 'room'", "red")
            return "Wrong object"
