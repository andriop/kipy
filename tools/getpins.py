#!/usr/bin/env python2.6

'''
    Usage:  From inside a KiCAD project directory, use getpins with
            a component reference designator as the sole parameter:

              xxxxx/kipy/tools/getpins.py U13

     getpins will dump pin information to stdout.
'''

import os
import sys
import find_kipy
import kipy.project, kipy.parsesch

proj = kipy.project.Project(os.path.abspath('.'))
sch = kipy.parsesch.ParseSchematic(proj)

refdes, = sys.argv[1:]
refdes = refdes.upper()

pinlist = []
for net in sch.netinfo:
    for pin in net.pins:
        if pin.component.refdes.upper() != refdes:
            continue
        name = ', '.join(net.names).lower()
        if not name:
            others = set(net.pins) - set([pin])
            others = ['%s.%s' % (x.component.refdes, x.pinnum) for x in others]
            others.sort()
            name = ', '.join(others)
        pinlist.append((pin.pinnum, pin.pinname, name))

print
print refdes
for pinnum, pinname, name in sorted(pinlist):
    print '%4s %-10s  %s' % (pinnum, pinname, name)
print
