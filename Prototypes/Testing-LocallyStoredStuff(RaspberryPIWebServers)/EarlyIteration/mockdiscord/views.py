from django.shortcuts import render

def homepage(request):
	return render(request, 'index.html')
def loginpage(request):
	return render(request, 'SignIn.html')
def signuppage(request):
	return render(request, 'SignUp.html')
