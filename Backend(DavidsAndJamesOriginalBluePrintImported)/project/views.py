from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response    
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from mockDiscord.models import testPerson, testPersonSerializer, Person, PersonSerializer
from rest_framework import request
from bson import ObjectId
import json
import traceback
import sys

# Create your views here.

@api_view(('GET',))
def test(*args, **kwargs):
    data =  {
            "test":"test",
            "test2":"test"
        }

    return JsonResponse(data)

@api_view(('GET',))
#@renderer_classes((JSONRenderer))
def getItemsFromDatabase(*args, **kwargs):
    #data = testPerson('Test','a2Industries@outlook.com','01-06-1993')
    #serializer = testPersonSerializer(data)

    data = testPerson.objects

    for i in data.all():
        print("Test: " + i.name)
    
    serializer = testPersonSerializer(testPerson.objects.all(), many=True)


    #Make sure all serialized data is JSON. 
    return JsonResponse(serializer.data, safe=False)

@api_view(('GET',))
#@renderer_classes((HttpResponse))
def saveTestModels(*args, **kwargs):

    data = testPerson(name='Test', email='a2Industries@outlook.com', birthday='1993-06-01')

    data.save()
    return HttpResponse('OK')

#Consider changing to a PUT request so we don't create multiple identical users.
@api_view(('POST',))
def createUser(request, *args, **kwargs):
    requestData = request.data

    #print(requestData)  

    data = Person(user_name=requestData['uname'], fname=requestData['fname'],lname=requestData['lname'], email=requestData['email'], birthday=requestData['birthday'], channels=requestData['channels'])
    data.save()
    return Response(status=200)

@api_view(('PUT',))
def updateUser(request, *args, **kwargs):
    requestData = request.data
    
    try:
        grabPerson = Person.objects.get(_id=ObjectId(requestData["_id"]))

        for key in requestData:
            if(key != "_id"):
                print(key)
                setattr(grabPerson, key, requestData[key])
        
        grabPerson.save()
        #for key in requestData:
        #    stringKey = str(key)
        #    Person.objects.filter(_id=ObjectId(requestData['id'])).update(stringKey = requestData[key])
    except Exception:
        print(traceback.format_exc())
        return Response(data="Nonexistent record", status=404)

    return Response(status=200)

@api_view(('GET',))
#@renderer_classes((JSONRenderer))
def getUsers(request, *args, **kwargs):

    serializer = PersonSerializer(Person.objects.all(), many=True)

    orderedData = serializer.data

    data = {}

    #for key, value in orderedData:
    #    print(key.__class__.__name__)
    #    if(key != "channels"):
    #        data[key] = value
    #    else:
    #        innerDict = {}
    #        for innerKey, innerValue in value:
    #            innerDict[innerKey] = innerValue
    #        data[key] = innerDict

    #Make sure all serialized data is JSON. 
    #AND REMEMBER TO PARSE IT ON THE RECEIVING END
    return JsonResponse(serializer.data, safe=False)
    #return Response(status=200)

@api_view(('DELETE',))
def deleteUser(request, *args, **kwargs):
    try:
        Person.objects.filter(_id=ObjectId(request.data["_id"])).delete()
    except Exception:
        print(traceback.format_exc())
        return Response(status=404)
    return Response(status=200)