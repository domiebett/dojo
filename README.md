[![Build Status](https://travis-ci.org/DomieBett/Week_Two_Andela_Project_Dojo.svg?branch=develop)](https://travis-ci.org/DomieBett/Week_Two_Andela_Project_Dojo) [![Coverage Status](https://coveralls.io/repos/github/DomieBett/Week_Two_Andela_Project_Dojo/badge.svg?branch=master)](https://coveralls.io/github/DomieBett/Week_Two_Andela_Project_Dojo?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6eb22d0872f74963a28d4b35ac9f0677)](https://www.codacy.com/app/dbett49/Week_Two_Andela_Project_Dojo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DomieBett/Week_Two_Andela_Project_Dojo&amp;utm_campaign=Badge_Grade)
# Week_Two_Andela_Project_Dojo

## Final project for week two bootcamp

This repository contains files for the final Andela Bootcamp Cohort 18 Project, Creating an office or living space room allocation sofware for joining Andela Fellows or Andela Staff Members.


## Starting Up on system

I assume you already have git, python and pip package installer installed. Install virtualenv:

>pip install virtualenv

Make a project directory and navigate to it:

>mkdir ~/Projects

>cd ~/Projects

Clone repository:

>git clone https://github.com/DomieBett/Week_Two_Andela_Project_Dojo.git

Navigate into project directory:

>cd Week_Two_Andela_Project_Dojo

Set up a virtual environment:

>virtualenv --python=python3 env

Activate virtual environment:

>source env/bin/activate

Install requirements:

>pip install -r requirements.txt

To run the program in interactive mode, enter:

>python main.py -i


## Usage:

```
> main.py>> create_room <roomtype> <name>...
> main.py>> add_person <first_name> <last_name> <person_role> [<want_accommodation>]
> main.py>> find_userid <first_name> <last_name>
> main.py>> print_allocations [<filename>]
> main.py>> print_unallocated [<file_name>]
> main.py>> print_room <room_name>
> main.py>> reallocate_person <person_ID> <room_name>
> main.py>> load_people <file_name>
> main.py>> save_state [--db=<database>]
> main.py>> load_state [<database>]
> main.py>> delete <object_to_delete> <object_identifier> [<selector>]
> main.py>> quit
> main.py>> (-i | --interactive)
> main.py>> (-h | --help)
```

## Options:

```
> add_person          : Adds people to rooms or to unallocated if no rooms exists.
> create_room         : Creates room and automatically adds unallocated people to it.
> print_allocations   : Prints rooms and all people in them. Also prints people id(s)
> print_unallocated   : Print unallocated people with their id.
> print_room          : Prints the occupants in a specific room.
> reallocate_person   : Moves person with the person_id to the room specified.
> load_people         : Loads people from a text file.
> save_state          : Saves data in system to database.
> load_state          : Retrieves rooms and people from database.
> delete              : Delete room or person from system. 
> quit                : Exit applications. 
```

The repo has:

1. main.py	-Contains functions parsing the docopt command line arguments and calling respective function

Modules folder with the following modules:

1. dojo.py	-Contains Dojo class with lists for rooms and functions for all app features.
2. rooms.py -Contains Room object holding with list containing its occupants (Person objects)
3. people.py -Contains Person object used as a template for Fellows and Staff.
4. database.py - Contains class models for purpose of saving to database.

Tools folder with the following modules:

1. tools.py -Contains simple functions that are regularly used by the program. 


## Test Files

tests folder with the following modules:

 1. test_cases.py - Contains test cases for all functionality and objects


### It also contains this README.md file.

## Author:

Dominic Kipchumba Bett.