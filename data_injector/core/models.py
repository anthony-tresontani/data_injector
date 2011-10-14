import datetime
import random

from test_data.models import IntModel
from django.db.models import *


class Generator(object):
    
    @classmethod
    def create(cls, Model, **kwargs):
        kwargs = kwargs
        for field_name in Model._meta.get_all_field_names():
            if field_name in kwargs:
                # If a value is already provided, just skip
                continue
            field = Model._meta.get_field_by_name(field_name)[0]
            value = None
            if isinstance(field, (AutoField, related.RelatedObject)):
                continue
            if isinstance(field, ForeignKey):
                value = cls.create(field.rel.to)
            if isinstance(field, (IntegerField,
                                  BigIntegerField,
                                  PositiveIntegerField,
                                  PositiveSmallIntegerField,
                                  SmallIntegerField)):
                value = random.randint(0,100)
            if isinstance(field, FloatField):
                value = random.random()
            if isinstance(field, CharField):
                value ="a_char"[:field.max_length]
            if isinstance(field, DateField):
                value = datetime.datetime.now()
            kwargs[field_name]=value
            print "Assigned to %s(%s) : %s" % (field_name,field, value)
        return Model.objects.create(**kwargs)