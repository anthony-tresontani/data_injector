from django.test import TestCase
from django.db import IntegrityError

from core.models import Generator
from test_data.models import *

class TestInjector(TestCase):
    
    def check_this_model(self, model):
        self.assertRaises(IntegrityError, model.objects.create)
        my_obj = Generator.create(model)
        self.assertTrue(isinstance(my_obj,model), "The object should be of the %s class" % model)
        
    
    def test_int_model(self):
        self.check_this_model(IntModel)
        self.check_this_model(BigIntegerModel)
        self.check_this_model(PositiveIntegerModel)
        self.check_this_model(PositiveSmallIntegerModel)

       
    def test_float_models(self):
        self.check_this_model(FloatModel)
        
    def test_char_field(self):
        self.check_this_model(CharModel)
        self.check_this_model(SmallCharModel)
        
    def test_date_field(self):
        self.check_this_model(DateModel)
        
    def test_foreign_field(self):
        self.check_this_model(ForeignModel)
        
    def test_partial_value(self):
        my_obj = Generator.create(CharModel, int_field=18)
        self.assertEquals(my_obj.int_field, 18)
        