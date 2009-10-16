import re
import types

class IndexedString(str):
    """   An indexed string is designed to sort properly alphanumerically
    """
    _indexedsplitter = types.MethodType(re.compile('([0-9]+)').split, None, str)

    def __init__(self, *whatever):
        # Put the string itself into the key so that
        # 'xxx00' doesn't equal 'xxx0'
        key = [int(x) if x.isdigit() else x for x in self._indexedsplitter()]
        key.append(str(self))
        self._key = key = tuple(key)
        self._hash = hash(key)

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
