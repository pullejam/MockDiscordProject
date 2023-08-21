from django.http import response
from django.http.response import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import serializers
from rest_framework.response import Response    
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from DatabaseAPI.models import testPerson, testPersonSerializer, Person, PersonSerializer, Channel, ChannelSerializer, Message, MessageSerializer
from rest_framework import request
from bson import ObjectId
import json
import traceback
import sys
import ast
import re
from collections import OrderedDict
from django.http import HttpResponseRedirect
import bcrypt

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
    isNeumont = requestData['isFromNeumont']

    initPass = requestData["password"]
    verPass = requestData["passwordVerify"]

    if initPass == verPass:
        pass
    else:
        if isNeumont == "true":
            return HttpResponseRedirect(redirect_to="http://10.10.16.84/account/signup/")
        else:
        # Make error
            return HttpResponseRedirect(redirect_to="https://www.delware.tech/account/signup/")

    #print(requestData)  
    if Person.objects.filter(user_name=requestData['user_name']).exists():
        if isNeumont == "true":
            return HttpResponseRedirect(redirect_to="http://10.10.16.84/account/signup/")
        else:
        # Make error
            return HttpResponseRedirect(redirect_to="https://www.delware.tech/account/signup/")
    else:
        # salt = bcrypt.gensalt(rounds = 16);
        hashedPass = bcrypt.hashpw(initPass.encode('utf8'), bcrypt.gensalt(16))
        endpass = hashedPass.decode('utf8')
        data = Person(user_name=requestData['user_name'], fname=requestData['fname'],lname=requestData['lname'], email=requestData['email'], birthday=requestData['birthday'], password=endpass, channels=[])
        data.save()

    if isNeumont == "true":
        return HttpResponseRedirect(redirect_to="http://10.10.16.84/account/login/")
    else:
        return HttpResponseRedirect(redirect_to="https://www.delware.tech/account/login/")

@api_view(('GET','POST'))
def logIn(request, *args, **kwargs):
    requestdata = request.data
    isNeumont = requestdata['isFromNeumont']
    userName = requestdata["user_name"]
    pw = requestdata['pw']
    dataList = {}
    if Person.objects.filter(user_name=userName).exists():
        person = Person.objects.get(user_name=userName)
        serializer = PersonSerializer(person)
        match = bcrypt.checkpw(pw.encode('utf8'), str(serializer.data['password']).encode('utf8'))
        if match:
            
            dataList["isValid"] = ("true")
            return JsonResponse(dataList, safe=False)
        else:
            pass
    dataList = {
        "isValid":"false"
    }
    return JsonResponse(dataList, safe=False)
            



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

    #Done so an actual call to the database is performed.
    
    dataList = []

    for item in serializer.data:
        dataDict = {
            "_id":item["_id"],
            "user_name":item["user_name"],
            "fname":item["fname"],
            "lname":item["lname"],
            "email":item["email"],
            "birthday":item["birthday"],
    #   error
    # 
            "channels":eval(item["channels"])
        }
        dataList.append(dataDict)





    #Make sure all serialized data is JSON. 
    #AND REMEMBER TO PARSE IT ON THE RECEIVING END
    return JsonResponse(dataList, safe=False)
    #return Response(status=200)

@api_view(('GET','POST',))
def getUserById(request, *args, **kwargs):

    person = Person.objects.get(_id=ObjectId(request.data["id"]))
    serializer = PersonSerializer(person)
        
    data = {
        "id":serializer.data["_id"],
        "user_name":serializer.data["user_name"],
        "fname":serializer.data["fname"],
        "lname":serializer.data["lname"],
        "email":serializer.data["email"],
        "birthday":serializer.data["birthday"],
        "channels":(serializer.data["channels"])
    }

    return JsonResponse(data, safe=False)



@api_view(('GET','POST',))
def getUserByUserName(request, *args, **kwargs):

    if Person.objects.filter(user_name=request.data['user_name']).exists():
        person = Person.objects.get(user_name=request.data["user_name"])
        serializer = PersonSerializer(person)
            
        data = {
            "id":serializer.data["_id"],
            "user_name":serializer.data["user_name"]
        }

        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotFound





@api_view(('DELETE',))
def deleteUser(request, *args, **kwargs):
    try:
        Person.objects.filter(_id=ObjectId(request.data["_id"])).delete()
    except Exception:
        print(traceback.format_exc())
        return Response(status=404)
    return Response(status=200)

@api_view(('GET',))
def getUserByChannelId(request, *args, **kwargs):
    try:
        #serializer = PersonSerializer(Person.objects.filter(channels__in=ObjectId(request.data["_id"])), many=True) use this when we've got proper objectIds to reference and put in
        serializer = PersonSerializer(Person.objects.filter(channels__contains=request.data["_id"]), many=True)
        #serializer.data["channels"] = ast.literal_eval(serializer.data["channels"]) This doesn't work, unfortunately.

        print(serializer.data["channels"])


        data = {
            "id":serializer.data["id"],
            "user_name":serializer.data["user_name"],
            "channels":ast.literal_eval(serializer.data["channels"])
        }


        return JsonResponse(data, safe=False)
    except Exception:
        print(traceback.format_exc())
        return Response(status=404)

@api_view(('POST',))
def addChannelToUser(request, *args, **kwargs):

    try:
    
        channel = Channel.objects.get(_id=ObjectId(request.data["channels"]))
        channelserializer = ChannelSerializer(channel)
    
        personToModify = Person.objects.get(_id=ObjectId(request.data["_id"]))
        # print(type(request.data["channels"]))

        channelSet = {
            "id":channelserializer.data["id"],
            "name":channelserializer.data["name"],

        }
        
        personToModify.channels.append(dict(channelSet))
        personToModify.save()
        return Response(status=201)
    except:
        return Response(status=204)
    

@api_view(('DELETE',))
def delChannelFromUser(request, *args, **kwargs):
    personToModify = Person.objects.get(_id=ObjectId(request.data["_id"]))
    for item in request.data["channels"]:
        personToModify.channels.remove(item)
    personToModify.save()
    return Response(status=200)

@api_view(('POST',))
def createNewChannel(request, *args, **kwargs):
    messages = []
    #should remove the message creation here - when creating a channel we should not have to have an initial message
    # for item in request.data:
    #     # print(item["userId"])
    #     # print(item["date_time"])
    #     # print(item["message"])
    #     messages.append(Message(userId=ObjectId(item["userId"]), date_time=item["date_time"], message_content=item["message"]))


    print(messages)

    for item in messages:
        item.save()

    messageSerializer = MessageSerializer(messages, many=True)

    print(messageSerializer.data)

    data = []

    for item in messageSerializer.data:
        print(item)
        data.append(item)
    


    channelObject = Channel.objects.create()
    channelObject.name=request.data["name"]
    channelObject.id = channelObject._id
    channelObject.message = messages
    
    # channelSerializer = ChannelSerializer(channelObject)
    

    # print(channelSerializer.data)

    channelObject.save()
    ITAM = {"channelID":str(channelObject.id) }
    return JsonResponse(ITAM, safe=False)

@api_view(('POST',))
def getChannelsForUser(request, *args, **kwargs):
    person = Person.objects.get(_id=ObjectId(request.data["_id"]))

    channelList = []
    for item in person.channels:
        channelObj = Channel(id=ObjectId(item["id"]), name=item["name"], message="")
        channelList.append(channelObj)

    senddata = []
    for item in channelList:
        channelserializer = ChannelSerializer(item)
        senddata.append(channelserializer.data)
    return JsonResponse(senddata, safe=False)


#Post to this with the userId sending the message and the channel id sending it. This is to add messages to channels.
@api_view(('POST',))
def writeMessage(request, *args, **kwargs):
    try:
        message = Message(userId=request.data["userId"], user_name=request.data["user_name"], date_time=request.data["date_time"], message_content=request.data["message_content"])
        channel = Channel.objects.get(_id=ObjectId(request.data["channelId"]))
        message.save()
        messageSerializer = MessageSerializer(message)
        channel.message.append(messageSerializer.data)
        channel.save()
        
        return redirect(request.data["originalURL"])

    except:
        return HttpResponseRedirect(redirect_to="/")



@api_view(('POST',))
def getMessages(request, *args, **kwargs):
    channel = Channel.objects.get(id=ObjectId(request.data["channelId"]))
    
    messageList = []

    for item in channel.message:
        messageObject = Message(userId=item["userId"], user_name=item["user_name"], date_time = item["date_time"], message_content = item["message_content"])
        messageList.append(messageObject)

    #print(messageList)
    serializedData = []

    for item in messageList:
        messageSerializer = MessageSerializer(item)
        print(messageSerializer.data)
        serializedData.append(messageSerializer.data)

    print(serializedData)

    return JsonResponse(data=serializedData, safe=False)


