from django.http import HttpResponse
from scrapping.link import Link
from scrapping.main import getAll
from django.shortcuts import render


# Create your views here.

def index(request):
    # getAll()
    return HttpResponse("yay")
