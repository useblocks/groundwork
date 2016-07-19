from .sharedobject import SharedObject
from .exceptions import SharedObjectExists, SharedObjectNotRegistered


class SharedObjectManager:
    def __init__(self):
        self.shared_objects = {}

    def get(self, name, default=None):
        if name in self.shared_objects.keys():
            return self.shared_objects[name]
        else:
            return None

    def register(self, shared_object):
        if not isinstance(shared_object, SharedObject):
            raise TypeError("shared_object must be from type SharedObject not %s" % type(shared_object))

        if shared_object.name in self.shared_objects.keys():
            raise SharedObjectExists("%s is already registered" % shared_object.name)

        self.shared_objects[shared_object.name] = shared_object
        return self.shared_objects[shared_object.name]

    def set(self, shared_object):
        if not isinstance(shared_object, SharedObject):
            raise TypeError("shared_object must be from type SharedObject not %s" % type(shared_object))

        if shared_object.name not in self.shared_objects.keys():
            raise SharedObjectNotRegistered("%s is not registered/known." % shared_object.name)

    def exists(self, shared_object=None, name=None):
        if shared_object is None and name is None:
            raise Exception("shared_object or name MUST be given.")
        else:
            if shared_object is not None:
                name = shared_object.name
            if name in self.shared_objects.keys():
                return True
            else:
                return False


