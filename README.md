# Week_Two_Andela_Project_Dojo

Final project for week two bootcamp

This repository contains files for the final Andela Bootcamp Cohort 18 Project, Creating an office or living space room allocation sofware for joining Andela Fellows or Andela Staff Members. It contains:

dojo.py	-Contains Dojo class with lists for rooms and functions for accessing database.
rooms.py -Contains Room object holding with list containing its occupants (Person objects)
people.py -Contains Person object used as a template for Fellows and Staff.
office.py	-Contains Office object which used to create office rooms. Imports the Room object.
livingspace.py	-Contains LivingSpace object which creates Living spaces for Fellow(s).
fellow.py	-Contains Fellow object representing Andela Fellows joining. 
staff.py	-Contains Staff object representing Staff joining Andela.
main.py	-Contains functions parsing the docopt command line arguments and calling respective functions.

TestFiles
------------

test_create_add.py	-Contains test cases for the create_room and add_person task 0.

It also contains this README.md file.
