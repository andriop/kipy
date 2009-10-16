#!/usr/bin/env python2.6
'''
    Check the schematics of all the KiCAD demo projects
'''
import os
import glob
import traceback
import find_kipy
from kipy.fileobjs.paths import kicad_demo_root
from kipy.project import Project
from kipy.parsesch import ParseSchematic

for projdir in sorted(glob.glob(os.path.join(kicad_demo_root, '*'))):
    print '\n%s\n\nReading project %s\n' % (60*'=', projdir)
    proj = Project(projdir)
    if proj.topschfname:
        try:
            ParseSchematic(proj)
        except Exception:
            print traceback.format_exc()
