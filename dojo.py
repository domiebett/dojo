from rooms import Room, Office, LivingSpace


class Dojo():

    """Creates two global variables, office_array and 
    living_space_array which are lists that hold data 
    for rooms that are Offices and Living Spaces 
    respectively.
    """

    #initialises the class

    def __init__(self):
        self.office_array = []
        self.living_space_array = []

    # Adds rooms created in the main module into their
    # respective arrays above.

    def add_room(self, room):
        if isinstance(room, Office):
            self.office_array.append(room)

        elif isinstance(room, LivingSpace):
            self.living_space_array.append(room)
    
    # Creates a room either office or living space that is then
    # added to the respective lists in Dojo class


    def create_room(self, room_type, room_names):

        # The two below if statements creates an Office or LivingSpace
        # object, same number of times equal to the number of arguments
        # passed for room names in command line

        if room_type == "office":

            for room_name in room_names:
                new_room = Office(room_name)
                self.add_room(new_room)

        if room_type == "living_space":

            for room_name in room_names:
                new_room = LivingSpace(room_name)
                self.add_room(new_room)

        self.get_rooms(room_type)

    # Used to fetch data from the room arrays above.

    def get_rooms(self, room_type):
        if room_type == "office":
            array = self.office_array
        elif room_type == "living_space":
            array = self.living_space_array
        for room in array:
            print ("Created a " + room.room_type + " named " + room.name)
