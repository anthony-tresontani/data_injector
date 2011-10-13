from django.db import models

# Create your models here.
class IntModel(models.Model):
    int_field = models.IntegerField()
    
class FloatModel(models.Model):
    char_field = models.FloatField()