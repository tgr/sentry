from __future__ import absolute_import, print_function

__all__ = ('ImplementationManager',)


# Ideally this and PluginManager abstracted from the same base, but
# InstanceManager has become convulated and wasteful
class ImplementationManager(object):
    def __init__(self):
        self.__values = {}

    def __iter__(self):
        return self.__values.iteritems()

    def get(self, key):
        return self.__values.get(key)

    def register(self, key, cls):
        self.__values[key] = cls

    def unregister(self, key, cls):
        if self.__values[key] != cls:
            raise KeyError(key)
        del self.__values[key]
