import json

from authentication.models import LastTimetable
from schedule.models import User


def save_last_timetable(timetable: str, username: str):
    gmail_user = username + '@gmail.com'
    db_user = User.objects.get(email=gmail_user)
    LastTimetable(user=db_user, lastTimetable=timetable).save()


def get_last_timetable(username):
    username = username + '@gmail.com'
    user = User.objects.get(email=username)
    last = LastTimetable.objects.get(user=user).lastTimetable
    return json.loads(LastTimetable.objects.get(user=user).lastTimetable)



def get_differences(last_timetable: dict, generated_timetable: dict):
    pass
