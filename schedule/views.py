from django.http import HttpResponse
from scrapping.Link import Link
from scrapping.main import getInfo
from django.shortcuts import render
# Create your views here.

def index(request):
    # getInfo(Link.IE3)
    return HttpResponse("yay")
