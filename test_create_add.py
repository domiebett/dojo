import unittest

from rooms import Room, Office, LivingSpace
from dojo import Dojo
from people import Person, Fellow, Staff


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

    #test if correct name and type are set in rooms

    def test_if_correct_room_type_and_name_is_saved(self):

        description = [self.office_room.name, self.office_room.room_type]
        self.assertListEqual(description, ["Blue", "office"])

    #test if add_occupant adds occupant to room

    def test_if_adding_occupants_increases(self):

        for i in range(4):
            self.office_room.add_occupant(self.commuter)

        occupants = len(self.office_room.room_occupants)
        self.assertEqual(occupants, 4)

    #test maximum capacity in rooms is not exceeded

    def test_doesnt_add_past_maximum_capacity(self):

        for i in range(7):
            self.office_room.add_occupant(self.commuter)

        add_extra = self.office_room.add_occupant(self.commuter)
        self.assertEqual(add_extra, "This room is full, try another")

    #test if offices are added into office array and living spaces
    #into living_space array

    def test_rooms_are_added_into_correct_array_in_dojo(self):

        self.office_array = self.dojo_object.office_array
        living_array = self.dojo_object.living_space_array
        self.dojo_object.add_room(self.office_room)
        self.dojo_object.add_room(self.living_space_room)
        self.assertTrue(isinstance(self.office_array[0], Office))
        self.assertTrue(isinstance(living_array[0], LivingSpace))
    
    #test if office is an instance of a living space

    def test_office_and_livingspace_is_an_instance_of_room(self):

        self.assertIsInstance(self.office_room, Room)
        self.assertIsInstance(self.living_space_room, Room)
    
    #test if exisiting rooms with same names are not created.

    def test_existing_room_is_not_created(self):
        
        self.dojo_object.create_room("office", ["Black"])
        wrong_room = self.dojo_object.create_room("office", ["Black"])
        self.assertEqual(wrong_room, "Room exists")


class AddPersonTestCase(unittest.TestCase):

    def setUp(self):
        
        self.living_space_room = LivingSpace("Red")
        self.office_room = Office("Blue")
        self.staff_member = Staff("Harry")
        self.dojo_object = Dojo()

    #test no staff is given a living space.

    def test_staff_are_not_given_living_space(self):

        illegal_staff = self.living_space_room.add_occupant(self.staff_member)
        self.assertEqual(illegal_staff, "Staff not allowed in Living Space")
    
    #test people without rooms are added to unallocated array
    
    def test_person_is_added_to_unallocated(self):

        self.dojo_object.add_person("Dominic Bett", "fellow", "Y")
        unallocated = self.dojo_object.office_unallocated
        self.assertEqual(len(unallocated), 1)
        unallocated = self.dojo_object.living_unallocated
        self.assertEqual(len(unallocated), 1)
