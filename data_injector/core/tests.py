from django.test import TestCase
from django.db import IntegrityError

from core.models import Generator
from test_data.models import IntModel, FloatModel

class TestInjector(TestCase):
    
    def check_this_model(self, model):
        self.assertRaises(IntegrityError, model.objects.create)
        my_int = Generator.create(model)
        self.assertTrue(isinstance(my_int,model), "The object should be of the %s class" % model)
        
    
    def test_int_model(self):
        self.check_this_model(IntModel)

       
    def test_float_models(self):
        self.check_this_model(FloatModel)

            
        