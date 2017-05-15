import unittest

from rooms import Room, Office, LivingSpace
from dojo import Dojo
from people import Person, Fellow, Staff


class CreateRoomTestCase(unittest.TestCase):

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

        self.office_room.add_occupant(self.commuter)
        self.office_room.add_occupant(self.commuter)
        self.office_room.add_occupant(self.commuter)
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
        self.assertTrue(isinstance(self.office_array[0], Office))
        self.assertTrue(isinstance(living_array[0], LivingSpace))

    def test_office_and_livingspace_is_an_instance_of_room(self):

        self.assertIsInstance(self.office_room, Room)
        self.assertIsInstance(self.living_space_room, Room)


class AddPersonTestCase(unittest.TestCase):


    def setUp(self):
        self.living_space_room = LivingSpace("Red")
        self.staff_member = Staff("Harry")

    def test_staff_are_not_given_living_space(self):

        illegal_staff = self.living_space_room.add_occupant(self.staff_member)
        self.assertEqual(illegal_staff, "Staff not allowed in Living Space")