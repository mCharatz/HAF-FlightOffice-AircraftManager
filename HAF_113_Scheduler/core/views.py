import imp
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'core/index.html')

def upload(request):
    return render(request,'core/upload_file.html')