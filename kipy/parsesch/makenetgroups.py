'''
    Make groups of partial nets.

    Make lots of little twisty, interlocking objects for easier
    ERC analysis.
'''

class Categorize(object):
    ''' Mix-in class -- requires enclosing class to have 'items' '''

    def __getattr__(self, attr):
        if not attr.startswith('find_') or not attr.endswith('s') or not attr.islower():
            raise AttributeError

        attr = attr[5:-1]
        return set((x for x in self.items if x.__class__.__name__.lower() == attr))

    @property
    def find_real_pins(self):
        return set((x for x in self.find_pins if not x.component.virtual_component))

class NetGroup(set, Categorize):
    def __init__(self, partial):
        set.__init__(self)
        self.items = set()
        self.items.update(partial)

    def merge(self, other):
        if other is self:
            return
        if len(other) > len(self):
            self, other = other, self
        for net_id in other:
            assert net_id.group is other, (net_id, net_id.group, other)
            net_id.group = self
        self.update(other)
        other.clear()
        self.items.update(other.items)
        other.items.clear()
        return self


class NetIdInfo(str, Categorize):       # Actual label

    original = None

    def __init__(self, labelstr):
        self.group = None
        self.items = set()

    def setgroup(self, group):
        assert self.group is None
        self.group = group
        group.add(self)
        return group

    def merge(self, other):
        sg = self.group
        og = other.group if isinstance(other, NetIdInfo) else other
        if sg is None:
            return self.setgroup(og)
        if og is None:
           return other.setgroup(sg)
        return sg.merge(og)

class NetIdDict(dict):
    def __missing__(self, key):
        result = NetIdInfo(key)
        self[result] = result
        return result

    def __init__(self, *arg, **kw):
        dict.__init__(self, *arg, **kw)

def makegroups(partials):
    by_net_id = NetIdDict()
    allgroups = []

    for partial in partials:
        partial.net_ids = net_ids = set()
        for item in partial:
            item.partial = partial
            item_net_ids = item.net_ids
            if item_net_ids:
                item_net_ids = [by_net_id[x] for x in item_net_ids]
                item.net_ids = tuple(item_net_ids)
                for net_id in item_net_ids:
                    net_id.items.add(item)
                net_ids.update(item_net_ids)

        group = NetGroup(partial)
        allgroups.append(group)
        for net_id in net_ids:
            group = net_id.merge(group)

    return by_net_id, allgroups
