import random
from termcolor import cprint


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


def occupant_string(room):
    """Concatenates strings with information of occupants in a room"""

    string = "\tOccupants: \n"
    count = 1

    data = [[" ", "Name", "|", "Id"], [" ", "-----", "", "---"]]

    # Arranges occupant information into a list which is then appended
    # to the 'data' list to be used to display data to console.

    for occupant in room.occupants:
        data.append([(str(count) + ". "), occupant.name,
                     "|", str(occupant.id_key)])
        count += 1

    col_width = [max(map(len, col))
                 for col in zip(*data)]  # Spaces between columns

    # Takes each list from the data list above and arranges it as
    # rows, with columns spaced with the maximum column width plus
    # col_width

    for row in data:
        string += "\t\t" + (" ".join((val.ljust(width)
                                      for val, width
                                      in zip(row, col_width))) + "\n")

    return string


def assign_unallocated(unallocated_array, room_array):
    """Automatically allocates unallocated people to rooms if one exists"""

    while len(unallocated_array) > 0:
        empty_room = random_empty_rooms(room_array)

        if empty_room == "Full":
            break
        else:
            person = unallocated_array[0]
            if empty_room.type == "office":
                person.office_name = empty_room.name
            elif empty_room.type == "living_space":
                person.living_space_name = empty_room.name
            empty_room.add_occupant(person)
            unallocated_array.remove(person)
            cprint("\t" + person.name +
                   " has been added to Office " + empty_room.name, "green")


def add_to_room(person, room_name, array):
    """Finds room with name that matches argument 'room_name' and adds
    person to it"""

    for room in array:
        if room_name == room.name:

            room.add_occupant(person)
            cprint("\n     Added " + person.name + " to " + room_name,
                   "green")
            return "Success"


def delete_from_room(array, identifier):
    """Used to delete people from specific rooms"""

    for room in array:
        for occupant in room.occupants:
            if occupant.id_key == int(identifier):
                room.occupants.remove(occupant)
                cprint("Occupant " + occupant.name +
                       " has been deleted from " + room.type + " " +
                       room.name, "green")


def delete_from_unallocated(array, identifier):
    """Used to delete unallocated people"""

    for person in array:
        if person.id_key == int(identifier):
            array.remove(person)
            cprint("Removed " + person.name + " from waiting list",
                   "green")
