[![Build Status](https://travis-ci.org/DomieBett/Week_Two_Andela_Project_Dojo.svg?branch=develop)](https://travis-ci.org/DomieBett/Week_Two_Andela_Project_Dojo) [![Coverage Status](https://coveralls.io/repos/github/DomieBett/Week_Two_Andela_Project_Dojo/badge.svg?branch=master)](https://coveralls.io/github/DomieBett/Week_Two_Andela_Project_Dojo?branch=master)
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


The repo has:

1. main.py	-Contains functions parsing the docopt command line arguments and calling respective function

modules folder with the following modules:

1. dojo.py	-Contains Dojo class with lists for rooms and functions for accessing database.
2. rooms.py -Contains Room object holding with list containing its occupants (Person objects)
3. people.py -Contains Person object used as a template for Fellows and Staff.
4. database.py - Contains class models for purpose of saving to database.

tools folder with the following modules:

1. tools.py -Contains simple functions that are regularly used in systems. 


## Test Files

tests folder with the following modules:

 1. test_cases.py - Contains test cases for all functionality and objects


### It also contains this README.md file.

To run the program in interactive mode, enter:

>python main.py -i

Enter either of the following for the corresponding functionality;


# Functionality
1. create_room >> Creates a room, either Office or Living Space and appends the room to an array in Dojo class in dojo.py
2. add_person >> Adds person either Fellow or Staff and gives them an office. Adds them to specific rooms depending on their requirements.
3. print_room >> prints occupants of the room whose name is given as arguments in function.
4. print_allocations >> outputs to text file if filename option is given, else prints all allocations to the console.
5. print_unallocated >> output to text file if filename option is given, else prints all unallocated person to the console.
6. reallocate_person >> moves person with specified id to specified room
7. load_people >> Loads people from a txt file with the specified name. Txt files are found in the 'input' folder
8. save_state >> Saves data to a database of a given name or to default.db if no name has been given.
9. load_state >> Loads data from the database using the SQLAlchemy library.
10. delete >> Delete either room or person with identifier passed

Check Usage docs in main.py for a full understanding of the arguments to be passed.
