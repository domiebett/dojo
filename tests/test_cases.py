import unittest
from unittest import mock
import os
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from modules.rooms import Room, Office, LivingSpace
from modules.dojo import Dojo
from modules.people import Fellow, Staff


class CreateRoomTestCase(unittest.TestCase):
    """Tests for the create_room and some add_person functionality"""

    def setUp(self):

        self.dojo = Dojo()
        self.dojo.create_room("office", ["Blue"])
        self.dojo.create_room("living_space", ["Red"])

    def tearDown(self):

        self.dojo.offices[0].occupants[:] = []

    def test_create_room(self):
        office = self.dojo.offices[0]
        living = self.dojo.living_spaces[0]
        self.assertListEqual([office.name, office.type],
                         ["Blue", "office"])
        self.assertListEqual([living.name, living.type],
                         ["Red", "living_space"])

    def test_rooms_are_instances_of_room(self):

        self.assertIsInstance(self.dojo.offices[0], Room)
        self.assertIsInstance(self.dojo.living_spaces[0], Room)

    def test_only_office_or_living_space_allowed(self):

        wrong_type = self.dojo.create_room("blah", ["White"])
        self.assertEqual(wrong_type, "Wrong room type")


class AddPersonTestCase(unittest.TestCase):

    """Tests for functionalities of the add_person() function in dojo.py"""

    def setUp(self):
        self.dojo = Dojo()
        self.dojo.add_person("Dominic", "fellow", "Y")

    def test_office_unallocation(self):
        unallocated = self.dojo.office_unallocated
        self.assertEqual(unallocated[0].name, "Dominic")

    def test_living_space_unallocation(self):
        unallocated = self.dojo.living_unallocated
        self.assertEqual(unallocated[0].name, "Dominic")

    def test_only_fellow_and_staff_allowed(self):
        illegal_person = self.dojo.add_person(
            "Dominic Bett", "boogey_man", "Y")
        self.assertEqual(illegal_person, "Wrong person role")

    def test_staff_doesnt_get_living_space(self):
        staff_accommodation = self.dojo.add_person(
            "Patrick Sacho", "staff", "Y")
        self.assertEqual(self.dojo.office_unallocated[1].name,
                         "Patrick Sacho")
        self.assertEqual(staff_accommodation,
                         "Cannot add staff to living space")

    def test_only_Y_option_allocates_accomodation(self):
        illegal_accommodation = self.dojo.add_person(
            "Patrick Sacho", "fellow", "P")
        self.assertEqual(illegal_accommodation,
                         "Person not allocated a living space")

    def test_unallocated_is_automatically_added_to_room(self):
        self.dojo.create_room("office", ["Yellow"])
        self.assertEqual(self.dojo.offices[0].occupants[0].name,
                         "Dominic")
        unallocated = self.dojo.office_unallocated
        self.assertEqual(len(unallocated), 0)

    def test_person_allocation(self):
        self.dojo.create_room("office", ["Blue"])
        self.dojo.add_person("Darren", "fellow")
        occupants = self.dojo.offices[0].occupants
        self.assertListEqual([occupants[0].name, occupants[1].name],
                             ["Dominic", "Darren"])


class AllocationsTestCase(unittest.TestCase):

    """Tests for print_room, print_allocations, and print_unallocated
    functions"""

    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", ["Yellow"])
        self.dojo.create_room("living_space", ["Red"])
        self.dojo.add_person("Dominic", "fellow", "Y")
        self.dojo.add_person("Jamie Heineman", "staff")
        self.dojo.add_person("Grant Imahara", "fellow")

    def test_right_number_of_occupants_is_in_room(self):
        test_room = self.dojo.offices[0]
        occupant_list = [occupant.name for occupant in test_room.occupants]
        self.assertListEqual(occupant_list, ["Dominic", "Jamie Heineman",
                                          "Grant Imahara"])

    def test_room_exists(self):
        print_room = self.dojo.print_room("White")
        self.assertEqual(print_room, "Room doesnt exist")

    def test_print_room(self):
        printed_room = self.dojo.print_room("Yellow")
        self.assertIsInstance(printed_room, str)

    def test_print_allocations_outputs_to_file(self):
        string = "File saved to output/tests.txt."
        allocation_string = self.dojo.print_allocations("tests.txt")
        self.assertEqual(string, allocation_string)

    def test_print_unallocated_outputs_to_file(self):
        string = "File saved to path: 'output/tests.txt'."
        unallocated_string = self.dojo.print_unallocated("tests.txt")
        self.assertEqual(string, unallocated_string)


class ReallocateTestCase(unittest.TestCase):

    """Test the reallocated_person() function in dojo.py"""

    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", ["Blue"])
        self.dojo.add_person("Dominic", "fellow", "N")
        self.dojo.add_person("Darren Kasengo", "fellow", "Y")
        self.dojo.create_room("office", ["White"])
        self.dojo.create_room("living_space", ["Yellow"])
        self.offices = self.dojo.offices

    def test_reallocate_person(self):
        person_id = self.offices[0].occupants[0].id_key
        self.dojo.reallocate_person(person_id, "White")
        self.assertEqual(self.offices[1].occupants[0].name,
                         "Dominic")
        self.assertEqual(len(self.offices[0].occupants),
                         1)

    def test_reallocation_is_between_similar_room_types(self):
        occupant = self.offices[0].occupants[0]
        wrong_reallocation = self.dojo.reallocate_person(occupant.id_key,
                                                         "Yellow")
        self.assertEqual(wrong_reallocation, "Wrong reallocation")

    def test_reallocation_is_between_existing_rooms(self):
        wrong_reallocation = self.dojo.reallocate_person(
            50484848111, "Black")
        self.assertEqual(wrong_reallocation, "Room doesnt exist")

    def test_only_existing_persons_are_reallocated(self):
        wrong_reallocation = self.dojo.reallocate_person(
            504, "White")
        self.assertEqual(wrong_reallocation, "Wrong reallocation")

    def test_only_integers_are_allowed(self):
        wrong_id = self.dojo.reallocate_person("string", "White")
        self.assertEqual(wrong_id, "Not an integer")

    def test_person_is_not_moved_if_there_destination_is_full(self):
        for _ in range(12):
            self.dojo.add_person("Dominic Bett", "fellow", "N")
        person_id = self.dojo.offices[0].occupants[0].id_key
        wrong_reallocation = self.dojo.reallocate_person(
            person_id, "White")
        self.assertEqual(wrong_reallocation, "Destination is full")

    def test_reallocation_is_not_to_same_room(self):
        occupant1 = self.dojo.offices[0].occupants[0]
        wrong_reallocation = self.dojo.reallocate_person(
            int(id(occupant1)), "Blue")
        self.assertEqual(wrong_reallocation, "Wrong reallocation")


class LoadPeopleTestCase(unittest.TestCase):

    """Tests the load_people function in dojo.py"""

    def setUp(self):
        self.dojo = Dojo()

    def test_people_are_added_to_room(self):
        self.dojo.create_room("office", ["Blue"])
        self.dojo.load_people("input.txt")
        occupants = self.dojo.offices[0].occupants
        self.assertEqual(len(occupants), 5)

    def test_returns_message_if_txt_file_doesnt_exist(self):
        no_file = self.dojo.load_people("no_file.txt")
        self.assertEqual(no_file, "File not found")


class PeopleTestCase(unittest.TestCase):

    """Test the entire Person, Fellow and Staff objects"""

    def setUp(self):
        self.fellow = Fellow("Dominic Bett", "Y")
        self.staff = Staff("Dominic Bett")

    def test_gender_is_assigned(self):
        self.fellow.set_gender("Female")
        self.staff.set_gender("Male")
        self.assertEqual(self.fellow.gender, "Female")
        self.assertEqual(self.staff.gender, "Male")

    def test_age_is_assingned(self):
        self.fellow.set_age(21)
        self.staff.set_age(20)
        self.assertEqual(self.fellow.age, 21)
        self.assertEqual(self.staff.age, 20)

    def test_unassigned_age_gender_error(self):
        self.assertEqual(self.fellow.get_gender(), "Gender not assigned")
        self.assertEqual(self.fellow.get_age(), "Age not assigned")

    def test_age_and_gender_is_returned(self):
        self.fellow.set_gender("Male")
        self.staff.set_age(22)
        self.assertEqual(self.fellow.get_gender(), "Male")
        self.assertEqual(self.staff.get_age(), 22)

    def test_age_and_gender_wrong_format(self):
        wrong_age = self.fellow.set_age("Twenty One")
        wrong_gender = self.fellow.set_gender(474747)
        self.assertEqual(wrong_age, "Should be a number")
        self.assertEqual(wrong_gender, "Should be a string")


class RoomsTestCase(unittest.TestCase):
    """Test all Room, Office, LivingSpace objects"""

    def setUp(self):
        self.office = Office("Office_Name")
        self.living = LivingSpace("Living_Name")

    def test_add_occupant(self):
        self.office.add_occupant(Fellow("Dom Bett"))
        self.living.add_occupant(Fellow("Dom Bett"))
        self.assertTrue(self.office.occupants[0].name, "Dom Bett")
        self.assertEqual(self.living.occupants[0].name, "Dom Bett")

    def test_has_space(self):
        self.assertTrue(self.office.has_space())
        for _ in range(6):
            self.office.add_occupant(Fellow("Dom Bett"))
        self.assertFalse(self.office.has_space())

    def test_doesnt_add_past_maximum_capacity(self):

        for _ in range(6):
            self.office.add_occupant(Fellow("Dominic"))
        add_extra = self.office.add_occupant(Fellow("Darren"))
        self.assertEqual(add_extra, "This room is full, try another")


class DatabaseTestCase(unittest.TestCase):

    """Tests database functionality: save_state and load_state"""

    def setUp(self):
        self.dojo = Dojo()
        self.other_dojo = Dojo()
        self.other_dojo.create_room("office", ["White"])
        self.other_dojo.create_room("living_space", ["Red"])
        for _ in range(7):
            self.other_dojo.add_person("Dominic Bett", "fellow", "Y")
        self.other_dojo.save_state("tests.db")

    def tearDown(self):
        if os.path.exists("tests.db"):
            os.remove("tests.db")

    def test_save_state_creates_db(self):
        success = self.other_dojo.save_state("tests.db")
        self.assertEqual(success, "Success")
        self.assertTrue(os.path.exists("tests.db"))

    def test_load_state_unallocated(self):
        self.dojo.load_state("tests.db")
        unallocated = [len(self.dojo.office_unallocated),
                       len(self.dojo.living_unallocated)]
        self.assertListEqual(unallocated, [2, 4])

    def test_load_state_room_occupants(self):
        self.dojo.load_state("tests.db")
        occupants = self.dojo.offices[0].occupants
        self.assertEqual(occupants[0].name, "Dominic Bett")
        self.assertTrue(len(self.dojo.offices[0].occupants) == 6)
        self.assertTrue(len(self.dojo.living_spaces[0].occupants) == 4)

    def test_return_message_if_database_doesnt_exist(self):
        database = "nonexistent.db"
        if os.path.exists(database):
            os.path.remove(database)
        wrong_retrieval = self.dojo.load_state(database)
        self.assertEqual("No database", wrong_retrieval)

    @mock.patch('builtins.input', side_effect=['database'])
    def test_database_overwrites_room(self, sys_input):
        self.dojo.create_room("office", ["White"])
        self.dojo.load_state("tests.db")
        people = self.dojo.offices[0].occupants
        self.assertEqual(len(people), 6)

    @mock.patch('builtins.input', side_effect=['system'])
    def test_system_keeps_system_files(self, sys_input):
        self.dojo.create_room("office", ["White"])
        self.dojo.load_state("tests.db")
        people = self.dojo.offices[0].occupants
        self.assertEqual(len(people), 0)


class DeleteTestCase(unittest.TestCase):

    """Tests the delete person or room functionality"""

    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", ["Blue"])
        self.dojo.create_room("living_space", ["White"])
        self.dojo.add_person("Dominic", "fellow", "Y")
        self.dojo.add_person("Dan", "fellow", "Y")
        self.dojo.add_person("Darren", "staff")
        self.dojo.create_room("office", ["Yellow"])

    def test_person_is_deleted(self):
        person = self.dojo.offices[0].occupants[0]
        self.dojo.delete_object("person", person.id_key)
        self.assertEqual(len(self.dojo.offices[0].occupants), 2)

    def test_room_is_deleted(self):
        self.dojo.delete_object("room", "Yellow")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(self.dojo.offices[0].name, "Blue")

    def test_person_identifier_is_integer(self):
        wrong_delete = self.dojo.delete_object("person", "Whodiss..!!")
        self.assertEqual(wrong_delete, "Not integer")

    def test_only_person_from_specified_room_is_deleted(self):
        people = self.dojo.offices[0].occupants
        self.dojo.delete_object("person", people[0].id_key, "office")
        self.assertEqual(len(self.dojo.offices[0].occupants), 2)
        self.assertEqual(
            len(self.dojo.living_spaces[0].occupants), 2)

    def test_returns_error_if_object_doesnt_exist(self):
        wrong_delete = self.dojo.delete_object("elChapo", "Nothing")
        self.assertEqual(wrong_delete, "Wrong object")

    def test_person_in_multiple_rooms_deleted_if_option_specified(self):
        person = self.dojo.offices[0].occupants[0]
        self.dojo.delete_object("person", person.id_key, "all")
        living_occupants = self.dojo.living_spaces[0].occupants
        office_occupants = self.dojo.offices[0].occupants
        self.assertEqual(len(living_occupants), 1)
        self.assertEqual(len(office_occupants), 2)


if __name__ == "__main__":
    unittest.main()
