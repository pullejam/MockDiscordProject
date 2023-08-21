from django.shortcuts import render

# Create your views here.

def signupPage(request):
    return render(request, 'SignUp.html')

def loginPage(request):
    return render(request, 'SignIn.html')