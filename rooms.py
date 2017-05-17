from people import Staff


class Room(object):

    global maximum_people
    maximum_people = 0
    global room_occupants
    room_occupants = []

    def __init__(self, room_type, name):

        self.room_type = room_type
        self.name = name
        self.maximum_people = maximum_people
        self.room_occupants = room_occupants

    # Function is imported by Living Space class and Office class
    # to determine if the class has been occupied to the maximum
    # capacity.

    def has_space(self):

        if (len(self.room_occupants) < self.maximum_people):
            return True
        return False

    # Adds occupants to the rooms. Checks if occupant is Staff and
    # denies them access to LivingSpace

    def add_occupant(self, person):

        if not self.has_space():
            return "This room is full, try another"
        elif (isinstance(self, LivingSpace)):
            if (isinstance(person, Staff)):
                return "Staff not allowed in Living Space"
            else:
                self.room_occupants.append(person)
        else:
            self.room_occupants.append(person)


class LivingSpace(Room):

    #Initialises variables, which represent maximum capacity
    #of the living space and current number of occupants in the living space.

    def __init__(self, name):

        self.name = name
        self.room_type = "living_space"
        self.maximum_people = 4
        self.room_occupants = []


class Office(Room):

    #Initialises variables, which represent maximum capacity
    #of the living space and current number of occupants in the living space.

    def __init__(self, name):

        self.name = name
        self.room_type = "office"
        self.maximum_people = 6
        self.room_occupants = []
