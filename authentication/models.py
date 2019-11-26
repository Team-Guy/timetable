from django.db.models import Model, OneToOneField, CASCADE, TimeField, TextField
from schedule.models import User
import datetime


# Create your models here.

class Preference(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    mondayStart = TimeField(default=datetime.time(8, 0, 0))
    tuesdayStart = TimeField(default=datetime.time(8, 0, 0))
    wednesdayStart = TimeField(default=datetime.time(8, 0, 0))
    thursdayStart = TimeField(default=datetime.time(8, 0, 0))
    fridayStart = TimeField(default=datetime.time(8, 0, 0))
    mondayEnd = TimeField(default=datetime.time(20, 0, 0))
    tuesdayEnd = TimeField(default=datetime.time(20, 0, 0))
    wednesdayEnd = TimeField(default=datetime.time(20, 0, 0))
    thursdayEnd = TimeField(default=datetime.time(20, 0, 0))
    fridayEnd = TimeField(default=datetime.time(20, 0, 0))


class LastTimetable(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    lastTimetable = TextField()
