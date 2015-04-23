from .models import *
from .stash import Stash

stash = Stash()
try: 
    foo, created = Foo.objects.get_or_create()
    bar, created = Bar.objects.get_or_create()
    baz, created = Baz.objects.get_or_create(foo=foo, bar=bar)
    stash.add('foo', foo)
    stash.add('bar', bar)
    stash.add('baz', baz)
except:
    print "Something went wrong while loading the stash"
