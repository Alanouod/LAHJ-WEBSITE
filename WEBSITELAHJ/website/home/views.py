# home/views.py
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def resource(request):
    return render(request, 'resource.html')

def inspiration(request):
    return render(request, 'inspiration.html')

def findPro(request):
    return render(request, 'findPro.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def joinAsPro(request):
    return render(request, 'joinAsPro.html')

def services(request):
    return render(request, 'services.html')

def reso1(request):
    return render(request, 'reso1.html')

def refe(request):
    return render(request, 'refe.html')

