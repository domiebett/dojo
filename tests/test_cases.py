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

        self.office_room = Office("Blue")
        self.living_space_room = LivingSpace("Red")
        self.commuter = Fellow("Dominic")
        self.resident = Fellow("Kevin", True)
        self.staff_member = Staff("Harry")
        self.dojo_object = Dojo()

    def tearDown(self):

        self.office_room.room_occupants[:] = []

    def test_if_correct_room_type_and_name_is_saved(self):

        description = [self.office_room.name, self.office_room.room_type]
        self.assertListEqual(description, ["Blue", "office"])

    def test_if_adding_occupants_increases(self):

        for _ in range(4):
            self.office_room.add_occupant(self.commuter)

        occupants = len(self.office_room.room_occupants)
        self.assertEqual(occupants, 4)

    def test_doesnt_add_past_maximum_capacity(self):

        for _ in range(7):
            self.office_room.add_occupant(self.commuter)

        add_extra = self.office_room.add_occupant(self.commuter)
        self.assertEqual(add_extra, "This room is full, try another")

    def test_rooms_are_added_into_correct_array_in_dojo(self):

        office_array = self.dojo_object.office_array
        living_array = self.dojo_object.living_space_array
        self.dojo_object.create_room("office", ["Blue"])
        self.dojo_object.create_room("living_space", ["White"])
        self.assertIsInstance(office_array[0], Office)
        self.assertIsInstance(living_array[0], LivingSpace)

    def test_office_and_livingspace_is_an_instance_of_room(self):

        self.assertIsInstance(self.office_room, Room)
        self.assertIsInstance(self.living_space_room, Room)

    def test_room_type_is_office_or_living_space(self):

        wrong_type = self.dojo_object.create_room("blah", ["White"])
        self.assertEqual(wrong_type, "Wrong room type")


class AddPersonTestCase(unittest.TestCase):

    """Tests for functionalities of the add_person() function in dojo.py"""

    def setUp(self):
        self.living_space_room = LivingSpace("Red")
        self.office_room = Office("Blue")
        self.staff_member = Staff("Harry")
        self.dojo_object = Dojo()

    def test_staff_are_not_given_living_space(self):
        illegal_staff = self.living_space_room.add_occupant(self.staff_member)
        self.assertEqual(illegal_staff, "Staff not allowed in Living Space")

    def test_person_is_added_to_unallocated(self):
        self.dojo_object.add_person("Dominic Bett", "fellow", "Y")
        unallocated = self.dojo_object.office_unallocated
        self.assertEqual(len(unallocated), 1)
        unallocated = self.dojo_object.living_unallocated
        self.assertEqual(len(unallocated), 1)

    def test_only_fellow_and_staff_allowed(self):
        illegal_person = self.dojo_object.add_person(
            "Dominic Bett", "boogey_man", "Y")
        self.assertEqual(illegal_person, "Not allowed")

    def test_function_doesnt_allow_attempt_to_give_staff_living_space(self):
        illegal_accommodation = self.dojo_object.add_person(
            "Patrick Sacho", "staff", "Y")
        self.assertEqual(illegal_accommodation, "Wrong allocation")

    def test_only_Y_and_N_accommodation_options_allowed(self):
        illegal_accommodation = self.dojo_object.add_person(
            "Patrick Sacho", "fellow", "P")
        self.assertEqual(illegal_accommodation, "Wrong input")

    def test_person_is_automatically_added_to_empty_room(self):
        self.dojo_object.add_person("Dominic Bett", "fellow", "Y")
        self.dojo_object.add_person("Darren Kasengo", "staff", "N")
        list_length = len(self.dojo_object.office_unallocated)
        self.assertEqual(list_length, 2)
        list_length = len(self.dojo_object.living_unallocated)
        self.assertEqual(list_length, 1)

    def test_person_is_removed_from_unallocated_if_room_exists(self):
        self.dojo_object.add_person("Dominic Bett", "fellow", "Y")
        self.dojo_object.add_person("Darren Kasengo", "staff", "N")
        self.dojo_object.create_room("office", ["White"])
        office = self.dojo_object.office_array[0]
        office_unallocated = self.dojo_object.office_unallocated
        self.assertEqual(len(office.room_occupants), 2)
        self.assertEqual(len(office_unallocated), 0)

    def test_person_is_assigned_right_room(self):
        self.dojo_object.create_room("office", ["White"])
        self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        office_name = self.dojo_object.office_array[
            0].room_occupants[0].office_name
        self.assertEqual(office_name, "White")


class AllocationsTestCase(unittest.TestCase):

    """Tests for print_room, print_allocations, and print_unallocated
    functions"""

    def setUp(self):
        self.dojo_object = Dojo()
        self.dojo_object.create_room("office", ["Yellow"])
        self.dojo_object.create_room("living_space", ["Red"])
        self.commuter = Fellow("Dominic Bett", "N")

    def test_if_right_number_of_occupants_is_output(self):
        self.dojo_object.create_room("office", ["Blue"])
        test_room = self.dojo_object.office_array[0]
        test_room.add_occupant(Fellow("Dominic Bett", "N"))
        test_room.add_occupant(Fellow("Jamie Heineman"))
        test_room.add_occupant(Staff("Grant Imahara"))
        names_list = [occupant.name for occupant in test_room.room_occupants]

        self.assertListEqual(names_list, ["Dominic Bett", "Jamie Heineman",
                                          "Grant Imahara"])

    def test_finds_no_room_if_no_room_with_name_exists(self):
        print_room = self.dojo_object.print_room("White")
        self.assertEqual(print_room, "Room doesnt exist")

    def test_only_fellow_and_staff_are_allowed_during_auto_allocation(self):
        wrong_allocation = self.dojo_object.append_unallocated_persons(
            "Dominic Bett", "ninja")
        self.assertEqual(wrong_allocation, "No such specification")

    def test_print_empty_room_return_empty_result(self):
        string = "\nAllocation: \n"
        string += "\tRoom Name: Yellow" + \
            " (office).\n"

        string += "\tOccupants: \n\t\t  Name  | Id \n\t\t  -----   ---\n\n"

        func_string = self.dojo_object.print_room("Yellow")
        self.assertEqual(string, func_string)

    def test_automatically_allocated_person_is_assingned_the_right_room(self):
        for _ in range(8):
            self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        self.dojo_object.create_room("office", ["Green"])
        person = self.dojo_object.office_array[1].room_occupants[0]
        self.assertEqual(person.office_name, "Green")

    def test_print_allocations_outputs_to_file(self):
        string = "File saved to output/tests.txt."
        allocation_string = self.dojo_object.print_allocations("tests.txt")
        self.assertEqual(string, allocation_string)

    def test_print_unallocated_outputs_to_file(self):
        string = "File saved to path: 'output/tests.txt'."
        unallocated_string = self.dojo_object.print_unallocated("tests.txt")
        self.assertEqual(string, unallocated_string)


class ReallocateTestCase(unittest.TestCase):

    """Test the reallocated_person() function in dojo.py"""

    def setUp(self):
        self.dojo_object = Dojo()
        self.dojo_object.create_room("office", ["Blue"])
        self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        self.dojo_object.add_person("Darren Kasengo", "fellow", "Y")
        self.dojo_object.create_room("office", ["White"])

    def test_if_reallocate_is_successful(self):
        reallocated_person = self.dojo_object.office_array[0].room_occupants[0]
        person_id = int(id(reallocated_person))
        self.dojo_object.reallocate_person(person_id, "White")
        room_one_occupants = self.dojo_object.office_array[0].room_occupants
        room_two_occupants = self.dojo_object.office_array[1].room_occupants
        occupant_list = [len(room_one_occupants), len(room_two_occupants)]
        self.assertListEqual([1, 1], occupant_list)

    def test_if_right_person_is_reallocated(self):
        occupant1 = self.dojo_object.office_array[0].room_occupants[0]
        self.dojo_object.reallocate_person(int(id(occupant1)), "White")
        occupant2 = self.dojo_object.office_array[1].room_occupants[0]
        self.assertEqual(occupant1.name, occupant2.name)
        self.assertEqual(occupant1.id_key, occupant2.id_key)

    def test_reallocation_is_between_similar_room_types(self):
        self.dojo_object.create_room("living_space", ["Yellow"])
        occupant1 = self.dojo_object.office_array[0].room_occupants[0]
        wrong_reallocation = self.dojo_object.reallocate_person(
            int(id(occupant1)), "Yellow")
        self.assertEqual(wrong_reallocation, "Person doesnt exist")

    def test_reallocation_is_between_existing_rooms(self):
        wrong_reallocation = self.dojo_object.reallocate_person(
            50484848111, "Yellow")
        self.assertEqual(wrong_reallocation, "Room doesnt exist")

    def test_only_existing_persons_are_reallocated(self):
        wrong_reallocation = self.dojo_object.reallocate_person(
            5048488882, "White")
        self.assertEqual(wrong_reallocation, "Person doesnt exist")

    def test_only_integers_are_allowed(self):
        wrong_id = self.dojo_object.reallocate_person("string", "White")
        self.assertEqual(wrong_id, "Not an integer")

    def test_person_is_not_moved_if_there_destination_is_full(self):
        for _ in range(12):
            self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        person_id = self.dojo_object.office_array[0].room_occupants[0].id_key
        wrong_reallocation = self.dojo_object.reallocate_person(
            person_id, "White")
        self.assertEqual(wrong_reallocation, "Destination is full")

    def test_reallocation_is_not_to_same_room(self):
        occupant1 = self.dojo_object.office_array[0].room_occupants[0]
        wrong_reallocation = self.dojo_object.reallocate_person(
            int(id(occupant1)), "Blue")
        self.assertEqual(wrong_reallocation, "Wrong reallocation")

    def test_unallocated_person_is_not_reallocated(self):
        person = Fellow("Dominic Bett")
        self.dojo_object.office_unallocated.append(person)
        unallocated1 = self.dojo_object.office_unallocated[0].id_key
        wrong_reallocation = self.dojo_object.reallocate_person(
            unallocated1, "Blue")
        self.assertEqual(wrong_reallocation, "Person doesnt exist")

    def test_if_right_room_name_is_assigned_to_person(self):
        person = self.dojo_object.office_array[0].room_occupants[0]
        self.dojo_object.reallocate_person(person.id_key, "White")
        person = self.dojo_object.office_array[1].room_occupants[0]
        self.assertEqual(person.office_name, "White")


class LoadPeopleTestCase(unittest.TestCase):

    """Tests the load_people function in dojo.py"""

    def setUp(self):
        self.dojo_object = Dojo()

    def test_correct_number_of_people_are_added_to_room(self):
        self.dojo_object.create_room("office", ["Blue"])
        self.dojo_object.load_people("input.txt")
        occupants = self.dojo_object.office_array[0].room_occupants
        self.assertEqual(len(occupants), 5,
                         msg="People should be added to room correctly")

    def test_returns_message_if_txt_file_doesnt_exist(self):
        no_file = self.dojo_object.load_people("no_file.txt")
        self.assertEqual(no_file, "File not found",
                         msg="File to load from should exist")


class PeopleTestCase(unittest.TestCase):

    """Test the entire Person, Fellow and Staff objects"""

    def setUp(self):
        self.fellow = Fellow("Dominic Bett", "Y")
        self.staff = Staff("Dominic Bett")

    def test_if_gender_is_assigned(self):
        self.fellow.set_gender("Female")
        self.staff.set_gender("Male")
        self.assertEqual(self.fellow.gender, "Female")
        self.assertEqual(self.staff.gender, "Male")

    def test_if_age_is_assingned(self):
        self.fellow.set_age(21)
        self.staff.set_age(20)
        self.assertEqual(self.fellow.age, 21)
        self.assertEqual(self.staff.age, 20)

    def test_error_message_returned_gender_or_age_not_assigned(self):
        self.assertEqual(self.fellow.get_gender(), "Gender not assigned")
        self.assertEqual(self.fellow.get_age(), "Age not assigned")

    def test_age_and_gender_is_returned(self):
        self.fellow.set_gender("Male")
        self.staff.set_age(22)
        gender = self.fellow.get_gender()
        age = self.staff.get_age()
        self.assertEqual(gender, "Male")
        self.assertEqual(age, 22)

    def test_error_message_if_wrong_format_is_set(self):
        wrong_assignment = self.fellow.set_age("Twenty One")
        self.assertEqual(wrong_assignment, "Should be a number")
        wrong_assignment = self.fellow.set_gender(474747)
        self.assertEqual(wrong_assignment, "Should be a string")


class RoomsTestCase(unittest.TestCase):
    """Test all Room, Office, LivingSpace objects"""

    def setUp(self):
        self.office = Office("Office_Name")
        self.living_space = LivingSpace("Living_Name")

    def test_has_space_and_add_occupant_function(self):
        self.assertTrue(self.office.has_space())
        self.assertTrue(self.living_space.has_space())
        for _ in range(6):
            person = Fellow("Dom Bett")
            self.office.add_occupant(person)
            self.living_space.add_occupant(person)
        self.assertFalse(self.office.has_space())
        self.assertFalse(self.living_space.has_space())


class DatabaseTestCase(unittest.TestCase):

    """Tests database functionality: save_state and load_state"""

    def setUp(self):
        self.dojo_for_save = Dojo()
        self.dojo_for_save.create_room("office", ["White", "Blue"])
        self.dojo_for_save.create_room("living_space", ["Red", "Black"])
        for _ in range(10):
            self.dojo_for_save.add_person("Dominic Bett", "fellow", "Y")
            self.dojo_for_save.add_person("Darren Kasengo", "staff")
        self.dojo_for_save.save_state("tests.db")
        self.dojo_object = Dojo()

    def tearDown(self):
        if os.path.exists("tests.db"):
            os.remove("tests.db")

    def test_if_save_state_is_successful(self):
        success = self.dojo_for_save.save_state("tests.db")
        self.assertEqual(success, "Success")
        self.assertTrue(os.path.exists("tests.db"))

    def test_unallocated_persons_are_retrieved_successfully(self):
        self.dojo_object.load_state("tests.db")
        office_unallocated_len = len(self.dojo_object.office_unallocated)
        living_unallocated_len = len(self.dojo_object.living_unallocated)
        quantity_array = [office_unallocated_len, living_unallocated_len]
        self.assertListEqual(quantity_array, [8, 2])

    def test_room_occupants_are_retrieved_successfully(self):
        self.dojo_object.load_state("tests.db")
        self.assertFalse(self.dojo_object.office_array[0].has_space())
        self.assertFalse(self.dojo_object.office_array[1].has_space())
        self.assertFalse(self.dojo_object.living_space_array[0].has_space())
        self.assertFalse(self.dojo_object.living_space_array[1].has_space())

    def test_return_message_if_database_doesnt_exist(self):
        database = "nonexistent.db"
        if os.path.exists(database):
            os.path.remove(database)
        wrong_retrieval = self.dojo_object.load_state(database)
        self.assertEqual("No database", wrong_retrieval)

    @mock.patch('builtins.input', side_effect=['database'])
    def test_database_overwrites_room(self, sys_input):
        self.dojo_object.create_room("office", ["White"])
        self.dojo_object.load_state("tests.db")
        people = self.dojo_object.office_array[0].room_occupants
        self.assertEqual(len(people), 6)

    @mock.patch('builtins.input', side_effect=['system'])
    def test_system_keeps_system_files(self, sys_input):
        self.dojo_object.create_room("office", ["White"])
        self.dojo_object.load_state("tests.db")
        people = self.dojo_object.office_array[0].room_occupants
        self.assertEqual(len(people), 0)


class DeleteTestCase(unittest.TestCase):

    """Tests the delete person or room functionality"""

    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", ["Blue"])
        self.dojo.create_room("living_space", ["White"])
        self.dojo.add_person("Dominic Bett", "fellow", "Y")
        self.dojo.add_person("Dan Katana", "fellow", "Y")
        self.dojo.add_person("Darren Kasengo", "staff")
        self.dojo.create_room("office", ["Yellow"])

    def test_if_person_is_deleted(self):
        person = self.dojo.office_array[0].room_occupants[0]
        self.dojo.delete_object("person", person.id_key)
        self.assertEqual(len(self.dojo.office_array[0].room_occupants), 2)

    def test_if_room_is_deleted(self):
        self.dojo.delete_object("room", "Yellow")
        self.assertEqual(len(self.dojo.office_array), 1)

    def test_if_person_identifier_is_not_integer(self):
        wrong_delete = self.dojo.delete_object("person", "Whodiss..!!")
        self.assertEqual(wrong_delete, "Not integer")

    def test_only_person_from_one_room_is_deleted(self):
        people = self.dojo.office_array[0].room_occupants
        self.dojo.delete_object("person", people[0].id_key, "office")
        self.assertEqual(len(self.dojo.office_array[0].room_occupants), 2)
        self.assertEqual(
            len(self.dojo.living_space_array[0].room_occupants), 2)

    def test_returns_error_if_object_doesnt_exist(self):
        wrong_delete = self.dojo.delete_object("elChapo", "Nothing")
        self.assertEqual(wrong_delete, "Wrong object")

    def test_person_in_multiple_rooms_deleted_if_option_specified(self):
        person = self.dojo.office_array[0].room_occupants[0]
        self.dojo.delete_object("person", person.id_key, "all")
        living_occupants = self.dojo.living_space_array[0].room_occupants
        office_occupants = self.dojo.office_array[0].room_occupants
        self.assertEqual(len(living_occupants), 1)
        self.assertEqual(len(office_occupants), 2)


if __name__ == "__main__":
    unittest.main()
