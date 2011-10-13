from test_data.models import IntModel 


class Generator(object):
    
    @classmethod
    def create(cls, Model):
        return Model.objects.create(int_field=0)