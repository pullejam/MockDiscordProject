from django.db import models
from rest_framework import serializers
# Create your models here.

class testPerson(models.Model):
#    def __init__(self, name, email, birthday, created=None):
#        self.name = name
#        self.email = email
#        self.birthday = birthday
    _id = models.Field(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    birthday = models.DateField()



class testPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = testPerson
        fields = ['_id','name','email','birthday']


class Person(models.Model):
    _id = models.Field(primary_key=True)
    user_name = models.CharField(max_length=200)
    fname = models.TextField()
    lname = models.TextField()
    email = models.EmailField()
    birthday = models.DateField()
    channels = models.Field()

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['_id','user_name', 'fname', 'lname', 'email', 'birthday', 'channels']

