import unittest
from modules.rooms import Room, Office, LivingSpace
from modules.dojo import Dojo
from modules.people import Person, Fellow, Staff


class CreateRoomTestCase(unittest.TestCase):
    """Tests for the create_room and add_person functionality"""

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

        for i in range(4):
            self.office_room.add_occupant(self.commuter)

        occupants = len(self.office_room.room_occupants)
        self.assertEqual(occupants, 4)

    def test_doesnt_add_past_maximum_capacity(self):

        for i in range(7):
            self.office_room.add_occupant(self.commuter)

        add_extra = self.office_room.add_occupant(self.commuter)
        self.assertEqual(add_extra, "This room is full, try another")

    def test_rooms_are_added_into_correct_array_in_dojo(self):

        self.office_array = self.dojo_object.office_array
        living_array = self.dojo_object.living_space_array
        self.dojo_object.add_room(self.office_room)
        self.dojo_object.add_room(self.living_space_room)
        self.assertIsInstance(self.office_array[0], Office)
        self.assertIsInstance(living_array[0], LivingSpace)

    def test_office_and_livingspace_is_an_instance_of_room(self):

        self.assertIsInstance(self.office_room, Room)
        self.assertIsInstance(self.living_space_room, Room)


class AddPersonTestCase(unittest.TestCase):
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
        illegal_person = self.dojo_object.add_person("Dominic Bett", "boogey_man", "Y")
        self.assertEqual(illegal_person, "Not allowed")

    def test_function_doesnt_allow_attempt_to_give_staff_living_space(self):
        illegal_accommodation = self.dojo_object.add_person("Patrick Sacho", "staff", "Y")
        self.assertEqual(illegal_accommodation, "Wrong allocation")

    def test_only_Y_and_N_accommodation_options_allowed(self):
        illegal_accommodation = self.dojo_object.add_person("Patrick Sacho", "fellow", "P")
        self.assertEqual(illegal_accommodation, "Wrong input")


class AllocationsTestCase(unittest.TestCase):
    def setUp(self):
        self.dojo_object = Dojo()
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
        self.assertEqual(print_room, "No room exists")

class ReallocateTestCase(unittest.TestCase):

    def setUp(self):
        self.dojo_object = Dojo()
        self.dojo_object.create_room("office", ["Blue"])
        self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        self.dojo_object.add_person("Darren Kasengo", "fellow", "Y")
        self.dojo_object.create_room("office", ["White"])

    def test_if_reallocate_moves_the_person(self):
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
        wrong_reallocation = self.dojo_object.reallocate_person(int(id(occupant1)), "Yellow")
        self.assertEqual(wrong_reallocation, "Cannot add to room")

    def test_only_existing_rooms_are_reallocated(self):
        wrong_reallocation = self.dojo_object.reallocate_person(50484848111, "Yellow")
        self.assertEqual(wrong_reallocation, "Room doesnt exist")

    def test_only_existing_persons_are_reallocated(self):
        wrong_reallocation = self.dojo_object.reallocate_person(5048488882, "White")
        self.assertEqual(wrong_reallocation, "Person doesnt exist")

    def test_person_is_not_moved_if_there_destination_is_full(self):
        for i in range(12):
            self.dojo_object.add_person("Dominic Bett", "fellow", "N")
        person_id = self.dojo_object.office_array[0].room_occupants[0].id_key
        wrong_reallocation = self.dojo_object.reallocate_person(person_id, "White")
        self.assertEqual(wrong_reallocation, "Destination is full")


class Load_People_Test_Case(unittest.TestCase):

    def setUp(self):
        self.dojo_object = Dojo()

    def test_correct_number_of_people_are_added_to_room(self):
        self.dojo_object.create_room("office", ["Blue"])
        self.dojo_object.load_people("input")
        occupants = self.dojo_object.office_array[0].room_occupants
        self.assertEqual(len(occupants), 5)

    def test_returns_message_if_txt_file_doesnt_exist(self):
        no_file = self.dojo_object.load_people("no_file")
        self.assertEqual(no_file, "File not found")