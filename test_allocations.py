import unittest

from dojo import Dojo
from rooms import Room, Office, LivingSpace
from people import Person, Staff, Fellow

class AllocationsTestCase(unittest.TestCase):

    def setUp(self):

        self.dojo_object = Dojo()
        self.commuter = Fellow("Dominic Bett", "N")

    def tearDown(self):
        pass

    def test_if_right_number_of_occupants_is_output(self):

        self.dojo_object.create_room("office", ["Blue"])
        test_room = self.dojo_object.office_array[0]
        test_room.add_occupant(Fellow("Dominic Bett", "N"))
        test_room.add_occupant(Fellow("Jamie Heineman"))
        test_room.add_occupant(Staff("Grant Imahara"))
        names_list = [occupant.name for occupant in test_room.room_occupants]

        self.assertListEqual(names_list, ["Dominic Bett", "Jamie Heineman",
        "Grant Imahara"])