#!/usr/bin/env python2.6
import os
import find_kipy
from kipy.project import Project
from kipy.parsesch import ParseSchematic

ParseSchematic(Project(os.path.abspath('.')))

#project.libdict.check_duplicates()
