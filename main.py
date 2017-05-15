#!/usr/bin/env python

"""main.py
    Usage:
        main.py create_room <room_type> [<room_name>]...
        main.py add_person <person_name> (--fellow | --staff) [--accommodate=<N>]
    Options:

"""

from docopt import docopt
from pprint import pprint

from people import Person, Fellow, Staff
from dojo import Dojo
from rooms import Room, Office, LivingSpace

# Function creates a person object by instantiating the person role
# class, i.e Fellow or Staff

def add_person(person_name, person_role, wants_accomodation):
    pass

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
        
        wants_accomodation = docopt['--accomodate']
        add_person(person_name, person_role, wants_accomodation)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
