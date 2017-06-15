import random

def is_int(s):
    """Checks if an object is an integer"""

    try:
        int(s)
        return True
    except ValueError:
        return False


def get_input(text):
    """Returns input"""

    return input(text)


def random_empty_rooms(array):
    """Generates a random room with space for allocation. Takes either
    office or living_space array as arguments"""

    empty_rooms = []

    for a in array:
        if a.has_space():
            empty_rooms.append(a)

    # returns "Full if all the rooms are full"

    if len(empty_rooms) <= 0:
        return "Full"

    # select a random room.

    random_room = random.choice(empty_rooms)
    return random_room
