"""
Usage:
main.py>> create_room <roomtype> <name>...                                                           
main.py>> add_person <first_name> <last_name> <person_role> [--accommodate=N]   
main.py>> find_userid <first_name> <last_name>                                                       
main.py>> reallocate_person <person_ID> <room_name>                                               
main.py>> load_people <filename>
main.py>> print_allocations [--o=file_name]
main.py>> print_unallocated [--o=file_name]
main.py>> print_room <room_name>
main.py>> save_state [--db=<sqlite_database>]
main.py>> load_state [--db=<sqlite_database>]
main.py>> quit
main.py>> (-i | --interactive)
main.py>> (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from colorama import init
init(strip=not sys.stdout.isatty())
from docopt import docopt, DocoptExit
from dojo import Dojo
# from db_conn import DbManager
from termcolor import cprint
from pyfiglet import figlet_format


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

            print('Invalid Command!')
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
    cprint(figlet_format(header, font="starwars"), "green")
    intro = """
      THE SPACE ALLOCATOR OF YOUR DREAMS   """
    cprint(figlet_format(intro, font='digital'), "white")

    prompt = 'Dojo>> '
    file = None
    dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, arg):

        """Usage: create_room <room_type> <room_name>..."""
        print(self.dojo.create_room(arg['<room_type>'], arg['<room_name>']))

    @docopt_cmd
    def do_add_person(self, arg):

        """Usage: add_person <first_name> <last_name> <person_role> [--a=<want_accomodation>]"""
        person_name = arg['<first_name>'] + ' ' + arg['<last_name>']
        if arg['--a'] == None:
            want_accomodation = 'n'
        else:
            want_accomodation = str(arg['--a'])
        person_role = arg['<person_role>']
        print(self.dojo.add_person(person_name, person_role, want_accomodation))

    @docopt_cmd
    def do_find_userid(self, arg):

        """Usage: find_userid <first_name> <last_name>"""
        # person_name = arg['<first_name>'] + ' ' + arg['<last_name>']
        # print(self.dojo.find_userid(person_name))
        pass

    @docopt_cmd
    def do_reallocate_person(self, arg):

        """Usage: reallocate_person <person_ID> <room_name>"""
        # print(self.dojo.reallocate_person(
        #     int(arg['<person_ID>']), arg['<room_name>']))
        pass

    @docopt_cmd
    def do_load_people(self, arg):

        """Usage: load_people <filename>"""
        # self.dojo.load_people(arg['<filename>'])
        pass

    @docopt_cmd
    def do_print_allocations(self, args):

        '''Usage: print_allocations [--o=filename]'''
        # print(self.dojo.print_allocations(args))
        pass

    @docopt_cmd
    def do_print_unallocated(self, args):

        """Usage: print_unallocated [--o=filename]"""
        # print(self.dojo.print_unallocated(args))
        pass

    @docopt_cmd
    def do_print_room(self, arg):

        """Usage: print_room <room_name>"""
        # print(self.dojo.print_room(arg['<room_name>']))
        pass

    @docopt_cmd
    def do_save_state(self, args):

        """Usage: save_state [--db=<sqlite_database>]"""
        # print(args)
        # self.dojo.save_state(args)
        pass

    @docopt_cmd
    def do_load_state(self, args):

        """Usage: load_state [--db=<sqlite_database>]"""
        # self.dojo.load_state(args)
        pass

    def do_quit(self, arg):

        """Usage: quit"""
        print('System closed.')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        FrontDojo().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")
