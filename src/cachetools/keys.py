"""Key functions for memoizing decorators."""
__all__ = 'hashkey', 'methodkey', 'typedkey', 'typedmethodkey'


class _HashedTuple(tuple):
    """A tuple that ensures that hash() will be called no more than once
    per element, since cache decorators will hash the key multiple
    times on a cache miss.  See also _HashedSeq in the standard
    library functools implementation.

    """
    __hashvalue = None

    def __hash__(self, hash=tuple.__hash__):
        hashvalue = self.__hashvalue
        if hashvalue is None:
            self.__hashvalue = hashvalue = hash(self)
        return hashvalue

    def __add__(self, other, add=tuple.__add__):
        return _HashedTuple(add(self, other))

    def __radd__(self, other, add=tuple.__add__):
        return _HashedTuple(add(other, self))

    def __getstate__(self):
        return {}


_kwmark = _HashedTuple,


def hashkey(*args, **kwargs):
    """Return a cache key for the specified hashable arguments."""
    key = args
    if kwargs:
        key += (_kwmark,)
        for item in kwargs.items():
            key += item
    return _HashedTuple(key)


def methodkey(self, *args, **kwargs):
    """Return a cache key for use with cached methods."""
    return hashkey(self.__class__, *args, **kwargs)


def typedkey(*args, **kwargs):
    """Return a typed cache key for the specified hashable arguments."""
    key = tuple(type(arg) for arg in args)
    if kwargs:
        key += (_kwmark,)
        for item in kwargs.items():
            key += (item[0], type(item[1]))
    return _HashedTuple(key)


def typedmethodkey(self, *args, **kwargs):
    """Return a typed cache key for use with cached methods."""
    return typedkey(self.__class__, *args, **kwargs)
