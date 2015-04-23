=========
Stashable
=========

Stashable is a simple Django module to allow on-the-fly storage and access to model instances during development by allowing developers to stash the instances they have on hand for later use.

Quick start
-----------

0. Really install it:
    1. Clone my repository - git clone https://github.com/pinetrees/django-stashable
    2. Build the package - python setup.py sdist
    3. Install the package using pip - pip install /path/to/repository/dist/django-stashable-x.x.tar.gz

1. Add "stashable" to your INSTALLED_APPS settings:

    INSTALLED_APPS = (
        ...
        'stashable',
    )

2. Import StashableModel into your models file

3. Inherit the StashableModel in place of Django's models.Model, or use it as a mixin alongside another class:

    class SuperSecretStashedObject(StashableModel):
        ...

4. Use something fancy like django-extensions' shell_plus to import the Stash class, and instantiate it. Ideally, load the stash with the shell, for seamless ease of use. 

    SomeModuleThatYouImportFrom/SomeFileThatYouImport.py:

    from stashable.stash import Stash
    
    stash = Stash()


    settings.py:

    SHELL_PLUS_PRE_IMPORTS = (
        ('SomeModuleThatYouImportFrom.SomeFileThatYouImport', 'stash'),
    )

5. Stash your models as you work:

    me = Person.objects.filter(name="Josh")
    my_dog = me.animals.filter(type="dog").first()
    my_dogs_first_toy = my_dog.toys.first()
    
    Person.objects.filter(name="Josh").animals.filter(type="dog").first().toys.first().stash('dog_toy', stash)

    ......
    
    assert stash.dog_toy == Person.objects.filter(name="Josh").animals.filter(type="dog").first().toys.first()

6. Exit the shell and come back in. You'll find that the assertion still holds:

    assert stash.dog_toy == Person.objects.filter(name="Josh").animals.filter(type="dog").first().toys.first()

7. Open up the very short and readable stash module and look through the functionality in the Stash object:

    * update
    * clear
    * add
    * set
    * rename
    * remove
    * keys
    * length

8. Reach out to me if you find any utility here.
