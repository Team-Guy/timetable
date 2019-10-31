# Create your models here.
from django.db.models import Model, CharField, TimeField, IntegerField, TextField, EmailField


class User(Model):
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    group = CharField(max_length=10)


class SchoolActivity(Model):

    title = CharField(max_length=255)
    professor = CharField(max_length=255)
    location = CharField(max_length=255)
    group = CharField(max_length=10)
    start_time = TimeField()
    duration = IntegerField(default=2)
    frequency = CharField(max_length=5)
    priority = CharField(max_length=30)
    type = CharField(max_length=30)
