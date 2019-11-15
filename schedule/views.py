from django.http import HttpResponse
from scrapping.link import Link
from scrapping.main import getAll
from django.shortcuts import render
from dbutils.school_utils import get_faculty_activities

# Create your views here.
from scrapping.serie import Serie


def index(request):
    # getAll()
    return HttpResponse("yay")
