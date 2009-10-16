#!/usr/bin/env python2.6
'''
     Example of how you can make a BOM.
'''
import os
import collections
import find_kipy
import kipy.project, kipy.parsesch
from kipy.utility import IndexedString, refdeslist

proj = kipy.project.Project(os.path.abspath('.'))
sch = kipy.parsesch.ParseSchematic(proj, showwarnings=False)

if sch.warnings:
    sch.dumpwarnings()
    raise SystemExit(1)

outfile = proj.projdir | proj.projname + '_bom.txt'

def buildparts(sch):
    by_ref_id = {}
    by_part_type = collections.defaultdict(set)

    class OnePart(object):
        footprint = None
        defaultfields = dict(enumerate('Value Footprint Datasheet'.split()))

        @property
        def fields(self):
            return self.__dict__

        def __init__(self, source):
            refdes = source.refdes
            parttype = source.parttype
            # These are parts I happen to not want to see in BOM
            if refdes.startswith('VIA_') or parttype == 'TP':
                return

            assert by_ref_id.setdefault(refdes, self) is self

            fields = self.fields
            self.parttype = parttype
            self.refdes = refdes
            for i, field in enumerate(source.source.fields[1:]):
                if field is None:
                    continue
                value = field[0]
                fieldname = len(field) > 8 and field[8]
                if not fieldname:
                    fieldname = self.defaultfields[i]
                assert fields.setdefault(fieldname.lower(), value) is value

        def setdefaults(self):
            # I allow a 'sameas' field to reference another reference designator.
            # Saves time and energy.
            if hasattr(self, 'sameas'):
                other = by_ref_id[IndexedString(self.sameas)]
                del self.sameas
                base = other.fields.copy()
                base.update(self.fields)
                self.fields.update(base)
            if self.footprint is not None:
                parttype = self.parttype, self.value, self.footprint
            else:
                parttype = self.parttype, self.value
            by_part_type[parttype].add(self)


    for x in sch.bomparts:
        OnePart(x)
    for x in by_ref_id.itervalues():
        x.setdefaults()

    return by_part_type

def checkparts(by_part_type):
    # Make sure that for each part type, there is only
    # one value for each field entry.
    ok = True
    result = []
    for partid, partset in sorted(by_part_type.iteritems()):
        attributes = collections.defaultdict(set)
        for part in partset:
            for attr, value in part.fields.iteritems():
                attributes[attr].add(value)
        entry = {}
        entry['refdes'] = sorted(attributes.pop('refdes'))
        badstuff = [x for x in attributes.iteritems() if len(x[1]) > 1]
        if badstuff:
            ok = False
            print partid, badstuff
        else:
            for attr, valueset in attributes.iteritems():
                entry[attr], = valueset
        result.append(entry)

    if not ok:
        raise SystemExit(1)
    return result

def getbom(parts):
    # This is my schematic-specific BOM info getter
    class BomEntry(object):
        mouser = None
        digikey = None
        Info = None

        def __init__(self, info):
            self.__dict__.update(info)
            self.numparts = len(self.refdes)
            self.refdes = refdeslist(self.refdes)

        def __cmp__(self, other):
            return cmp(str(self), str(other))
        def __str__(self):
            return str(sorted(x for x in self.__dict__.iteritems()))

    return sorted(BomEntry(x) for x in parts)

partinfo = buildparts(sch)
partinfo = checkparts(partinfo)
partinfo = getbom(partinfo)

for x in partinfo:
    print x
