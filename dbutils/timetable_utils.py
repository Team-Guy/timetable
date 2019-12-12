from authentication.models import LastTimetable
from schedule.models import User


def save_last_timetable(timetable: str, user: str):
    gmail_user = user + '@gmail.com'
    db_user = User.objects.get(email=gmail_user)
    LastTimetable(user=db_user, lastTimetable=timetable).save()


def get_differences(last_timetable: dict, generated_timetable: dict):
    pass
