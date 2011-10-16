from django.db import models

# Create your models here.
class IntModel(models.Model):
    int_field = models.IntegerField()
    
class BigIntegerModel(models.Model):
    int_field = models.BigIntegerField()
    
class PositiveIntegerModel(models.Model):
    int_field = models.PositiveIntegerField()
    
class PositiveSmallIntegerModel(models.Model):
    int_field = models.PositiveSmallIntegerField()
    
class FloatModel(models.Model):
    float_field = models.FloatField()
    
class CharModel(models.Model):
    int_field = models.IntegerField()
    char_field = models.CharField(max_length=10)
    
class SmallCharModel(models.Model):
    int_field = models.IntegerField()
    char_field = models.CharField(max_length=2)

class DateModel(models.Model):
    date_field = models.DateField()
    
class ForeignModel(models.Model):
    foreign_field = models.ForeignKey(IntModel)
    foreign_field_2 = models.ForeignKey(CharModel)
    int_field = models.IntegerField()

class Many2ManyModel(models.Model):
    many2many = models.ManyToManyField(IntModel)