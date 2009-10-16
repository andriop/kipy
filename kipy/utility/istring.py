import re

indexedsplitter = re.compile('([0-9]+)').split

def splitstr(s):
    for item in indexedsplitter(s):
        if not item:
            continue
        elif item.isdigit():
            yield int(item)
        else:
            yield item

class IndexedString(str):
    """   An indexed string is designed to sort properly alphanumerically
    """
    def __init__(self, *whatever):
        # Put the string itself into the key so that
        # 'xxx00' doesn't equal 'xxx0'
        self._key = tuple(splitstr(self)) + (str(self),)
        self._hash = hash(self._key)

    def __hash__(self):
        return self._hash
    def __eq__(self, other):
        try:                   return self._key == other._key
        except AttributeError: return str.__eq__(self, other)
    def __ne__(self, other):
        try:                   return self._key != other._key
        except AttributeError: return str.__ne__(self, other)
    def __gt__(self, other):
        try:                   return self._key >  other._key
        except AttributeError: return str.__gt__(self, other)
    def __ge__(self, other):
        try:                   return self._key >= other._key
        except AttributeError: return str.__ge__(self, other)
    def __lt__(self, other):
        try:                   return self._key <  other._key
        except AttributeError: return str.__lt__(self, other)
    def __le__(self, other):
        try:                   return self._key <= other._key
        except AttributeError: return str.__le__(self, other)
