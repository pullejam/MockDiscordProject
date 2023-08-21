"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DatabaseAPI.views import addChannelToUser, createNewChannel, delChannelFromUser, getChannelsForUser, getUserByChannelId, getUserById, getUserByUserName, writeMessage, getMessages, logIn
from DatabaseAPI.views import test,getItemsFromDatabase,saveTestModels,createUser,updateUser, getUsers, deleteUser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),
    path('testPerson/', getItemsFromDatabase),  
    path('addTestData/', saveTestModels),
    path('addUser/', createUser),
    path('updateUser/',updateUser),
    path('getPersons/',getUsers),
    path('getUserByUserName/',getUserByUserName),
    path('getUserById/',getUserById),
    path('deletePerson/', deleteUser),
    path('getUserByChannelId/', getUserByChannelId),
    path('addChannel/', addChannelToUser),
    path('delChannelFromUser/',delChannelFromUser),
    path('createNewChannel/',createNewChannel),
    path('getUserChannels/',getChannelsForUser),
    path('addMessage/',writeMessage),
    path('getMessages/', getMessages),
    path('logIn/', logIn),

]

