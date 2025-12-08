from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def myname(request):
    return HttpResponse("Hello i am store")