"""
Usage:
main.py>> create_room <roomtype> <name>...
main.py>> add_person <first_name> <last_name> <person_role> [<want_accommodation>]
main.py>> print_allocations [<filename>]
main.py>> print_unallocated [<file_name>]
main.py>> print_room <room_name>
main.py>> reallocate_person <person_ID> <room_name>
main.py>> load_people <file_name>
main.py>> save_state [--db=<database>]
main.py>> load_state [<database>]
main.py>> delete <object_to_delete> <object_identifier> [<selector>]
main.py>> quit
main.py>> (-i | --interactive)
main.py>> (-h | --help)
Options:
    add_person          : Adds people to rooms or to unallocated if no rooms exists.
    create_room         : Creates room and automatically adds unallocated people to it.
    print_allocations   : Prints rooms and all people in them. Also prints people id(s)
    print_unallocated   : Print unallocated people with their id.
    print_room          : Prints the occupants in a specific room.
    reallocate_person   : Moves person with the person_id to the room specified.
    load_people         : Loads people from a text file.
    save_state          : Saves data in system to database.
    load_state          : Retrieves rooms and people from database.
    delete              : Delete room or person from system.
    quit                : Exit applications.

    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""


import sys
import cmd

from docopt import docopt, DocoptExit
from termcolor import cprint
from pyfiglet import figlet_format
from colorama import init
init(strip=not sys.stdout.isatty())

from modules.dojo import Dojo


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):

        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('You entered the wrong command. Please review Usage')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class FrontDojo(cmd.Cmd):

    header = "  D O J O  "
    cprint(figlet_format(header, font="roman"), "green")
    intro = """
      ANDELA. BECOME OVERCOME PROSPER   """
    cprint(figlet_format(intro, font='digital'), "white")

    prompt = 'Dojo>> '
    file = None
    dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""
        self.dojo.create_room(arg['<room_type>'].lower(), arg['<room_name>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_role> [<wants_accommodation>]"""
        person_name = arg['<first_name>'] + ' ' + arg['<last_name>']
        if arg['<wants_accommodation>'] is None:
            want_accommodation = 'N'
        else:
            want_accommodation = str(arg['<wants_accommodation>'])
        person_role = arg['<person_role>'].lower()
        self.dojo.add_person(person_name, person_role, want_accommodation)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_ID> <room_name>"""
        person_id = arg['<person_ID>']
        room_name = arg['<room_name>']
        self.dojo.reallocate_person(person_id, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <filename>"""
        file_name = arg['<filename>']
        self.dojo.load_people(file_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        '''Usage: print_allocations [<filename>]'''
        if args['<filename>'] is None:
            output = None
        else:
            output = str(args['<filename>'])

        print(self.dojo.print_allocations(output))

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [<filename>]"""
        if args['<filename>'] is None:
            output = None
        else:
            output = str(args['<filename>'])
        print(self.dojo.print_unallocated(output))

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        print(self.dojo.print_room(arg['<room_name>']))

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=<database>]"""
        if args['--db'] is None:
            database = None
        else:
            database = str(args['--db'])

        self.dojo.save_state(database)

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [<database>]"""
        if args['<database>'] is None:
            database = None
        else:
            database = str(args['<database>'])

        self.dojo.load_state(database)

    @docopt_cmd
    def do_delete(self, arg):
        """Usage: delete <object> <identifier> [<selector>]"""

        obj = arg['<object>']
        identifier = arg['<identifier>']
        if arg['<selector>'] is None:
            selector = "all"
        else:
            selector = arg['<selector>']

        self.dojo.delete_object(obj, identifier, selector)

    def do_quit(self, arg):
        """Usage: quit"""
        print('\n   System closed. Good Bye...!!!\n')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        FrontDojo().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")
