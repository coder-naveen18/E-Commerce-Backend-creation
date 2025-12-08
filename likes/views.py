from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def firstlike(request):
    return HttpResponse('i am from the likes')