#!/usr/bin/env python2.6
'''
    Check the schematic of the project in the current directory.

    (cd to the project directory before executing)
'''
import os
import find_kipy
from kipy.project import Project
from kipy.parsesch import ParseSchematic

ParseSchematic(Project(os.path.abspath('.')))

#project.libdict.check_duplicates()
