teimport unittest

from dojo import Dojo
from rooms import Room, Office, LivingSpace
from people import Person, Staff, Fellow

class AllocationsTestCase(unittest.TestCase):

    def setUp(self):

        self.dojo_object = Dojo()
        self.commuter = Fellow("Dominic Bett", "N")

    def tearDown(self):
        pass

    #tests if occupants in rooms are equal to what was input

    def test_if_right_number_of_occupants_is_output(self):

        self.dojo_object.create_room("office", ["Blue"])
        test_room = self.dojo_object.office_array[0]
        test_room.add_occupant(Fellow("Dominic Bett", "N"))
        test_room.add_occupant(Fellow("Jamie Heineman"))
        test_room.add_occupant(Staff("Grant Imahara"))
        names_list = [occupant.name for occupant in test_room.room_occupants]

        self.assertListEqual(names_list, ["Dominic Bett", "Jamie Heineman",
        "Grant Imahara"])
    
    #test print_allocations returns no allocations if they
    #dont exist

    def test_allocations_are_printed_appropriately(self):

        print_string = self.dojo_object.print_allocations(self, None)
        string = "\nAllocations: \n"
        string += "\tOffices\n"
        string += "\t---------\n"
        string += "\n\tLiving Spaces\n"
        string += "\t----------------\n"
        string += "\n"
        self.assertEqual(string, print_string)

    #test print_room functionality doesnt return anything if there were no
    #rooms with the same name.
    
    def test_finds_no_room_if_no_room_with_name_exists(self):

        print_room = self.dojo_object.print_room("White")
        self.assertEqual(print_room, "No such room exists")

