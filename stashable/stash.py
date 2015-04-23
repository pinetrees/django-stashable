from .models import *

class Stash(object):
    _class = StashedObject

    #Update the stash when we initialize it. That covers the function we're looking for.
    def __init__(self):
        self.update()

    #Go fetch all of our stashed objects. Convert them to attributes on our object, using the name as the key.
    def update(self):
        objects = self._class.objects.all()
        dictionary = {}
        for obj in objects:
            dictionary[obj.name] = obj.content_object
        self.__dict__.update(dictionary)

    #What we want to see when we just type stash - the keys
    def __repr__(self):
        return self.keys().__str__()

    #Clear everything out of the stash. Be careful with this one. It won't ask you twice (not even once).
    def clear(self):
        self._class.objects.all().delete()
        for attr in self.keys():
            delattr(self, attr)

    #Manually add an object to the stash. You'll need to get give it a unique key, or it will override the current object stored under the key. And again, it won't ask you yet.
    def add(self, name, obj):
        _obj, created = self._class.objects.get_or_create(name=name)
        _obj.content_object = obj
        _obj.save()
        self.set(_obj)

    #This is utility. Don't use it.
    def set(self, _obj):
        setattr(self, _obj.name, _obj.content_object)

    #In case you think of something better to call your object.
    def rename(self, name, new):
        obj = getattr(self, name)
        self.add(new, obj)
        self.remove(name)

    #Remove an object from the stash by key. This doesn't delete the object from the database.
    def remove(self, name):
        self._class.objects.filter(name=name).delete()
        delattr(self, name)

    #See what's here
    def keys(self):
        return self.__dict__.keys()

    #Check how many objects you're stashing. If it gets big, its not a good stash. It isn't namespaced yet.
    def length(self):
        return len(self.keys())

