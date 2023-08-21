from django.db import models
from rest_framework import serializers
from djongo import models
# Create your models here.

class testPerson(models.Model):
#    def __init__(self, name, email, birthday, created=None):
#        self.name = name
#        self.email = email
#        self.birthday = birthday
    name = models.CharField(max_length=200)
    email = models.EmailField()
    birthday = models.DateField()



class testPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = testPerson
        fields = ['name','email','birthday']


class Message(models.Model):
    _id = models.ObjectIdField()
    userId = models.TextField()
    user_name = models.TextField()
#    date_time = models.DateTimeField()
    date_time = models.TextField() # changing this to a text field because the other one is stupidly ornery about the typing.
    message_content = models.CharField(max_length=1200)

class Channel(models.Model):
    _id = models.ObjectIdField()
    id = models.TextField()
    name = models.TextField()
    message = models.ArrayField(model_container=Message)


class Person(models.Model):
    _id = models.ObjectIdField()
    user_name = models.CharField(max_length=200)
    fname = models.TextField()
    lname = models.TextField()
    email = models.EmailField()
    birthday = models.DateField()
    password = models.TextField()
    channels = models.JSONField()

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['_id','user_name', 'fname', 'lname', 'email', 'birthday', 'password','channels']
        #fields = ['user_name', 'fname', 'lname', 'email', 'birthday', 'channels']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['_id', 'id', 'name', 'message']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['_id','userId', 'user_name', 'date_time','message_content']
