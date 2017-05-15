#!/usr/bin/env python

doc = """
usage: main.py
    main.py create_room <room_type> <room_name>...
    main.py add_person <person_name> (--fellow | --staff) [--accommodate=<N>]
    main.py -h | --h
    main.py --version
options:
    room_type           type of room
    room_name           name of Room
    person_name         name aof person
    accommodate         y or no
    --fellow            fellow is a fellow
    --staff             i wonder even why we have a staff option
    -h --help           display the full help options
    -v --version        display the app's running version
"""

from docopt import docopt
from pprint import pprint

from people import Person, Fellow, Staff
from dojo import Dojo
from rooms import Room, Office, LivingSpace


# main function that calls respective functions depending on argument
# passed on command line

def main(docopt_args):

    if docopt_args['create_room']:

        room_type = docopt_args['<room_type>']
        room_names = docopt_args['<room_name>']
        Dojo().create_room(room_type, room_names)

    if (docopt_args['add_person']):
        person_name = docopt_args['<person_name>']
        person_role = ""

        if docopt_args['--fellow']:
            person_role = "fellow"
        elif docopt_args['--staff']:
            person_role = "staff"
        
        wants_accomodation = docopt_args['--accommodate']
        Dojo().add_person(person_name, person_role, wants_accomodation)


if __name__ == '__main__':
    args = docopt(doc)
    main(args)
