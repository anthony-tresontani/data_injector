import datetime
import random

from test_data.models import IntModel
from django.db.models import *



class Skip(Exception):pass

class ValueGenerator(object):

    def __init__(self, model, field):
        self.model = model
        self.field = field

    def generate(self):
        gen =  self.default_generator()
        if (self.model,self.field.name) in Generator._generators:
            gen =  Generator._generators[(self.model,self.field.name)]
        elif self.field.__class__.__name__ in Generator._generators:
            gen = Generator._generators[self.field.__class__.__name__]

        # If gen is a callable, call the function
        # else return the value
        if hasattr(gen, '__call__'):
            return gen()
        return gen


    def default_generator(self):
        raise NotImplementedError()

class IntegerGenerator(ValueGenerator):

    def default_generator(self):
        return  random.randint(0,100)

class SkipGenerator(ValueGenerator):

    def default_generator(self):
        raise Skip()

class ForeignKeyGenerator(ValueGenerator):

    def default_generator(self):
        return Generator.create(self.field.rel.to)

class FloatKeyGenerator(ValueGenerator):

    def default_generator(self):
        return random.random()

class DateFieldGenerator(ValueGenerator):

    def default_generator(self):
        return datetime.datetime.now()

class CharFieldGenerator(ValueGenerator):

    def default_generator(self):
        return "a_char"[:self.field.max_length]

class ManyToManyGenerator(ForeignKeyGenerator):

    def default_generator(self):
        values = []
        for i in range(random.randint(1,5)):
            values.append(super(ManyToManyGenerator,self).default_generator())
        return values

class Generator(object):

    _generators = {}
    _field_mapping = {"IntegerField":IntegerGenerator,
                      "BigIntegerField":IntegerGenerator,
                      "PositiveIntegerField":IntegerGenerator,
                      "PositiveSmallIntegerField":IntegerGenerator,
                      "SmallIntegerField":IntegerGenerator,
                      "AutoField":SkipGenerator,
                      "RelatedObject":SkipGenerator,
                      "ForeignKey": ForeignKeyGenerator,
                      "FloatField":FloatKeyGenerator,
                      "DateField":DateFieldGenerator,
                      "CharField":CharFieldGenerator,
                      "ManyToManyField":ManyToManyGenerator,
    }

    @classmethod
    def create(cls, model, **kwargs):
        kwargs = kwargs
        many2many=[]
        for field_name in model._meta.get_all_field_names():
            if field_name in kwargs:
                # If a value is already provided, just skip
                continue
            field = model._meta.get_field_by_name(field_name)[0]
            try:
                generator = cls._field_mapping[field.__class__.__name__]
                value = generator(model, field).generate()
                if isinstance(field, ManyToManyField):
                    many2many.append(field)
                else:
                    kwargs[field_name] = value
                    print "Assigned to %s(%s) : %s" % (field_name,field, kwargs[field_name])
            except Skip:
                pass
        obj = model.objects.create(**kwargs)
        if many2many:
            generator = cls._field_mapping["ManyToManyField"]
            for relation in many2many:
                for value in generator(model,relation).generate():
                    many2manyManager = getattr(obj,field.name)
                    many2manyManager.add(value)
            obj.save()
        return obj

    @classmethod
    def register(cls, generator, obj, field=None):
        if not field:
            # Generator associated to any field of this type
            cls._generators[obj] = generator 
        else:
            # Generator associated to a field of the model
            cls._generators[(obj,field)] = generator



