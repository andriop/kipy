from .fileobjs import ConfigFile, LibDict, SchDict
from .fileobjs.paths import kicad_default_project
from .utility import FileAccess

class Project(object):
    '''  Collect all the information together about a schematic project
    '''

    def __init__(self, projdir):
        projdir = FileAccess(projdir)
        if not projdir.basename:
            projdir = projdir[-1]

        projname = projdir.basename
        projfname = projdir | projname + '.pro'
        schfname = projdir | projname + '.sch'
        default_proj = FileAccess(kicad_default_project)

        using_default = not projfname.exists
        if using_default:
            projfname = default_proj
        if not schfname.exists:
            schfname = None

        cfgfile = ConfigFile(projfname)
        if not using_default:
            defaultcfg = ConfigFile(default_proj)
            if not cfgfile.eeschema.libraries:
                cfgfile.eeschema.libraries = defaultcfg.eeschema.libraries

        self.projdir = projdir
        self.projname = projname
        self.projfname = projfname
        self.topschfname = schfname
        self.cfgfile = cfgfile

        self.libdict = LibDict(self.cfgfile, projdir)
        self.schematic = SchDict(schfname)
