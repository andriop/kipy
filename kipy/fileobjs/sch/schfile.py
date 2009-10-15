from .schitem import SchItem

class SchFile(SchItem):
    _classinit = None
    def __init__(self, sourcefile=None):
        if sourcefile != None:
            self.sourcefile = sourcefile
            self.startparse(self, sourcefile.readlinetokens())


    def render(self, linelist):
        self.EESchema.render(self, linelist)
        self.EELAYER.render(self, linelist)
        self.Descr.render(self, linelist)
        for item in self.items:
            item.render(linelist)
        self.EndSCHEMATC.render(self, linelist)

    def __str__(self):
        result = []
        self.render(result)
        result.append('')
        return '\n'.join(result)
