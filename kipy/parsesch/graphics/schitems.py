class SchItem(object):

    from .primitives import Point, Line, Rectangle
    from kipy.utility import MetaHelper as __metaclass__
    from kipy.fileobjs import SchItem as FileSchItem

    class PinOrLabel(Point):
        pass

    class Keepout(Rectangle):
        def __init__(self, userinfo, *args):
            self.install(*args)
            self.userinfo = userinfo

    _dispatchdict = {}
    fileclass = None
    add_dispatch = True

    @classmethod
    def _classinit(cls, base):
        if base is None:
            cls._rootclass = cls
            return
        if cls.add_dispatch:
            fileclass = getattr(cls.FileSchItem, cls.fileclass or cls.__name__)
            cls._dispatchdict[fileclass] = cls
        setattr(cls._rootclass, cls.__name__, cls)

    @classmethod
    def dispatch(cls, sourcefields, page):
        dispatchdict = cls._dispatchdict
        for item in sourcefields:
            dispatchdict[item.__class__](item, page)

    def normalize_name(self, nametype, name, warnobj=None):
        new = name.replace(' / ', '_/_')
        if new != name:
            wparams = nametype, name, new
            wmsg = ('%s name changed to simplify processing:\n' +
                        '               %s changed to %s') % wparams
            getattr(self, 'warn', warnobj)(wmsg)
        return new

    @staticmethod
    def pagejoin(page, name, separator=' / '):
        page = page.split(separator, 1)
        page[0] = ''
        page.append(name)
        return separator.join(page)

class Connection(SchItem, SchItem.Point):
    def __init__(self, item, page):
        self.install(page, item.posx, item.posy)

class NoConn(SchItem, SchItem.Point):
    def __init__(self, item, page):
        self.install(page, item.posx, item.posy)

class Wire(SchItem, SchItem.Line):
    ignore = ('Notes Line',)
    keep = 'Wire Line', 'Bus Line'
    def __init__(self, item, page):
        wiretype = item.wiretype
        if wiretype in self.keep:
            self.install(page, item.startx, item.starty, item.endx, item.endy)
            self.wiretype = wiretype
        else:
            assert wiretype in self.ignore, wiretype  # Others not supported yet
            self.Keepout(wiretype, page, item.startx, item.starty, item.endx, item.endy)

class Kmarq(SchItem, SchItem.PinOrLabel):
    def __init__(self, item, page):
        page.warn(item.text)

class Entry(SchItem, SchItem.Keepout):

    def makekeepout(self, page, x1, y1, x2, y2):
        # For simplicity, make a keepout that
        # doesn't impinge on the pins

        def shrink(a, b, percent=95):
            frac1 = percent / 100.0
            frac2 = 1.0 - frac1
            return int(round(a * frac1 + b * frac2))

        self.install(page, shrink(x1, x2), shrink(y1, y2),
                           shrink(x2, x1), shrink(y2, y1))

    def __init__(self, item, page):
        wiretype = item.wiretype
        assert wiretype in self.Wire.keep, wiretype
        x1, y1, x2, y2 = item.startx, item.starty, item.endx, item.endy
        self.makekeepout(page, x1, y1, x2, y2)
        self.page = page
        self.userinfo = 'Entry ' + wiretype
