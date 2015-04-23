from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class StashedObject(models.Model):
    # A slight extension of the standard use case for the Django ContentType / GenericForeignKey
    # I've added a tag, so that we can later use this as the key to our stashed object
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=32, null=True, default='', unique=True)

    @classmethod
    def set(self, content_object, name=''):
        return StashedObject.objects.create(name=name, content_object=content_object)

    @classmethod
    def recall(self, name):
        stashed_object = StashedObject.objects.filter(name=name).last()
        if stashed_object is not None:
            return stashed_object.content_object
        else:
            return None



class StashableModel(models.Model):
    class Meta:
        abstract = True

    def stash(self, name='_', stash=None):
        obj, created = StashedObject.objects.get_or_create(name=name)
        obj.content_object = self 
        obj.save()

        if stash is not None:
            stash.set(obj)

    @classmethod
    def purge(self):
        return self.objects.all().delete()


#Abstract model to add common fields to our samples
class NotableModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    note = models.TextField(null=True)

    class Meta:
        abstract = True

#Some models to demonstrate the utility of the stash
class Foo(StashableModel, NotableModel):
    bar = models.IntegerField(default=1)
    baz = models.BooleanField(default=False)
    
class Bar(StashableModel, NotableModel):
    foo = models.CharField(max_length=16)
    baz = models.BooleanField(default=True)

class Baz(StashableModel, NotableModel):
    foo = models.ForeignKey(Foo, null=True, related_name="foos")
    bar = models.ForeignKey(Bar, null=True, related_name="bars")
